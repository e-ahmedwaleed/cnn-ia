from model.onxx_dataflow.graph import Graph


def extract(path):
    Graph(path).identify_model_graph()
    return "Model Extracted Successfully."
