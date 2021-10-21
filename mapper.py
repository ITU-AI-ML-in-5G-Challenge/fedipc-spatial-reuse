from preprocessors.all_features_preprocessor import AllFeaturesPreprocessor
from preprocessors.padded_features_preprocessor import PaddedFeaturesPreprocessor


class Mapper:

    @staticmethod
    def get_federated_trainer(federated_trainer):
        from federated_trainers.fed_avg_trainer import FedAvgTrainer
        from federated_trainers.fed_prox_trainer import FedProxTrainer
        from federated_trainers.centralized_trainer import CentralizedTrainer

        return {
            "fedavg": FedAvgTrainer,
            "fedprox": FedProxTrainer,
            "centralized": CentralizedTrainer
        }[federated_trainer]

    @staticmethod
    def get_loss(loss):
        from torch import nn

        return {
            "mse": nn.MSELoss,
            "l1": nn.L1Loss,
            "smooth_l1": nn.SmoothL1Loss
        }[loss]

    @staticmethod
    def get_nn_model(nn_model):
        from nn_models.mlp import MLP
        from nn_models.separate_recurrents import SeparateRecurrentsModel

        return {
            "mlp": MLP,
            "separate_recurrents": SeparateRecurrentsModel,
        }[nn_model]

    @staticmethod
    def get_preprocessor(preprocessor):
        from preprocessors.mean_features_preprocessor import MeanFeaturesPreprocessor
        from preprocessors.sequential_features_preprocessor import SequentialFeaturesPreprocessor
        from preprocessors.input_features_preprocessor import InputFeaturesPreprocessor
        from preprocessors.statistical_features_preprocessor import StatisticalFeaturesPreprocessor

        return {
            "mean_features": MeanFeaturesPreprocessor,
            "padded_features": PaddedFeaturesPreprocessor,
            "sequential_features": SequentialFeaturesPreprocessor,
            "input_features": InputFeaturesPreprocessor,
            "all_features": AllFeaturesPreprocessor,
            "statistical_features": StatisticalFeaturesPreprocessor,
        }[preprocessor]

    @staticmethod
    def get_data_loaders(scenario):
        from dataset import SRDataset, DataDownloader
        from torch.utils.data import DataLoader

        data_downloader = DataDownloader(scenario)

        train_data = SRDataset(data_downloader, split="train")
        val_data = SRDataset(data_downloader, split="val")
        test_data = SRDataset(data_downloader, split="test")

        train_loader = DataLoader(train_data)
        val_loader = DataLoader(val_data)
        test_loader = DataLoader(test_data)

        return train_loader, val_loader, test_loader

    @staticmethod
    def get_scaler(input_normalizer):
        from preprocessors.scalers.standard_scaler import StandardScaler
        from preprocessors.scalers.dummy_scaler import DummyScaler
        from preprocessors.scalers.minmax_scaler import MinMaxScaler
        from preprocessors.scalers.knownmax_scaler import KnownMaxScaler

        return {
            "none": DummyScaler,
            "standard": StandardScaler,
            "minmax": MinMaxScaler,
            "knownmax": KnownMaxScaler,
        }[input_normalizer]
