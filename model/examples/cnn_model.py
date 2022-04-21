from abc import ABC, abstractmethod


class CNNImplementation(ABC):

    @abstractmethod
    def generate_model(self, path, epochs):
        """ Load and prepare the dataset """
        """ Build/Compile the model """
        """ Train the model """
        """ Save/Convert the model """
        pass
