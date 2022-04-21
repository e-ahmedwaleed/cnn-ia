import torch

from torch import nn, optim
from torchvision import datasets, transforms

from model.examples.cnn_model import CNNImplementation


# noinspection PyTypeChecker
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.cnn_layers = nn.Sequential(
            # Defining a 2D convolution layer
            nn.Conv2d(1, 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            # Defining another 2D convolution layer
            nn.Conv2d(4, 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.linear_layers = nn.Sequential(
            nn.Linear(4 * 7 * 7, 10)
        )

    # Defining the forward pass
    def forward(self, x):
        x = self.cnn_layers(x)
        x = x.view(x.size(0), -1)
        x = self.linear_layers(x)
        return x


class PyTorchImplementation(CNNImplementation):
    def __init__(self):
        self.model = Net()

    def generate_model(self, path, epochs):
        """ Load and prepare the dataset """

        # transformations to be applied on images
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,)), ])

        # defining the training set
        train_set = datasets.MNIST('./data', download=True, train=True, transform=transform)

        # defining train_loader
        train_loader = torch.utils.data.DataLoader(train_set, batch_size=64, shuffle=True)

        """ Build/Compile the model """

        # defining the optimizer
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        # defining the loss function
        criterion = nn.CrossEntropyLoss()
        # checking if GPU is available
        if torch.cuda.is_available():
            self.model = self.model.cuda()
            criterion = criterion.cuda()

        """ Train the model """

        for i in range(epochs):
            running_loss = 0
            for images, labels in train_loader:

                if torch.cuda.is_available():
                    images = images.cuda()
                    labels = labels.cuda()

                # Training pass
                optimizer.zero_grad()

                output = self.model(images)
                loss = criterion(output, labels)

                # This is where the model learns by backpropagation
                loss.backward()

                # And optimizes its weights here
                optimizer.step()

                running_loss += loss.item()
            else:
                print("Epoch {} - Training loss: {}".format(i + 1, running_loss / len(train_loader)))

        """ Save/Convert the model """

        path = path + "/CNN-PyTorch-mnist.onnx"
        # noinspection PyUnboundLocalVariable
        torch.onnx.export(self.model, images[0].view(1, 1, 28, 28), path)
        return path
