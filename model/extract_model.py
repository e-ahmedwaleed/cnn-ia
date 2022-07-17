from gui import utils
from model.onxx_dataflow.graph import Graph


def extract(model_lib, model_path):
    if model_lib:
        try:
            model_path = model_lib.to_onnx(model_path)
        except Exception as e:
            return None, "Model conversion failed: " + str(e)

    dataflow = Graph(model_path)

    try:
        model_name = dataflow.identify_model_graph()
        output_dir = dataflow.save()
        if output_dir is None:
            raise Exception('Model extraction canceled.')

        # Spaces handled properly
        model_path = (output_dir + '/' + model_name).replace(' ', '*')
        proc = utils.run_python_subprocess('./main.py ' + model_path)

        return proc, model_path
    except Exception as e:
        return None, str(e)
