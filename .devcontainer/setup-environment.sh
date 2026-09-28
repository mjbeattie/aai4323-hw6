#!/usr/bin/env bash

set -e

echo "Creating or updating the AAI4323_HW5 Conda environment..."

conda env update \
    --name aai4323_hw5 \
    --file aai4323_conda_hw5.yml \
    --prune

echo "Checking the environment..."

conda run --name aai4323_hw5 python --version
conda run --name aai4323_hw5 python -m pip check

echo "Registering the Jupyter kernel..."

conda run --name aai4323_hw5 python -m ipykernel install \
    --user \
    --name aai4323_hw5 \
    --display-name "Python (AAI4323_HW5)"

echo "AAI4323_HW5 environment setup completed successfully."

echo "Configuring Conda for new terminals..."

conda init bash

grep -qxF "conda activate aai4323_hw5" ~/.bashrc || \
    echo "conda activate aai4323_hw5" >> ~/.bashrc

echo "New terminals will automatically activate the aai4323_hw5 environment."