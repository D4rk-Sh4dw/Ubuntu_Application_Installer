import os
import json
import urllib.request

CONFIG_PATH = "config.json"
ICONS_DIR = "icons"

os.makedirs(ICONS_DIR, exist_ok=True)

with open(CONFIG_PATH, "r") as f:
    apps = json.load(f)

# Add PC-Welt tools, Alias Generator and Cronjob Generator
new_apps = [
    {
        "name": "BleachBit",
        "description": "System cleaner and privacy tool",
        "type": "apt",
        "identifier": "bleachbit",
        "icon": "",
        "script": ""
    },
    {
        "name": "Synaptic",
        "description": "Graphical package management program",
        "type": "apt",
        "identifier": "synaptic",
        "icon": "",
        "script": ""
    },
    {
        "name": "GParted",
        "description": "Partition manager for Linux",
        "type": "apt",
        "identifier": "gparted",
        "icon": "",
        "script": ""
    },
    {
        "name": "PowerTOP",
        "description": "Linux system power consumption profiler (Run via: sudo powertop)",
        "type": "apt",
        "identifier": "powertop",
        "icon": "",
        "script": ""
    },
    {
        "name": "Cronjob Generator",
        "description": "Interactive tool to create system crontabs",
        "type": "none",
        "identifier": "",
        "icon": "",
        "script": "scripts/create_cronjob.sh"
    },
    {
        "name": "Bash Alias Generator",
        "description": "Interactive tool to create new terminal aliases",
        "type": "none",
        "identifier": "",
        "icon": "",
        "script": "scripts/create_alias.sh"
    }
]

existing_names = [app["name"] for app in apps]
for new_app in new_apps:
    if new_app["name"] not in existing_names:
        apps.append(new_app)

# Map app names to Papirus icon file names or explicit fallback URLs
icon_map = {
    "OnlyOffice": "onlyoffice-desktopeditors",
    "TeamViewer": "teamviewer",
    "Microsoft Teams": "teams",
    "Remote Desktop Manager": "remmina",
    "Spotify": "spotify-client",
    "Vivaldi Browser": "vivaldi",
    "VS Code": "visual-studio-code",
    "NormCap": "normcap",
    "Upscayl": "upscayl",
    "GIMP": "gimp",
    "VLC": "vlc",
    "Whatsie": "whatsie",
    "Bitwarden": "bitwarden",
    "Darktable": "darktable",
    "BleachBit": "bleachbit",
    "Synaptic": "synaptic",
    "GParted": "gparted",
    "PowerTOP": "powertop",
    "Cronjob Generator": "accessories-text-editor",
    "Bash Alias Generator": "utilities-terminal"
}

base_url = "https://raw.githubusercontent.com/PapirusDevelopmentTeam/papirus-icon-theme/master/Papirus/64x64/apps/{}.svg"

# Some icons might have different names in Papirus
fallback_urls = {
    "Microsoft Teams": "https://raw.githubusercontent.com/PapirusDevelopmentTeam/papirus-icon-theme/master/Papirus/64x64/apps/teams-for-linux.svg",
    "Spotify": "https://raw.githubusercontent.com/PapirusDevelopmentTeam/papirus-icon-theme/master/Papirus/64x64/apps/spotify.svg",
    "VS Code": "https://raw.githubusercontent.com/PapirusDevelopmentTeam/papirus-icon-theme/master/Papirus/64x64/apps/vscode.svg",
    "OnlyOffice": "https://raw.githubusercontent.com/PapirusDevelopmentTeam/papirus-icon-theme/master/Papirus/64x64/apps/onlyoffice-desktopeditors.svg"
}

print("Downloading SVG icons to " + ICONS_DIR + "/...")
for app in apps:
    icon_name = icon_map.get(app["name"])
    if icon_name:
        url = fallback_urls.get(app["name"], base_url.format(icon_name))
        icon_path = os.path.join(ICONS_DIR, f"{icon_name}.svg")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                content = response.read()
                with open(icon_path, 'wb') as icon_out:
                    icon_out.write(content)
            
            app["icon"] = f"./{ICONS_DIR}/{icon_name}.svg"
            print(f" [OK] {app['name']}")
        except Exception as e:
            print(f" [FAIL] {app['name']} ({url}): {e}")

with open(CONFIG_PATH, "w") as f:
    json.dump(apps, f, indent=4)

print("Icons downloaded and config.json updated!")
