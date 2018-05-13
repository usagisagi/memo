import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import convnet
import torchvisions


def main():
    net = convnet.Net()
    criterion = nn.CrossEntropyLoss()
    # optimizerにはnetのparamのポインタを渡す
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    for epoch in range(2):
        running_loss = 0.0

        # enemurate start 0
        for i, data in enumerate(torchvisions.trainloader, 0):
            inputs, labels = data

            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()  # update

            # このrunning_lossはLossの表示のみに用い、他に何も使わない
            running_loss += loss.item()

            if i % 2000 == 1999:
                print(f"[{epoch+1}, {i+1}] loss; {running_loss / 2000}")
                running_loss = 0.0

    print("finished training")

    import pickle

    with open("net.pkl", "wb") as f:
        pickle.dump(net, f)


if __name__ == '__main__':
    main()
