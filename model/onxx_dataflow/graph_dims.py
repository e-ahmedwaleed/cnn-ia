import onnx
import numpy as np
import onnxruntime as ort


class GraphDims:
    def __init__(self, path, nodes_output):
        self.dims = {}
        ort_outputs = self.__onnx_layer_output(path)

        # Attach each node with its output size
        for n_o in nodes_output:
            self.dims[n_o] = ort_outputs[nodes_output[n_o][0]].shape

    def identify_node_dim(self, node_name=''):
        return str(self.dims[node_name]).replace('[', '(').replace(']', ')')

    def __onnx_layer_output(self, path):
        # Add output branch to every layer that doesn't have one already
        ort_session = ort.InferenceSession(path)
        org_outputs = [x.name for x in ort_session.get_outputs()]
        model = onnx.load(path)
        for node in model.graph.node:
            for output in node.output:
                if output not in org_outputs:
                    model.graph.output.extend([onnx.ValueInfoProto(name=output)])

        # Run the model with dummy input to measure the output
        ort_session = ort.InferenceSession(model.SerializeToString())
        outputs = [x.name for x in ort_session.get_outputs()]
        ort_inputs = {ort_session.get_inputs()[0].name: self.__generate_random_input(model)}
        ort_outs = ort_session.run(outputs, ort_inputs)

        # Attach each output branch identifier with its value
        return dict(zip(outputs, ort_outs))

    def __generate_random_input(self, model):
        # The first element in dims is: input
        self.dims[''] = tuple(self.identify_tensor_dim(model.graph.input))
        from onnx.mapping import TENSOR_TYPE_TO_NP_TYPE
        # TODO: support multi-input models and consider the consequences [identifying dims for input(s)]
        data_type = TENSOR_TYPE_TO_NP_TYPE[model.graph.input[0].type.tensor_type.elem_type]
        return np.random.rand(*self.dims['']).astype(data_type)

    @staticmethod
    def identify_tensor_dim(var):
        dims = [[d.dim_value for d in _var.type.tensor_type.shape.dim] for _var in var][0]
        for i, dim in enumerate(dims):
            if not dim:
                dims[i] = 1
        return dims
