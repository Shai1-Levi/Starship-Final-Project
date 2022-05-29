from python_terraform import *
import os
import subprocess


class terraform:

    def __init__(self):    
        self.tf = Terraform()

    def create_vm_instances(self,vm_number=0):
        if vm_number>0:
            print("VM")
            # self.tf.apply('./vm_tfs', no_color=IsFlagged, refresh=False, var={'a':'b', 'c':'d'})

    def create_k8s_cluster(self,nodes_number=0):
        if nodes_number>0:
            print("cluster")
            os.chdir(os.getcwd()+"\cluster_tfs\\")
            print(os.getcwd())
            self.terraform_init()
            self.terraform_plan() 
            self.terraform_apply()

    def terraform_apply(self):
        subprocess.run("terraform apply -auto-approve", shell=True)
        print("apply")

    def terraform_plan(self):
        subprocess.run("terraform plan", shell=True)
        print("plan")

    def terraform_init(self):
        subprocess.run( "terraform init", shell=True)
        print("init")


       