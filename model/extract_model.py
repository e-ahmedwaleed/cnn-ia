from gui import utils
from model.onxx_dataflow.graph import Graph


def extract(path):
    dataflow = Graph(path)
    # noinspection PyBroadException
    try:
        dataflow.identify_model_graph()
        dir_path = dataflow.save()
        dataflow.visualize()
        utils.sleep(1)
        utils.open_folder(dir_path)
        return "Model Extracted Successfully."
    except:
        return "Model Extraction Failed!"
