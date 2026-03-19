import subprocess
import os
import shlex

def run_command_with_callback(cmd, log_callback=None, password=None):
    if log_callback:
        # Hide password in logs if present
        log_cmd = cmd.copy()
        log_callback(f"Running: {' '.join(log_cmd)}")
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE if password else None,
        text=True,
        bufsize=1
    )
    
    if password:
        process.stdin.write(password + '\n')
        process.stdin.flush()
    
    for line in iter(process.stdout.readline, ''):
        if log_callback:
            log_callback(line.rstrip('\n'))
            
    process.stdout.close()
    process.wait()
    
    if log_callback:
        if process.returncode == 0:
            log_callback("Success!")
        else:
            log_callback(f"Failed with return code {process.returncode}")
            
    return process.returncode

def install_apt(package, log_callback=None, password=None):
    cmd = ["sudo", "-S", "apt-get", "install", "-y"] + shlex.split(package)
    return run_command_with_callback(cmd, log_callback, password)

def ensure_snap(log_callback=None, password=None):
    import shutil
    if shutil.which("snap"):
        return True
    if log_callback:
        log_callback("snap not found – trying to install snapd...")
    # Update cache but ignore errors (e.g. broken GPG keys on other repos)
    run_command_with_callback(["sudo", "-S", "apt-get", "update", "--ignore-missing"], log_callback, password)
    if run_command_with_callback(["sudo", "-S", "apt-get", "install", "-y", "snapd"], log_callback, password) != 0:
        if log_callback:
            log_callback("ERROR: Could not install snapd. On Linux Mint, snap is disabled by default. Please install it manually.")
        return False
    return True

def ensure_flatpak(log_callback=None, password=None):
    import shutil
    if shutil.which("flatpak"):
        return True
    if log_callback:
        log_callback("flatpak not found – trying to install flatpak...")
    # Update cache but ignore errors (e.g. broken GPG keys on other repos)
    run_command_with_callback(["sudo", "-S", "apt-get", "update", "--ignore-missing"], log_callback, password)
    if run_command_with_callback(["sudo", "-S", "apt-get", "install", "-y", "flatpak"], log_callback, password) != 0:
        if log_callback:
            log_callback("ERROR: Could not install flatpak. Please install it manually and retry.")
        return False
    # Add flathub remote if missing
    run_command_with_callback(
        ["flatpak", "remote-add", "--if-not-exists", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"],
        log_callback, password
    )
    return True

def install_snap(package, log_callback=None, password=None):
    if not ensure_snap(log_callback, password):
        return 1
    cmd = ["sudo", "-S", "snap", "install"] + shlex.split(package)
    return run_command_with_callback(cmd, log_callback, password)

def install_flatpak(package, log_callback=None, password=None):
    if not ensure_flatpak(log_callback, password):
        return 1
    cmd = ["sudo", "-S", "flatpak", "install", "-y"] + shlex.split(package)
    return run_command_with_callback(cmd, log_callback, password)

def install_deb(path_or_url, log_callback=None, password=None):
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        filename = path_or_url.split("/")[-1]
        dl_path = f"/tmp/{filename}"
        if log_callback:
            log_callback(f"Downloading {path_or_url} to {dl_path}...")
        
        wget_cmd = ["wget", "-O", dl_path, path_or_url]
        if run_command_with_callback(wget_cmd, log_callback) != 0:
            return 1
            
        cmd = ["sudo", "-S", "apt-get", "install", "-y", dl_path]
        return run_command_with_callback(cmd, log_callback, password)
    else:
        cmd = ["sudo", "-S", "apt-get", "install", "-y", path_or_url]
        return run_command_with_callback(cmd, log_callback, password)

def run_post_install_script(script_path, log_callback=None):
    if not script_path or not os.path.exists(script_path):
        return
    if log_callback:
        log_callback(f"Running post-install script in terminal: {script_path}")
        
    terminals = [
        ["x-terminal-emulator", "-e"],
        ["gnome-terminal", "--wait", "--"],
        ["konsole", "-e"],
        ["xfce4-terminal", "-e"],
        ["alacritty", "-e"],
        ["kitty", "--"]
    ]
    
    
    # Ensure the script is executable
    try:
        import stat
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | stat.S_IEXEC)
    except Exception as e:
        if log_callback:
            log_callback(f"Warning: Could not make script executable: {e}")

    script_cmd = f"'{os.path.abspath(script_path)}'; echo 'Press Enter to close...'; read"
    
    for term in terminals:
        import shutil
        if shutil.which(term[0]):
            cmd = term + ["bash", "-c", script_cmd]
            subprocess.run(cmd)
            return
            
    if log_callback:
        log_callback("Error: Could not find a suitable terminal emulator to run the script.")
