# import subprocess
# import os

# print(os.getcwd())
# provider = "gcp"
# service = "vm"
# # os.chdir(os.getcwd() + f"\\{provider}\\{service}\\")
# # output = subprocess.getoutput('terraform output -raw public_ip')
# # print(output)

# import subprocess
# import os

# print(os.getcwd)

# # if os.getcwd[-6:-1] != "vm_tfs":
# #     os.chdiros.getcwd+"\\vm_tfs\\"
# print(os.getcwd())
# provider = "gcp"
# service = "vm"
# os.chdir(os.getcwd() + f"\\{provider}\\{service}\\")
# details = subprocess.run("terraform output", 
#                         universal_newlines = True,
#                         stdout = subprocess.PIPE)
# data_list = details.stdout.splitlines()
# print(data_list[1])
# vm_ips = {}
# vm_details = data_list[1].split('" = "')
# vm_name = vm_details[0].split('  "')[1]
# vm_ip = vm_details[1][:-1]
# vm_ips[vm_name] = vm_ip[7:]
# print(vm_ips)


images = "nginx,vault"
print(images.split(","))
