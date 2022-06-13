from re import sub
from python_terraform import *
import os
import subprocess


class terraform:

    def __init__(self):    
        self.tf = Terraform()


    def create_vm_instances(self, vm_name, vm_number=0):
        if vm_number>0:
            os.chdir(os.getcwd()+"\\vm_tfs\\")
            print(os.getcwd())
            self.terraform_init()
            self.terraform_plan()
            self.terraform_apply_vm_instance(vm_name)
            
            print("VM DONE")

    def create_k8s_cluster(self,nodes_number=0):
        if nodes_number>0:
            print("cluster")
            os.chdir(os.getcwd()+"\cluster_tfs\\")
            print(os.getcwd())
            self.terraform_init()
            self.terraform_plan() 
            self.terraform_apply_k8s_cluster(nodes_number)
            
        print("K8S DONE")

    def terraform_apply_vm_instance(self, vm_name):
        command = 'terraform apply -var "vm-instance-name={}" -auto-approve'.format(vm_name)
        subprocess.run(command, shell=True)
        print("apply")

    def terraform_apply_k8s_cluster(self, nodes_number):
        command = 'terraform apply -var "gke_node_count={}" -auto-approve'.format(nodes_number)
        subprocess.run(command, shell=True)
        print("apply")

    def terraform_plan(self):
        subprocess.run("terraform plan", shell=True)
        print("plan")

    def terraform_init(self):
        subprocess.run( "terraform init", shell=True)
        print("init")

    def terraform_destroy(self):
        subprocess.run("terraform destroy -auto-approve", shell=True)
        print("destroy")

