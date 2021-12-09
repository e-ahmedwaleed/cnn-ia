def extract(path, library):
    if library == "TensorFlow":
        from tensorflow.keras.models import load_model
        model = load_model(path)

        print(model.summary())
    else:
        from torch import load
        model = load(path)
        model.eval()

        print(model)

    return "Model Extracted Successfully."
