import torch
from preprocessors.abstract_base_preprocessor import AbstractBasePreprocessor


class MeanFeaturesPreprocessor(AbstractBasePreprocessor):

    def fit(self, train_loader):

        return self

    def transform(self, loader):

        all_context_indices, all_features, all_labels = [], [], []

        for context_idx, features, labels in loader:
            features, labels = self._process_node(features, labels)

            all_context_indices.append(context_idx)
            all_features.append(features)
            all_labels.append(labels)

        return all_context_indices, all_features, all_labels

    def _process_node(self, node_data, node_labels):

        feature_names = ["threshold", "interference", "rssi", "sinr"]

        num_data = len(node_data.keys())
        num_features = len(feature_names)

        features = torch.empty((num_data, num_features), dtype=torch.float32)
        labels = torch.zeros((num_data, self.output_size), dtype=torch.float32)

        for idx, (threshold, threshold_data) in enumerate(node_data.items()):

            threshold_data["threshold"] = [int(threshold_data["threshold"][0])]

            for fi, fname in enumerate(feature_names):
                feats = torch.FloatTensor(threshold_data[feature_names[fi]])
                feats = self.scale(fname, feats)
                features[idx, fi] = torch.mean(feats)

            labels[idx, :len(node_labels[threshold])] = torch.FloatTensor(node_labels[threshold])

        return features, labels
