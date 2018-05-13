import torch.nn as nn
import torch.nn.functional as F

VERBOSE = True


class Net(nn.Module):
    # x -> conv1 -> relu -> pool ->

    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Poolはbackwardで最大値のみを通す。
        # 順伝播時の値は保持しない

        # IN | torch.Size([4, 3, 32, 32])

        # -> torch.Size([4, 6, 28, 28])
        x = self.conv1(x)

        # -> torch.Size([4, 6, 14, 14])
        x = self.pool(F.relu(x))

        # -> torch.Size([4, 16, 10, 10])
        x = self.conv2(x)

        # -> torch.Size([4, 16, 5, 5])
        x = self.pool(F.relu(x))

        # -> torch.Size([4, 400])
        x = x.view(-1, 16 * 5 * 5)  # (N, Ch*H*W) ChはConv2のFN

        # -> torch.Size([4, 120])
        x = F.relu(self.fc1(x))

        # -> torch.Size([4, 84])
        x = F.relu(self.fc2(x))

        # -> torch.Size([4, 10])
        # label
        x = self.fc3(x)
        return x

if __name__ == '__main__':
    net = Net()
    print(net)

