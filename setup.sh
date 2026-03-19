#!/bin/bash

# Ensure script is run with sudo for system packages
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root (sudo ./setup.sh)"
  exit 1
fi

echo "Installing system dependencies..."
apt-get update
# We need python3-venv for uv to create virtual environments, 
# python3-pip just in case, and standard build tools
apt-get install -y python3-venv python3-pip curl libxcb-cursor0

echo "Installing uv package manager..."
# Install uv locally for all users
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "Creating desktop shortcut..."
APP_DIR=$(cd "$(dirname "$0")" && pwd)
cat <<EOF > /usr/share/applications/ubuntu-autoinstall.desktop
[Desktop Entry]
Name=Ubuntu Package Installer
Comment=Auto-installer for Ubuntu packages
Exec=$APP_DIR/run.sh
Icon=$APP_DIR/app_icon.png
Terminal=false
Type=Application
Categories=System;Utility;
EOF
update-desktop-database /usr/share/applications/

echo "=== Setup Complete! ==="
echo "You can now run the application as your normal user using: ./run.sh"
echo "Or start it right from your application menu!"
