import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from example_models.cnn_tensorflow import TensorflowImplementation
from example_models.cnn_pytorch import PyTorchImplementation


def generate(epochs, path, library):
    if library == "TensorFlow":
        tensorflow_model = TensorflowImplementation()
        tensorflow_model.generate_model(epochs)
        return tensorflow_model.save_model(path)
    else:
        pytorch_model = PyTorchImplementation()
        pytorch_model.generate_model(epochs)
        return pytorch_model.save_model(path)
