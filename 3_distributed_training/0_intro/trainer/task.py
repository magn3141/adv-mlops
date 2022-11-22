import tensorflow as tf
import tensorflow_datasets as tfds
import os


PER_REPLICA_BATCH_SIZE = 64
EPOCHS = 2

# TODO: replace {your-gcs-bucket} with the name of the Storage bucket you created earlier
BUCKET = 'gs://adv-mlops-bucket-2/mwms'

def preprocess_data(image, label):
  '''Resizes and scales images.'''

  image = tf.image.resize(image, (300,300))
  return tf.cast(image, tf.float32) / 255., label


def create_dataset(batch_size):
  '''Loads Cassava dataset and preprocesses data.'''

  data, info = tfds.load(name='cassava', as_supervised=True, with_info=True)
  number_of_classes = info.features['label'].num_classes
  train_data = data['train'].map(preprocess_data,
                                 num_parallel_calls=tf.data.experimental.AUTOTUNE)
  train_data  = train_data.shuffle(1000)
  train_data  = train_data.batch(batch_size)
  train_data  = train_data.prefetch(tf.data.experimental.AUTOTUNE)

  # Set AutoShardPolicy
  options = tf.data.Options()
  options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
  train_data = train_data.with_options(options)

  return train_data, number_of_classes


def create_model(number_of_classes):
  '''Creates and compiles pretrained ResNet50 model.'''

  base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False)
  x = base_model.output
  x = tf.keras.layers.GlobalAveragePooling2D()(x)
  x = tf.keras.layers.Dense(1016, activation='relu')(x)
  predictions = tf.keras.layers.Dense(number_of_classes, activation='softmax')(x)
  model = tf.keras.Model(inputs=base_model.input, outputs=predictions)

  model.compile(
      loss='sparse_categorical_crossentropy',
      optimizer=tf.keras.optimizers.Adam(0.0001),
      metrics=['accuracy'])

  return model


def _is_chief(task_type, task_id):
  '''Helper function. Determines if machine is chief.'''

  return task_type == 'chief'


def _get_temp_dir(dirpath, task_id):
  '''Helper function. Gets temporary directory for saving model.'''

  base_dirpath = 'workertemp_' + str(task_id)
  temp_dir = os.path.join(dirpath, base_dirpath)
  tf.io.gfile.makedirs(temp_dir)
  return temp_dir


def write_filepath(filepath, task_type, task_id):
  '''Helper function. Gets filepath to save model.'''

  dirpath = os.path.dirname(filepath)
  base = os.path.basename(filepath)
  if not _is_chief(task_type, task_id):
    dirpath = _get_temp_dir(dirpath, task_id)
  return os.path.join(dirpath, base)


def main():
  # Create strategy
  strategy = tf.distribute.MultiWorkerMirroredStrategy()

  # Get data
  global_batch_size = PER_REPLICA_BATCH_SIZE * strategy.num_replicas_in_sync
  train_data, number_of_classes = create_dataset(global_batch_size)

  # Wrap variable creation within strategy scope
  with strategy.scope():
    model = create_model(number_of_classes)

  model.fit(train_data, epochs=EPOCHS)

  # Determine type and task of the machine from
  # the strategy cluster resolver
  task_type, task_id = (strategy.cluster_resolver.task_type,
                        strategy.cluster_resolver.task_id)

  # Based on the type and task, write to the desired model path
  write_model_path = write_filepath(BUCKET, task_type, task_id)
  model.save(write_model_path)

if __name__ == "__main__":
    main()