from example_models.cnn_in_tensorflow import TensorflowImplementation
from example_models.cnn_in_pytorch import PyTorchImplementation


def generate(path, method):
    if method == "Tensorflow":
        tensorflow_model = TensorflowImplementation()
        tensorflow_model.generate_model()
        return tensorflow_model.save_model(path)
    else:
        pytorch_model = PyTorchImplementation()
        pytorch_model.generate_model()
        return pytorch_model.save_model(path)
