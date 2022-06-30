import os

from gui import utils
from model.onxx_dataflow.graph import Graph


def extract(model_path):
    dataflow = Graph(model_path)
    # noinspection PyBroadException
    try:
        model_path = dataflow.identify_model_graph()
        output_path = dataflow.save()
        if output_path is None:
            raise Exception('Model Extraction Canceled.')

        # Modules might not be detected when using 'python' while having 'venv'
        cmd = "python "
        if os.path.exists("./venv/Scripts/python.exe"):
            cmd = "./venv/Scripts/python.exe "
        utils.run_command(cmd + " ./gui/netron_exporter.py " + model_path + ' ' + output_path)

        utils.open_folder(output_path + "/model.png")
        return "Model Extracted Successfully."
    except Exception as e:
        return str(e)
