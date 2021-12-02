def generate(path, library, epochs):
    if library == "TensorFlow":
        from model.examples.cnn_tensorflow import TensorflowImplementation
        tensorflow_model = TensorflowImplementation()
        tensorflow_model.generate_model(epochs)
        return tensorflow_model.save_model(path)
    else:
        from model.examples.cnn_pytorch import PyTorchImplementation
        pytorch_model = PyTorchImplementation()
        pytorch_model.generate_model(epochs)
        return pytorch_model.save_model(path)
