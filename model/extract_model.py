import os

from gui import utils
from model.onxx_dataflow.graph import Graph


def extract(model_path):
    dataflow = Graph(model_path)
    # noinspection PyBroadException
    try:
        model_name = dataflow.identify_model_graph()
        output_dir = dataflow.save()
        if output_dir is None:
            raise Exception('Model Extraction Canceled.')

        # Modules might not be detected when using 'python' while having 'venv'
        cmd = "python "
        if os.path.exists("./venv/Scripts/python.exe"):
            cmd = "./venv/Scripts/python.exe "

        # Spaces handled properly
        model_path = (output_dir + '/' + model_name).replace(' ', '*')

        # TODO: timeout will be no longer needed
        timeout = 10
        utils.run_command(cmd + ' ./gui/export/netron_exporter.py ' + model_path + ' ' + str(timeout))

        # Open output folder in the explorer
        if os.path.exists(output_dir + "/model.png"):
            utils.open_folder(output_dir + "/model.png")
        else:
            raise Exception('Model Exportation Canceled.')

        return "Model Extracted Successfully."
    except Exception as e:
        return str(e)
