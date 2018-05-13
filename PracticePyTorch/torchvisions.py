import torch
import torchvision
import torchvision.transforms as transforms

import matplotlib.pyplot as plt
import numpy as np

# 前処理関数
# 1.Tensorにする
# 2. range[-1, 1]に正規化する
# 次のtrainset読み込みで使う
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)

trainset: torchvision.datasets.cifar.CIFAR10 = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform)

# Data loader. Combines a dataset and a sampler,
# and provides single- or multi-process iterators over the dataset.
# https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader
trainloader: torch.utils.data.dataloader.DataLoader = torch.utils.data.DataLoader(
    trainset, batch_size=4, shuffle=True, num_workers=2)

testset: torchvision.datasets.cifar.CIFAR10 = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform)

testloader: torch.utils.data.dataloader.DataLoader = torch.utils.data.DataLoader(
    testset, batch_size=4, shuffle=True, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


def imshow(img):
    img = img / 2 + 0.5  # range[-1,1] -> [0,1]
    npimg = img.numpy()  # tensor -> numpy
    plt.imshow(np.transpose(npimg, (1, 2, 0)))  # (C, x, y) -> (x, y, C)


# dataloaderが独自のiterを返す
dataiter = iter(trainloader)
images, labels = dataiter.next()

# 　画像法事用のgridつくるよ
imshow(torchvision.utils.make_grid(images))

print(' '.join('%5s' % classes[labels[j]] for j in range(4)))
