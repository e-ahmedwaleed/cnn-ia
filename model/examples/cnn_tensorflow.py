import tensorflow as tf

tf.get_logger().setLevel('ERROR')

from tensorflow.keras import datasets, layers, models
from tensorflow.keras.utils import to_categorical


# noinspection SpellCheckingInspection
class TensorflowImplementation(object):
    def __init__(self):
        self.model = models.Sequential()

    def generate_model(self, epochs):
        """ Load and prepare the dataset """

        (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data(path='mnist.npz')
        # Normalize pixel values to be between 0 and 1
        train_images, test_images = train_images / 255.0, test_images / 255.0

        # reshaping the images
        train_images = train_images.reshape((60000, 28, 28, 1))
        test_images = test_images.reshape((10000, 28, 28, 1))

        # one hot encoding the target variable
        train_labels = to_categorical(train_labels)
        test_labels = to_categorical(test_labels)

        """ Build/Train the model """

        # defining the model architecture
        self.model.add(layers.Conv2D(4, (3, 3), activation='relu', input_shape=(28, 28, 1)))
        self.model.add(layers.MaxPooling2D((2, 2), strides=2))
        self.model.add(layers.Conv2D(4, (3, 3), activation='relu'))
        self.model.add(layers.MaxPooling2D((2, 2), strides=2))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(10, activation='softmax'))

        # compiling the model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        """ Train the model """

        # training the model
        self.model.fit(train_images, train_labels, epochs=epochs, validation_data=(test_images, test_labels))

    def save_model(self, path):
        path = path + "/CNN-TensorFlow-mnist"
        import os
        try:
            os.mkdir(path)
        except OSError:
            pass
        self.model.save(path)
        return path
