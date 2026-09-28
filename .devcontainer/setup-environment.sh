#!/usr/bin/env bash

set -x
set -e

echo "Creating or updating the AAI4323_HW6 Conda environment..."

conda env update \
    --name aai4323_hw6 \
    --file aai4323_conda_hw6.yml \
    --prune

echo "Checking the environment..."

conda run --name aai4323_hw6 python --version
conda run --name aai4323_hw6 python -m pip check

echo "Registering the Jupyter kernel..."

conda run --name aai4323_hw6 python -m ipykernel install \
    --user \
    --name aai4323_hw6 \
    --display-name "Python (AAI4323_HW6)"

echo "AAI4323_HW6 environment setup completed successfully."

echo "Configuring Conda for new terminals..."

conda init bash

grep -qxF "conda activate aai4323_hw6" ~/.bashrc || \
    echo "conda activate aai4323_hw6" >> ~/.bashrc

echo "New terminals will automatically activate the aai4323_hw6 environment."
