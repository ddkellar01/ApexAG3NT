#!/bin/bash
# Prepares an Android Termux environment for local execution and AI orchestration

set -e

echo "[*] Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing Python, Rust, and networking tools..."
pkg install -y python rust git clang libffi openssl make root-repo

echo "[*] Configuring Python virtual environment..."
python -m venv ~/apex-env
source ~/apex-env/bin/activate

echo "[*] Installing dependencies..."
pip install --upgrade pip wheel
pip install aiohttp networkx web3 pydantic astor

echo "[*] Note: Kali NetHunter Rootless or PRoot is recommended for eBPF kernel features."
echo "[*] Termux environment configured successfully. To start, run: source ~/apex-env/bin/activate"
