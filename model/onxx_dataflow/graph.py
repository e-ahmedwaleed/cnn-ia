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
        Node.id = 0

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

        # Add node depth in addition to node id (.Maro :pepeEvil:)
        self.normalized_node_id()

    def normalized_node_id(self):
        nodes_depth = {self.onnx_nodes[0].name: 0}
        self.onnx_nodes[0].name = "0_" + self.onnx_nodes[0].name

        for node in self.onnx_nodes[1:]:
            # Identify each node true depth
            max_parent_id = 0
            for parent in node.inputs:
                parent_name = parent[0:parent.find('(') - 1]
                max_parent_id = max(max_parent_id, nodes_depth[parent_name])
            nodes_depth[node.name] = max_parent_id + 1

            # Append depth to names
            node.name = str(nodes_depth[node.name]) + '_' + node.name
            for i, parent in enumerate(node.inputs):
                parent_name = parent[0:parent.find('(') - 1]
                node.inputs[i] = str(nodes_depth[parent_name]) + '_' + parent

    def save(self):
        selected_path = utils.choose_folder_dialog('Choose output folder')
        if not selected_path:
            return None
        dir_path = selected_path + "/output"
        utils.delete_folder(dir_path)
        utils.create_folder(dir_path)

        for node in self.onnx_nodes:
            node.save(dir_path)

        return dir_path + '/' + self.onnx_nodes[0].name + ".node"
