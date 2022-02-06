import netron

from gui import utils
from model.onxx_dataflow.graph import Graph


def extract(path):
    dataflow = Graph(path)
    # noinspection PyBroadException
    try:
        dataflow.identify_model_graph()
        dir_path = dataflow.save()
        netron.start(path)
        utils.sleep(1.0)
        utils.open_folder(dir_path)
        return "Model Extracted Successfully (close the browser to continue using the program)"
    except:
        return "Model Extraction Failed!"
