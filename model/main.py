import torch as th
from torch import nn
from torch.utils.data import DataLoader
from torch.optim import Adam

from typing import Literal

import polars as pl

import sys


def progres_bar(iteration, total, prefix='', suffix='', decimals=1, bar_length=40):
    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\033[32m\r{prefix}\033[0m |{bar}| {percent}% \033[36m{suffix}\033[0m')
    sys.stdout.flush()
    if iteration == total:
        print()


class FYPModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, function: Literal["reLU", "tanh"] = "reLU"):
        super(FYPModel, self).__init__()
        self.sequence_1 = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU() if function == "reLU" else nn.Tanh(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU() if function == "reLU" else nn.Tanh(),
            nn.Linear(hidden_size, hidden_size),
        )
        self.sequence_2 = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU() if function == "reLU" else nn.Tanh(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU() if function == "reLU" else nn.Tanh(),
            nn.Linear(hidden_size, output_size),
        )
        self.out_fc = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.sequence_1(x)
        x = self.sequence_2(x)
        x = self.out_fc(x)
        return x

    def train(self, lr:int = 0.001, epochs:int = 100, dataloader: DataLoader = None) -> None:
        """
        Metodo para que el modelo se entrene en los modulos nesesarios
        :param lr:
            learning rate
            set in 0.001 para mejor precision
        :param epochs:
            number of epochs
            set in 100 para mejor precision
            pero puede ser alterada para mas
        :param dataloader:
            el data loader tiene que ser preparado con ejemplos
            con la mayor cantidad de caracteristicas posibles
        :return:
            None
        """

        optimizer = Adam(
            params=self.parameters(),
            lr=lr,
            betas=(0.9, 0.999),
        )
        criterion = nn.CrossEntropyLoss()

        for epoch in range(epochs):
            progres_bar(epoch, epochs, prefix="Train", suffix=f"Epoch: {epoch}")
            total_loss = []
            for data, target in dataloader:
                out = self(data)
                loss = criterion(out, target)
                total_loss.append(loss.item())
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            df_loss = pl.DataFrame({
                "loss": total_loss
            })
            print(f"Epoch: {epoch}, Loss: {sum(total_loss)}, Accuracy: {sum(total_loss)/len(total_loss)}")
            print(f"Loss: {df_loss}, Shape: {df_loss.shape}")

