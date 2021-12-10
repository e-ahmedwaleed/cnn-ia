import onnx


def extract(path):
    model = onnx.load(path)
    onnx.checker.check_model(model)
    from onnx import numpy_helper

    onnx_weights = {}
    for initializer in model.graph.initializer:
        w = numpy_helper.to_array(initializer)
        onnx_weights[initializer.name] = w

    onnx_nodes = {}
    onnx_nodes_inputs = {}
    onnx_nodes_outputs = {}
    onnx_nodes_attributes = {}
    for i, node in enumerate(model.graph.node):
        onnx_nodes[i] = node.op_type

        onnx_nodes_inputs[i] = node.input
        if len(node.input) > 1:
            weights = {}
            for j, weight in enumerate(node.input[1:]):
                # noinspection PyUnresolvedReferences
                weights[i + j] = onnx_weights[weight]
                onnx_nodes_inputs[i][j + 1] = str(weights[i + j].dtype) + ":" + str(weights[i + j].shape)

        onnx_nodes_outputs[i] = node.output

        attributes = {}
        for k, attribute in enumerate(node.attribute):
            attributes[k] = attribute.name
        onnx_nodes_attributes[i] = attributes

    print(onnx_weights.keys())

    print(onnx_nodes)
    print(onnx_nodes_inputs)
    print(onnx_nodes_outputs)
    print(onnx_nodes_attributes)

    import re

    # TODO: output a warning when there is an unknown dimension
    print(re.sub('\"unk[_0-9]*\"', '1', str(model.graph.input[0])))
    print(re.sub('\"unk[_0-9]*\"', '1', str(model.graph.output[0])))

    return "Model Extracted Successfully."
