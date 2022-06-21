import requests
import os
from flask import Flask, request , jsonify, render_template
import json
from flask_cors import CORS, cross_origin
import tkinter as tk
from containers import Containers
from terraform import terraform
from helm import Helm
import re



app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

containers = Containers()
tf = terraform()
helm = Helm()


def genrate_valid_name(self,image_name):
    regex = "/"
    new_image_name = re.compile(regex).split(image_name)
    return new_image_name[-1]

@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")


def image_container():

    valid_name = genrate_valid_name(img)
    containers.pull_image(img)
    containers.run_container(img, valid_name, 80, 8080)

def genrate_valid_name(images_name):
        new_images_name = []
        for image_name in images_name:
            if "/" in image_name:
                regex = "/"            
                image_name = re.compile(regex).split(image_name)[1]
            regex = ":"  
            vaild_name = re.compile(regex).split(image_name)[0]           
            
            new_images_name.append(vaild_name)
        return new_images_name

def destroy():
    tf.terraform_destroy()


@app.route("/app", methods=['POST'])
# @cross_origin()
# defining a function that will
# get the fields and
# print them on the screen
def submit():  
    # dic = request.form
    provider = request.form.get('provider')
    service = request.form.get('service')
    images = request.form.get('images')
    names = request.form.get('names')
    ports = request.form.get('ports')
    hermes = request.form.get('hermes')
    print(provider,service,images ,names ,ports ,hermes)

    # print("The image Name is : " + img)
    # print("The instance name is : " + vm_names)
    # print("The number of VMs : " + str(vm))
    # print("The k8s cluster : " + str(k8s))

    # img = img[1:-1].split(", ")

    # container_valid_names = genrate_valid_name(img)
    vm = 1
    k8s=0
    vm_names = "demo"

    #change provider directiory
    os.chdir(os.getcwd() + f"\\{provider}\\{service}\\")



    if (vm > 0) and (k8s==0):
        tf.create_vm_instances(vm_name=vm_names, vm_number=vm)
        containers.pull_and_run_images(image_name_tag=images, container_valid_names=names)

    if (vm == 0) and (k8s>0):
        tf.create_k8s_cluster(k8s)
        helm.run_helm(name=names, image_name=images) #, image_tag=version)

    
    # image_var.set("")
    # vm_name_var.set("")
    # vm_var.set(0)
    # k8s_var.set(0)
    return "done"
        

# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)