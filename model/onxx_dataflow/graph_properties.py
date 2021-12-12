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
    def __init__(self, node_data):
        self.inputs = list(node_data.input)
        self.outputs = list(node_data.output)
        self.attributes = []
        for i, attribute_data in enumerate(node_data.attribute):
            self.attributes.append(Attribute(attribute_data))
        self.parameters = []
        super().__init__(node_data.name, node_data.op_type)

    def identify_node_inputs(self, outputs):
        for i, node in enumerate(self.inputs):
            unmatched = True
            for j in outputs:
                for k in outputs[j]:
                    if node == k:
                        unmatched = False
                        self.inputs[i] = j
            if unmatched & ("MODEL_INPUT" not in node):
                self.parameters.append(node)
        for parameter in self.parameters:
            self.inputs.remove(parameter)

    def identify_node_parameters(self, initializers):
        for i, node in enumerate(self.parameters):
            unmatched = True
            for j in initializers:
                if node == j:
                    unmatched = False
                    self.parameters[i] = initializers[j]
            if unmatched:
                print("Unmatched parameter!?")
        pass

    def identify_node_outputs(self, inputs):
        for i, node in enumerate(self.outputs):
            unmatched = True
            for j in inputs:
                for k in inputs[j]:
                    if node == k:
                        unmatched = False
                        self.outputs[i] = j
            if unmatched & ("MODEL_OUTPUT" not in node):
                print("Unmatched output!?")

    def save(self, path):
        summary = super().__str__() + ":\n"

        if len(self.attributes):
            summary += '\t' + "Attributes:" + '\n'
            for attribute in self.attributes:
                summary += "\t\t" + str(attribute) + '\n'

        if len(self.inputs):
            summary += '\t' + "Inputs:" + '\n'
            for node in self.inputs:
                summary += "\t\t" + str(node) + (".node" if "(" not in str(node) else "") + '\n'

        if len(self.parameters):
            summary += '\t' + "Parameters:" + '\n'
            for i, parameter in enumerate(self.parameters):
                param_file = self.save_parameter(path, self.name + "_" + str(i), parameter)
                summary += "\t\t" + param_file + ".param '" + str(parameter.dtype) + "': " + str(parameter.shape) + '\n'

        if len(self.outputs):
            summary += '\t' + "Outputs:" + '\n'
            for node in self.outputs:
                summary += "\t\t" + str(node) + (".node" if "(" not in str(node) else "") + '\n'

        utils.create_file(path + '/' + self.name + ".node", summary)

    @staticmethod
    def save_parameter(path, file_name, parameter):
        import numpy as np
        np.set_printoptions(threshold=np.inf)
        utils.create_file(path + '/' + file_name + ".param", str(parameter))
        return file_name
