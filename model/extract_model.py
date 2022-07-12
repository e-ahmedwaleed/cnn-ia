from gui import utils
from model.onxx_dataflow.graph import Graph


def extract(model_lib, model_path):
    if model_lib:
        model_path = model_lib.to_onnx(model_path)
    dataflow = Graph(model_path)

    # noinspection PyBroadException
    try:
        model_name = dataflow.identify_model_graph()
        output_dir = dataflow.save()
        if output_dir is None:
            raise Exception('Model Extraction Canceled.')

        # Spaces handled properly
        # TODO: if you were to kill it, consider this
        model_path = (output_dir + '/' + model_name).replace(' ', '*')
        proc = utils.run_python_subprocess('./main.py ' + model_path)

        return proc
    except:
        return None
