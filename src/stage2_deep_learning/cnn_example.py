import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc1 = nn.Linear(32 * 7 * 7, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)

def run_stage2_demo():
    print("\n[Stage 2] Deep Learning CNN Demo")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)

    transform = transforms.ToTensor()
    dataset = datasets.MNIST("./data", train=True, download=True, transform=transform)
    loader = DataLoader(dataset, batch_size=64, shuffle=True)

    model = SimpleCNN().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    model.train()
    for i, (x, y) in enumerate(loader):
        if i > 100:
            break
        x, y = x.to(device), y.to(device)

        optimizer.zero_grad()
        out = model(x)
        loss = loss_fn(out, y)
        loss.backward()
        optimizer.step()

    print("✅ Stage 2 Complete — CNN Treinado com Sucesso.\n")
