# Program to make a simple
# wizard ui 
 
import tkinter as tk
from containers import Containers
from terraform import terraform
from helm import Helm
import re

class GUI:
    def __init__(self):

        self.containers = Containers()
        self.tf = terraform()
        self.helm = Helm()
        
        self.root=tk.Tk()
 
        # setting the windows size
        self.root.geometry("600x400")
  
        # declaring string and int variables
        self.image_var=tk.StringVar()
        self.vm_name_var=tk.StringVar()
        self.vm_var=tk.IntVar()
        self.k8s_var=tk.IntVar()

        # creating a label for Docker Image Name using widget Label
        image_label = tk.Label(self.root, text = 'Docker Image Name', font=('calibre',10, 'bold'))
        
        # creating a entry for Docker Image Name using widget Entry Docker Image Version
        image_entry = tk.Entry(self.root, textvariable = self.image_var, font=('calibre',10,'normal'))
        self.image_var.set("[nginx:latest, dperson/samba:latest]")

        # creating a label for Docker Image Version using widget Label
        vm_name = tk.Label(self.root, text = 'VM Instance Name', font=('calibre',10, 'bold'))
        
        # creating a entry for Docker Image Version using widget Entry
        vm_name_entry = tk.Entry(self.root,textvariable = self.vm_name_var, font=('calibre',10,'normal'))
        self.vm_name_var.set("Instance Name")
        
        # creating a label for vm instances
        vm_label = tk.Label(self.root, text = 'Number of VMs', font = ('calibre',10,'bold'))
        
        # creating a entry for vm instances
        vm_entry=tk.Entry(self.root, textvariable = self.vm_var, font = ('calibre',10,'normal'))

        # creating a label for k8s
        k8s_label = tk.Label(self.root, text = 'k8s cluster', font = ('calibre',10,'bold'))
        
        # creating a entry for k8s
        k8s_entry=tk.Entry(self.root, textvariable = self.k8s_var, font = ('calibre',10,'normal'))
        
        # creating a button using the widget
        # Button that will call the submit function
        sub_btn=tk.Button(self.root,text = 'Create', command = self.submit)
        sub_btn2=tk.Button(self.root,text = 'Destroy', command = self.destroy)
        

        
        # placing the label and entry in
        # the required position using grid
        # method
        image_label.grid(row=0,column=0)
        image_entry.grid(row=0,column=1)
        vm_name.grid(row=1,column=0)
        vm_name_entry.grid(row=1,column=1)
        vm_label.grid(row=2,column=0)
        vm_entry.grid(row=2,column=1)
        k8s_label.grid(row=3,column=0)
        k8s_entry.grid(row=3,column=1)
        sub_btn.grid(row=5,column=1)
        sub_btn2.grid(row=7,column=1)

        # performing an infinite loop
        # for the window to display
        self.root.mainloop()
    

    def genrate_valid_name(self,images_name):
        new_images_name = []
        for image_name in images_name:
            if "/" in image_name:
                regex = "/"            
                image_name = re.compile(regex).split(image_name)[1]
            regex = ":"  
            vaild_name = re.compile(regex).split(image_name)[0]           
            
            new_images_name.append(vaild_name)
        return new_images_name

    def destroy(self):
        self.tf.terraform_destroy()

  
    # defining a function that will
    # get the fields and
    # print them on the screen
    def submit(self):
    
        img=self.image_var.get()
        vm_names=self.vm_name_var.get()
        vm=self.vm_var.get()
        k8s=self.k8s_var.get()
        
        print("The image Name is : " + img)
        print("The instance name is : " + vm_names)
        print("The number of VMs : " + str(vm))
        print("The k8s cluster : " + str(k8s))

        img = img[1:-1].split(", ")

        container_valid_names = self.genrate_valid_name(img)

        if (vm > 0) and (k8s==0):
            self.tf.create_vm_instances(vm_name=vm_names, vm_number=vm)
            self.containers.pull_and_run_images(image_name_tag=img, container_valid_names=container_valid_names)

        if (vm == 0) and (k8s>0):
            self.tf.create_k8s_cluster(k8s)
            self.helm.run_helm(name=container_valid_names, image_name=img) #, image_tag=version)

        
        self.image_var.set("")
        self.vm_name_var.set("")
        self.vm_var.set(0)
        self.k8s_var.set(0)

gui = GUI()