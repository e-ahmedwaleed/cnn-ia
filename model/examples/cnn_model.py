from abc import ABC, abstractmethod


class CNNImplementation(ABC):

    @abstractmethod
    def generate_model(self, path, epochs):
        pass
