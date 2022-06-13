"""Client to handle connections and actions executed against a remote host."""
from paramiko import AutoAddPolicy, RSAKey, SSHClient
from paramiko.auth_handler import AuthenticationException, SSHException



class RemoteClient:
    """Client to interact with a remote host via SSH """
    def __init__(self, host: str, user: str, ssh_key_filepath: str ):
        self.host = host
        self.user = user
        self.ssh_key_filepath = ssh_key_filepath
        self.client = None

    def connection(self):
        """Open SSH connection to remote host."""
        try:
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(
                self.host,
                username=self.user,
                key_filename=self.ssh_key_filepath,
                timeout=5000,
            )
        except AuthenticationException as e:
            print(
                f"AuthenticationException occurred; did you remember to generate an SSH key? {e}"
            )
        except Exception as e:
            print(f"Unexpected error occurred while connecting to host: {e}")
    
    def disconnect(self):
        """Close SSH & SCP connection."""
        if self.connection:
            self.client.close()

    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command) #assuming is linux

        print(stdout.read().decode())




