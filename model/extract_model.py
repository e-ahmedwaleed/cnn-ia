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

        # Spaces handled properly
        model_path = (output_dir + '/' + model_name).replace(' ', '*')
        # TODO: the process is now asynchronous, consider killing if needed later
        utils.run_subprocess('./gui/export/model_exporter.py ' + model_path)

        return "Model Extracted Successfully."
    except Exception as e:
        return str(e)
