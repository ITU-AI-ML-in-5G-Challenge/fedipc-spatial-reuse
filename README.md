# fedipc-spatial-reuse
FedIPC Spatial Reuse Project for ITU AI/ML Challenge 2021.


## Setup
* Download `output_11ax_sr_simulations.txt` from [this link](https://zenodo.org/record/5352060#.YT-3aZ4zbOR) and place this file into the `./data/` folder.
* Download `simulator_input_files.zip` from [this link](https://zenodo.org/record/5352060#.YT-3aZ4zbOR) and place `simulator_input_files` directory into the `./data/` folder.
* `pip install requirements.txt`

## Running
* `python main.py`
* or you may use arguments via `python main.py --preprocessor all_features` 

## Command Line  Interface Arguments
* `--preprocessor` (default: `basic_features`)
    * `basic_features`
* `--nn_model` (default: `mlp`)
    * `mlp`
* `--fed_model` (default: `fed_avg`)
    * `fed_avg`
* `--metrics` (can include multiple metrics, default: `mse r2`)
    * `mse`
    * `r2`

## Extending

### Adding New Neural Network Model
1. Create a model extending `torch.nn.Module` in `./nn_models` directory.
2. Import the new model class and add an entry of <`$model_name`, `$model_class`> to the `modelname_2_modelcls` dictionary in `./nn_models/__init__.py` file.
3. Use the model with `--nn_model $model_name` cli argument.

### Adding New Federated Learning Architecture
1. Create a trainer class extending `federated_trainers.abstract_base_federated_trainer.AbstractBaseFederatedTrainer` in `./federated_trainers` directory.
2. Import the new federated learning trainer class and add an entry of <`$trainer_name`, `$trainer_class`> to the `modelname_2_modelcls` dictionary in `./federated_trainers/__init__.py` file.
3. Use the FL architecture with `--fed_model $trainer_name` cli argument.
