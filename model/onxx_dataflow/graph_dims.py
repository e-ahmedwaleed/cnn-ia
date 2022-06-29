import onnx
import numpy as np
import onnxruntime as ort


class GraphDims:
    def __init__(self, path, nodes_output):
        self.dims = {}
        ort_outputs = self.__onnx_layer_output(path)

        for n_o in nodes_output:
            self.dims[n_o] = ort_outputs[nodes_output[n_o][0]].shape

    def identify_node_dim(self, node_name=''):
        return str(self.dims[node_name]).replace('[', '(').replace(']', ')')

    def __onnx_layer_output(self, path):
        ort_session = ort.InferenceSession(path)
        org_outputs = [x.name for x in ort_session.get_outputs()]
        model = onnx.load(path)
        for node in model.graph.node:
            for output in node.output:
                if output not in org_outputs:
                    model.graph.output.extend([onnx.ValueInfoProto(name=output)])
        ort_session = ort.InferenceSession(model.SerializeToString())
        outputs = [x.name for x in ort_session.get_outputs()]
        ort_inputs = {ort_session.get_inputs()[0].name: self.__generate_random_input(model)}
        ort_outs = ort_session.run(outputs, ort_inputs)
        return dict(zip(outputs, ort_outs))

    def __generate_random_input(self, model):
        # TODO: dynamic type! (not static float32)
        self.dims[''] = self.identify_tensor_dim(model.graph.input)
        return np.random.rand(*self.dims['']).astype(np.float32)

    @staticmethod
    def identify_tensor_dim(var):
        dims = [[d.dim_value for d in _var.type.tensor_type.shape.dim] for _var in var][0]
        for i, dim in enumerate(dims):
            if not dim:
                dims[i] = 1
        return dims
