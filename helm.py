import subprocess
import os
import re

class Helm:
    def __init__(self):
        self.list_of_sets = []
        self.helm_command = ""
        self.change_fir = False
        

    def run_helm(self,names, images, ports, expose_type="LoadBalancer"):
        for name, image, port in list(zip(names,images,ports)):
            print("name, image", name, image)
            self.helm_command = 'helm install manifst-{} manifst'.format(name)
            sets=' --set name="{}" --set deployment.image="{}" --set deployment.tag="{}" --set service.port="{}" --set service.targetPort="{}" --set service.exposeType="{}"'.format(name,image,"latest", port, port,expose_type)
        
        print(self.helm_command+sets)
        subprocess.run(self.helm_command+sets)
