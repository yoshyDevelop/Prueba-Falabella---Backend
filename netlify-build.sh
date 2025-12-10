#!/usr/bin/env bash
set -e

# Install rustup (non-interactive)
curl https://sh.rustup.rs -sSf | sh -s -- -y

# Make cargo and rustc available in this shell
source $HOME/.cargo/env

# (Optional) verify rust is available
rustc --version
cargo --version

# Upgrade pip and install requirements
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Continue with whatever build/publish steps your project needs
# e.g., run tests or build commands
