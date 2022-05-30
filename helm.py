import subprocess
import os
import re

class Helm:
    def __init__(self):
        self.list_of_sets = []
        self.helm_command = ""
        self.change_fir = False
        

    def run_helm(self,name, image_name, image_tag, port=80, target_port=80, expose_type="LoadBalancer"):
        if not self.change_fir:
            os.chdir(os.getcwd()+"\cluster_tfs\\")
            print(os.getcwd())
            self.change_fir = True
        self.helm_command = 'helm install manifst-{} manifst'.format(name)
        sets=' --set name="{}" --set deployment.image="{}" --set deployment.tag="{}" --set service.exposeType="{}"'.format(name,image_name,image_tag,expose_type)
       
        print(self.helm_command+sets)
        subprocess.run(self.helm_command+sets)
