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

        # Try exporting the model images with increasing timeout
        timeout = 15
        success = False
        # Spaces handled properly
        model_path = (output_dir + '/' + model_name).replace(' ', '*')
        for i in range(4):
            utils.run_command(cmd + ' ./gui/netron_exporter.py ' + model_path + ' ' + str(timeout))
            if os.path.exists(output_dir + "/model.png"):
                success = True
                break
            else:
                timeout *= 2

        # Open output folder in the explorer
        if success:
            utils.open_folder(output_dir + "/model.png")
        else:
            raise Exception('Model Exportation Failed.')

        return "Model Extracted Successfully."
    except Exception as e:
        return str(e)
