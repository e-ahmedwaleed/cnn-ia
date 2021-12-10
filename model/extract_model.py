import onnx


def extract(path):
    model = onnx.load(path)
    onnx.checker.check_model(model)
    from onnx import numpy_helper
    initializers = model.graph.initializer

    onnx_weights = {}
    for initializer in initializers:
        w = numpy_helper.to_array(initializer)
        onnx_weights[initializer.name] = w

    return "Model Extracted Successfully."
