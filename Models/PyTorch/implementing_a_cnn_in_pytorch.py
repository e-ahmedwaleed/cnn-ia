import numpy as np
import torch
from torchvision import datasets, transforms
from torch import nn, optim


# defining the model

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


class ImplementingPyTorch(object):
    def __init__(self):
        self.model = Net()

    def generate_model(self):
        """Step 2: Load and prepair the dataset"""
        # transformations to be applied on images
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,)), ])

        # defining the training and testing set
        trainset = datasets.MNIST('./data', download=True, train=True, transform=transform)
        testset = datasets.MNIST('./', download=True, train=False, transform=transform)

        # defining trainloader and testloader
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
        testloader = torch.utils.data.DataLoader(testset, batch_size=64, shuffle=True)

        # shape of training data
        dataiter = iter(trainloader)
        images, labels = dataiter.next()

        # shape of validation data
        dataiter = iter(testloader)
        images, labels = dataiter.next()

        """ Build/Train the model """

        # defining the optimizer
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        # defining the loss function
        criterion = nn.CrossEntropyLoss()
        # checking if GPU is available
        if torch.cuda.is_available():
            self.model = self.model.cuda()
            criterion = criterion.cuda()

        """ train this model for 10 epochs"""

        for i in range(10):
            running_loss = 0
            for images, labels in trainloader:

                if torch.cuda.is_available():
                    images = images.cuda()
                    labels = labels.cuda()

                # Training pass
                optimizer.zero_grad()

                output = self.model(images)
                loss = criterion(output, labels)

                # This is where the model learns by backpropagating
                loss.backward()

                # And optimizes its weights here
                optimizer.step()

                running_loss += loss.item()
            else:
                print("Epoch {} - Training loss: {}".format(i + 1, running_loss / len(trainloader)))

    def save_model(self, path):
        path = path + "\\CNN-PyTorch-mnist"
        torch.save(self.model.state_dict(), path)
        return path
