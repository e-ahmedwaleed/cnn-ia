import onnx

from gui import utils
from onnx import numpy_helper

from model.onxx_dataflow.graph_dims import GraphDims
from model.onxx_dataflow.graph_properties import Node


class Graph:
    def __init__(self, path):
        self.path = path
        self.onnx_nodes = []

    def identify_model_graph(self):
        # Reset node ids for every model
        Node.type_id = {}

        model = onnx.load(self.path)
        onnx.checker.check_model(model)

        # Extract model parameters
        onnx_initializers = {}
        for initializer in model.graph.initializer:
            w = numpy_helper.to_array(initializer)
            onnx_initializers[initializer.name] = w

        # Extract model layers
        onnx_nodes_inputs = {}
        onnx_nodes_outputs = {}
        for i, node_data in enumerate(model.graph.node):
            self.onnx_nodes.append(Node(node_data))
            onnx_nodes_inputs[self.onnx_nodes[i].name] = node_data.input
            onnx_nodes_outputs[self.onnx_nodes[i].name] = node_data.output

        # Create a parallel model to identify the output of every layer
        graph_outputs = GraphDims(self.path, onnx_nodes_outputs)

        # Assuming that the model will have a single input/output
        self.onnx_nodes[0].inputs[0] = "MODEL_INPUT " + graph_outputs.identify_node_dim()
        self.onnx_nodes[-1].output[0] = graph_outputs.identify_node_dim(self.onnx_nodes[-1].name) + " MODEL_OUTPUT"

        # Connect model layers and parameters
        for node in self.onnx_nodes:
            node.identify_node_inputs(onnx_nodes_outputs, graph_outputs.identify_node_dim)
            node.identify_node_output(onnx_nodes_inputs, graph_outputs.identify_node_dim)
            node.identify_node_parameters(onnx_initializers)

        # Update graph nodes types to match the extracted names
        # so that netron defaults will give a desired outcome
        for node in self.onnx_nodes:
            node.update_graph_node_name()

        # TODO: make this safer by saving that model in the output folder
        # Make sure the replica model is in the project dir
        self.path = self.path[self.path.rfind('/') + 1:]
        onnx.save(model, self.path)
        return self.path

    def save(self):
        selected_path = utils.choose_folder_dialog('Choose output folder')
        if not selected_path:
            return None
        dir_path = selected_path + "/output"
        utils.delete_folder(dir_path)
        utils.create_folder(dir_path)

        for node in self.onnx_nodes:
            node.save(dir_path)

        return dir_path
