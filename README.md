# Ubuntu Application Installer

A modern PyQt6-based GUI application for automating software installation on Ubuntu.

![App Icon](app_icon.png)

## Features

- 📦 **Multi-Package Manager Support**: Install via `apt`, `snap`, `flatpak`, or local/remote `.deb` files
- 🎨 **Modern Dark UI**: Sleek dark-themed GUI with custom icons for each application
- 🔍 **Full-Text Search**: Instantly filter applications by name, description, or type
- ☑️ **Select All**: Toggle all (or filtered) applications at once
- ✏️ **Edit & Delete**: Modify or remove any entry directly from the GUI
- 📜 **Pre-Install Scripts**: Run scripts before installation (e.g., add repositories to `sources.list.d`)
- 📜 **Post-Install Scripts**: Run interactive bash scripts after installation (e.g., create aliases, set up cronjobs)
- 💬 **Real-Time Logs**: Stream installation output directly into the app
- ➕ **Add Applications**: Extend the list at runtime through the GUI
- 🔑 **Privilege Escalation**: Uses `pkexec` for secure, graphical root prompts

## Quickstart

### 1. Setup Dependencies

```bash
sudo ./setup.sh
```

This installs `python3-venv`, `curl`, and the `uv` package manager.

### 2. Download Icons

```bash
python3 download_icons.py
```

This pulls SVG icons from the Papirus icon theme for all pre-configured applications.

### 3. Run the App

```bash
./run.sh
```

## Project Structure

```
.
├── app_icon.png                # Application icon
├── config.json                 # List of applications (persistent)
├── download_icons.py           # Icon downloader script
├── icons/                      # Downloaded app icons (SVG)
├── run.sh                      # Launcher script (uses uv)
├── setup.sh                    # System dependency installer
├── scripts/                    # Pre/post-install bash scripts
│   ├── create_alias.sh
│   ├── create_cronjob.sh
│   └── ...
└── src/
    ├── data.py                 # Config load/save
    ├── dialogs.py              # Add/Edit application dialog
    ├── installer.py            # Package manager logic
    └── main.py                 # Main window & UI
```

## Pre-configured Applications

The following apps are included out of the box:

| Name | Type |
|------|------|
| OnlyOffice | snap |
| VS Code | snap |
| TeamViewer | deb |
| Vivaldi Browser | deb |
| Spotify | snap |
| GIMP | apt |
| VLC | apt |
| Bitwarden | snap |
| Darktable | flatpak |
| NormCap | flatpak |
| Upscayl | flatpak |
| BleachBit | apt |
| GParted | apt |
| Synaptic | apt |
| PowerTOP | apt |
| Whatsie | snap |
| Microsoft Teams | snap |
| Bash Alias Generator | script |
| Cronjob Generator | script |
| plocate | apt |
| Mission Center | apt |

## Requirements

- Ubuntu (tested on Ubuntu 24.04+)
- Python 3.12+
- `uv` (installed via `setup.sh`)
