def generate(path, library, epochs):
    if "TensorFlow" in library:
        from model.examples.cnn_tensorflow import TensorflowImplementation
        tensorflow_model = TensorflowImplementation()
        tensorflow_model.generate_model(epochs)
        return tensorflow_model.save_model(path)
    elif "PyTorch" in library:
        from model.examples.cnn_pytorch import PyTorchImplementation
        pytorch_model = PyTorchImplementation()
        return pytorch_model.generate_model(path, epochs)
    else:
        return path
