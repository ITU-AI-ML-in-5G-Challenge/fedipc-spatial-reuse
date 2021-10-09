import numpy as np
import torch
from torch.optim import SGD
from tqdm import tqdm
from copy import deepcopy

from federated_trainers import get_loss


class FederatedAveragingTrainer:

    def __init__(self, model, **params):
        self.model = model
        self.params = params

    def train(self, train_loader):

        for round_idx in tqdm(range(self.params["num_rounds"])):
            m = max(int(np.round(self.params["participation"]*len(train_loader))), 1)
            chosen_contexts = np.random.choice(list(range(len(train_loader))), m, replace=False)

            original_state_dict = deepcopy(self.model.state_dict())
            state_dicts = {}

            for i, (context_key, context_data_loader) in enumerate(train_loader):
                if i not in chosen_contexts:
                    continue

                self.model.load_state_dict(original_state_dict)
                optimizer = SGD(self.model.parameters(), lr=self.params["lr"])

                self.train_node(self.model, optimizer, context_data_loader)

                state_dicts[context_key] = deepcopy(self.model.state_dict())

            self.aggregate(state_dicts)

    def train_node(self, model, optimizer, context_data_loader):
        model.train()

        total_loss = .0

        for epoch_idx in range(self.params["num_epochs"]):

            epoch_total_loss = .0

            # The data are shuffled in preprocessor so no need to shuffle again.
            for X, y in context_data_loader:
                model.zero_grad()
                optimizer.zero_grad()

                y_pred = model.forward(X)

                cur_loss = get_loss(y_pred, y)

                cur_loss.backward()

                optimizer.step()

                epoch_total_loss += cur_loss.item() * len(X)

            epoch_avg_loss = epoch_total_loss / len(context_data_loader)
            total_loss += epoch_avg_loss
            avg_loss = total_loss / (epoch_idx + 1)

    def aggregate(self, state_dicts):

        new_state_dict = {}

        for key in self.model.state_dict().keys():
            # TODO: implement n_k / n part (not required for now since all n_k / n values are equal)
            new_state_dict[key] = torch.mean(torch.stack([sd[key] for sd in state_dicts.values()], dim=0), dim=0)

        self.model.load_state_dict(new_state_dict)

    def predict(self, data_loader):
        self.model.eval()

        y_pred = {}
        y_true = {}
        for context_idx, context_loader in data_loader:

            for X, y in context_loader:

                preds = self.model.forward(X).detach()

                y_pred[context_idx] = torch.cat([y_pred[context_idx], preds], dim=0) if context_idx in y_pred else preds

                y_true[context_idx] = torch.cat([y_true[context_idx], y], dim=0) if context_idx in y_true else y

        return y_true, y_pred
