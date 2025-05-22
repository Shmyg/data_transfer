from pathlib import Path
import paramiko
import configparser
import os

def download_file():

    config = configparser.ConfigParser()
    config_path = Path(__file__).parent / 'config.ini'
    config.read(config_path)

    try:
        hostname = config.get("OS","hostname")
    except configparser.NoOptionError:
        print("Hostname not found in config file.")
        return
    
    try:
        username = config.get("OS", "username")
    except configparser.NoOptionError:
        print("Username not found in config file.")
        return
    
    try:
        password = config.get("OS", "password")
    except configparser.NoOptionError:
        print("Password not found in config file.")
        return
    
    try:
        port = config.get("OS", "port")
    except configparser.NoOptionError:
        print("Port not found in config file.")
        return
    
    try:
        local_dir = config.get("OS", "local_dir")
    except configparser.NoOptionError:
        print("Local directory not found in config file.")
        return
    
    # End of config file reading
    # Ensure the local directory exists
    local_dir = Path(local_dir)
    if not local_dir.exists():
        print(f"Local directory {local_dir} does not exist. Creating it.")
        local_dir.mkdir(parents = True, exist_ok = True)

    # Create an SSH client and connect
    try:
        transport = paramiko.Transport((hostname, int(port)))
        transport.connect(username=username, password=password)
    except paramiko.SSHException as e:
        print(f"SSH connection failed: {e}")
        return

    # Start an SFTP session
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Change directory (equivalent to 'cd')
    sftp.chdir('Field')

    for field_dir in sftp.listdir(): 

        sftp.chdir(field_dir)

        for remote_file in sftp.listdir():
            if remote_file.endswith('.csv'):
            # Download the file
                print(f"Downloading {remote_file}...")

                local_file = os.path.join(local_dir, remote_file)
                print(f"Saving to {local_file}...")

                sftp.get(remote_file, str(local_file))
                print(f"Downloaded {remote_file} to {local_file}")

        # Change back to the parent directory
        sftp.chdir('..')

    # Always close connections
    sftp.close()
    transport.close()

if __name__ == "__main__":
    download_file()