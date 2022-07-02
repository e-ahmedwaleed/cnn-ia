import re

from gui import utils
from onnx.helper import get_attribute_value

AttributeType = {
    0: "UNDEFINED",
    1: "FLOAT",
    2: "INT",
    3: "STRING",
    4: "TENSOR",
    5: "GRAPH",
    11: "SPARSE_TENSOR",
    13: "TYPE_PROTO",

    6: "FLOATS",
    7: "INTS",
    8: "STRINGS",
    9: "TENSORS",
    10: "GRAPHS",
    12: "SPARSE_TENSORS",
    14: "TYPE_PROTOS"
}


class Property:
    def __init__(self, name, property_type):
        self.name = self.valid_property_name(name)
        self.type = property_type

    def __str__(self):
        return str(self.name) + " '" + str(self.type) + "'"

    @staticmethod
    # A file name can't contain any of the following characters: \/:*?"<>|
    def valid_property_name(name):
        return re.sub('[\\\\/:*?\\"<>|]', '_', str(name))


class Attribute(Property):
    def __init__(self, onnx_attribute):
        self.value = get_attribute_value(onnx_attribute)
        super().__init__(onnx_attribute.name, AttributeType[onnx_attribute.type])

    def __str__(self):
        return super().__str__() + ": " + str(self.value)


class Node(Property):
    type_id = {}

    def __init__(self, graph_node):
        # A layer knows about all of its inputs and the size of its output
        self.inputs = list(graph_node.input)
        self.output = list(graph_node.output)

        # It also knows the details about its attributes and parameters
        self.attributes = []
        for i, attribute_data in enumerate(graph_node.attribute):
            self.attributes.append(Attribute(attribute_data))
        self.parameters = []

        # An ID is added to each layer to have a unique name
        if graph_node.op_type not in Node.type_id:
            Node.type_id[graph_node.op_type] = 0
        node_name = str(Node.type_id[graph_node.op_type]) + '_' + graph_node.op_type
        Node.type_id[graph_node.op_type] += 1

        # Keep track of original node to update name later
        self.graph_node = graph_node
        super().__init__(node_name, graph_node.op_type)

    def identify_node_inputs(self, outputs, dim):
        for i, node in enumerate(self.inputs):
            unmatched = True
            # Look for the layer inputs in others output to find parent layers
            for j in outputs:
                for k in outputs[j]:
                    if node == k:
                        unmatched = False
                        # Append the parent layer along with its output size
                        self.inputs[i] = j + ' ' + dim(j)
            # If the input not found as layer output, then it is a parameter
            if unmatched & ("MODEL_INPUT" not in node):
                self.parameters.append(node)
        # Delete parameters from input list, since they have a special one
        for parameter in self.parameters:
            self.inputs.remove(parameter)

    def identify_node_parameters(self, initializers):
        for i, node in enumerate(self.parameters):
            unmatched = True
            # Look for the layer inputs that was marked as parameters in the graph initializers (parameters)
            for j in initializers:
                if node == j:
                    unmatched = False
                    self.parameters[i] = initializers[j]
            # Well ideally this should never happen
            if unmatched:
                raise Exception("Unmatched parameter: " + str(node) + " @ " + self.name)

    def identify_node_output(self, inputs, dim):
        for i, node in enumerate(self.output):
            unmatched = True
            # Look for the layer output in others input to find the actual output dim
            # it will match only once, it is assumed that a layer can't produce multiple
            # usable outputs (other outputs if existed won't be used as input for others)
            for j in inputs:
                for k in inputs[j]:
                    if node == k:
                        unmatched = False
                        self.output[i] = dim(self.name)
            # Remove other unused outputs (as in 'Dropout' layers)
            if unmatched & ("MODEL_OUTPUT" not in node):
                self.output.remove(node)

    def update_graph_node_name(self):
        self.graph_node.op_type = self.name

    def save(self, path):
        summary = super().__str__() + ":\n"

        summary += self.field_to_string(self.attributes, "Attributes:")
        summary += self.field_to_string(self.inputs, "Inputs:")

        if len(self.parameters):
            summary += '\t' + "Parameters:" + '\n'
            for i, parameter in enumerate(self.parameters):
                param_name = self.name + "_" + str(i)
                summary += "\t\t" + param_name + " '" + str(parameter.dtype) + "': " + str(parameter.shape) + '\n'

        summary += self.field_to_string(self.output, "Output:")
        utils.create_file(path + '/' + self.name + ".node", summary)

    @staticmethod
    def field_to_string(field, title):
        s = ''
        if len(field):
            s += '\t' + title + '\n'
            for element in field:
                s += "\t\t" + str(element) + '\n'
        return s
