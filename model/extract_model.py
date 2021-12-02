def extract(path, library):
    if library == "TensorFlow":
        from tensorflow.keras.models import load_model
        model = load_model(path)

        for layer in model.layers:
            print(layer.output.name)
            print(layer.input_shape)
            print(layer.output_shape)
            for variable in layer.variables:
                print(variable.numpy().shape)

        print(model.summary())
        return "Model Extracted Successfully."
    else:
        return "Extracting parameters of the model (TO-BE-IMPLEMENTED-LATER)"
