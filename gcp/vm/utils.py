import subprocess
import os

print(os.getcwd())
provider = "gcp"
service = "vm"
os.chdir(os.getcwd() + f"\\{provider}\\{service}\\")
output = subprocess.getoutput('terraform output -raw public_ip')
print(output)