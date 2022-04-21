# The standard model used for generation:
# https://www.analyticsvidhya.com/blog/2020/07/how-to-train-an-image-classification-model-in-pytorch-and-tensorflow/

def generate(path, library, epochs):
    if "TensorFlow" in library:
        from model.examples.cnn_tensorflow import TensorflowImplementation
        mnist_model = TensorflowImplementation()
    elif "PyTorch" in library:
        from model.examples.cnn_pytorch import PyTorchImplementation
        mnist_model = PyTorchImplementation()

    # noinspection PyUnboundLocalVariable
    model_path = mnist_model.generate_model(path, epochs)
    return model_path if model_path else path
