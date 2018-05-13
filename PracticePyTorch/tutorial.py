import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x: torch.Tensor = self.pool(F.relu(self.conv1(x)))
        x: torch.Tensor = self.pool(F.relu(self.conv2(x)))
        x: torch.Tensor = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x: torch.Tensor):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s  # 1次元ごとにサイズをs倍
            # (-1, C*out_w*out_h)
        return num_features


import torch.optim as optim

net = Net()

input = torch.randn(1, 1, 32, 32)
target = torch.arange(1, 11)
target = target.view(1, -1)

criterion = nn.MSELoss()

optimizer = optim.SGD(net.parameters(), lr=0.01)

output = net(input)
optimizer.zero_grad()

loss = criterion(output, target)
loss.backward()

optimizer.step()
