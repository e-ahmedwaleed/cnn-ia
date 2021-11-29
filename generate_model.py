from Models.TensorFlow.implementing_a_cnn_in_tensorflow import ImplementingTensorflow
from Models.PyTorch.implementing_a_cnn_in_pytorch import ImplementingPyTorch


# from Models.PyTorch.implementing_a_cnn_in_pytorch import ImplementPyTorch

def generate(path, method):
    if method == "PyTorch":
        pytorch_model = ImplementingPyTorch()
        pytorch_model.generate_model()
        return pytorch_model.save_model(path)
    else:
        tensorflow_model = ImplementingTensorflow()
        tensorflow_model.generate_model()
        return tensorflow_model.save_model(path)
