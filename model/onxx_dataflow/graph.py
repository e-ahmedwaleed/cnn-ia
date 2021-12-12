import onnx

from model.onxx_dataflow.graph_properties import Node


class Graph:
    def __init__(self, path):
        self.path = path

    def identify_model_graph(self):
        model = onnx.load(self.path)
        onnx.checker.check_model(model)
        from onnx import numpy_helper

        onnx_initializers = {}
        for initializer in model.graph.initializer:
            w = numpy_helper.to_array(initializer)
            onnx_initializers[initializer.name] = w

        onnx_nodes = {}
        onnx_nodes_inputs = {}
        onnx_nodes_outputs = {}
        for i, node_data in enumerate(model.graph.node):
            onnx_nodes[i] = Node(node_data)
            onnx_nodes_inputs[onnx_nodes[i].name] = node_data.input
            onnx_nodes_outputs[onnx_nodes[i].name] = node_data.output

        # Assuming that the model will have a single input/output
        onnx_nodes[0].inputs[0] = "MODEL_INPUT: " + self.identify_dim(model.graph.input)
        onnx_nodes[len(onnx_nodes) - 1].outputs[0] = "MODEL_OUTPUT: " + self.identify_dim(model.graph.output)
        for i in onnx_nodes:
            onnx_nodes[i].identify_node_inputs(onnx_nodes_outputs)
            onnx_nodes[i].identify_node_outputs(onnx_nodes_inputs)
            onnx_nodes[i].identify_node_parameters(onnx_initializers)
            print(onnx_nodes[i])

    def visualize(self):
        import netron
        netron.start(self.path)

    @staticmethod
    def identify_dim(var):
        dims = [[d.dim_value for d in _var.type.tensor_type.shape.dim] for _var in var][0]
        # TODO: output a warning when there is an unknown dimension
        for i, dim in enumerate(dims):
            if not dim:
                dims[i] = 1
        return str(dims).replace('[', '(').replace(']', ')')
