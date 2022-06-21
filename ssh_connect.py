"""Client to handle connections and actions executed against a remote host."""
from paramiko import AutoAddPolicy, RSAKey, SSHClient
from paramiko.auth_handler import AuthenticationException, SSHException
import subprocess


class RemoteClient:
    """Client to interact with a remote host via SSH """
    # def __init__(self, host: str, user: str, ssh_key_filepath: str ):
    def __init__(self, ssh_key_filepath: str ):
        # self.host = host
        # self.user = user
        self.ssh_key_filepath = ssh_key_filepath
        self.client = None

    def connection(self, host, user):
        """Open SSH connection to remote host."""
        try:
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(
                host,
                username=user,
                key_filename=self.ssh_key_filepath,
                timeout=5000,
            )
        except AuthenticationException as e:
            print(
                f"AuthenticationException occurred; did you remember to generate an SSH key? {e}"
            )
        except Exception as e:
            print(f"Unexpected error occurred while connecting to host: {e}")
    
    
    def get_ip(self):
        details = subprocess.run("terraform output", 
                        universal_newlines = True,
                        stdout = subprocess.PIPE)
        data_list = details.stdout.splitlines()
        vm_ips = {}
        vm_details = data_list[1].split('" = "')
        vm_name = vm_details[0].split('  "')[1]
        vm_ip = vm_details[1][:-1]
        vm_ips[vm_name] = vm_ip[7:]
        return vm_ips[vm_name]
    
    def disconnect(self):
        """Close SSH & SCP connection."""
        if self.connection:
            self.client.close()

    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command) #assuming is linux

        print(stdout.read().decode())




