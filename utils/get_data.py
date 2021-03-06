from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import torch

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"


class BernoulliSyntheticDataset(Dataset):
    """
    Dataset for creating sparse vectors.
    """
    def __init__(self, m, n, s, l):
        self.m = m
        self.n = n
        self.s = s
        self.l = l
        self.reset()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return torch.Tensor(self.data[idx]), torch.Tensor([0.0])

    def reset(self):
        self.data = torch.zeros((self.l, self.n)) + self.s / self.n
        self.data = torch.bernoulli(self.data) * torch.normal(
            torch.zeros((self.l, self.n)), torch.ones((self.l, self.n))
        )


class Synthetic:
    """
    Synthetic dataset with train an test split.
    """
    def __init__(self, m, n, s_train, s_test, batch_size=512, dataset=BernoulliSyntheticDataset):
        self.m = m
        self.n = n
        self.s = s_train
        self.train_data = dataset(m, n, s_train, 50000)
        self.test_data = dataset(m, n, s_test, 10000)

        self.train_loader = torch.utils.data.DataLoader(
            self.train_data, batch_size=batch_size, shuffle=True, drop_last=True,
        )

        self.test_loader = torch.utils.data.DataLoader(
            self.test_data, batch_size=batch_size, shuffle=False, drop_last=True,
        )

    def visualize(self, x):
        plt.imshow(x.numpy().reshape(25, 20))
