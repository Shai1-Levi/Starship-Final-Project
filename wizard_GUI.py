# Program to make a simple
# wizard ui 
 
import tkinter as tk
from containers import Containers
from terraform import terraform

class GUI:
    def __init__(self):

        self.containers = Containers()
        self.tf = terraform()
        
        self.root=tk.Tk()
 
        # setting the windows size
        self.root.geometry("600x400")
  
        # declaring string and int variables
        self.image_var=tk.StringVar()
        self.image_version_var=tk.StringVar()
        self.vm_var=tk.IntVar()
        self.k8s_var=tk.IntVar()

        # creating a label for Docker Image Name using widget Label
        image_label = tk.Label(self.root, text = 'Docker Image Name', font=('calibre',10, 'bold'))
        
        # creating a entry for Docker Image Name using widget Entry
        image_entry = tk.Entry(self.root,textvariable = self.image_var, font=('calibre',10,'normal'))

        # creating a label for Docker Image Version using widget Label
        image_version_label = tk.Label(self.root, text = 'Docker Image Version', font=('calibre',10, 'bold'))
        
        # creating a entry for Docker Image Version using widget Entry
        image_version_entry = tk.Entry(self.root,textvariable = self.image_version_var, font=('calibre',10,'normal'))
        
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
        
        # placing the label and entry in
        # the required position using grid
        # method
        image_label.grid(row=0,column=0)
        image_entry.grid(row=0,column=1)
        image_version_label.grid(row=1,column=0)
        image_version_entry.grid(row=1,column=1)
        vm_label.grid(row=2,column=0)
        vm_entry.grid(row=2,column=1)
        k8s_label.grid(row=3,column=0)
        k8s_entry.grid(row=3,column=1)
        sub_btn.grid(row=4,column=1)

        # performing an infinite loop
        # for the window to display
        self.root.mainloop()
 
  
    # defining a function that will
    # get the fields and
    # print them on the screen
    def submit(self):
    
        img=self.image_var.get()
        version=self.image_version_var.get()
        vm=self.vm_var.get()
        k8s=self.k8s_var.get()
        
        print("The image Name is : " + img)
        print("The image version is : " + version)
        print("The number of VMs : " + str(vm))
        print("The k8s cluster : " + str(k8s))

        # self.containers.run_container(img, version, 80, 8080)
        if (vm > 0) and (k8s==0):
            self.tf.create_vm_instances(vm)
        if (vm == 0) and (k8s>0):
            self.tf.create_k8s_cluster(k8s)
        
        self.image_var.set("")
        self.image_version_var.set("")
        self.vm_var.set(0)
        self.k8s_var.set(0)

gui = GUI()