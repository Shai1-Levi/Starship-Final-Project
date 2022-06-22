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
    os.chdir('c:\\Users\\User\\Documents\\FourthYear\\Starship\\Starship-Final-Project')
    provider = request.form.get('provider')
    service = request.form.get('service')
    images = request.form.get('images').split(",")
    names = request.form.get('names').split(",")
    ports = request.form.get('ports').split(",")
    hermes = request.form.get('hermes')
    print(provider,service,images ,names ,ports ,hermes)

    vm_names = "demo"

    #change provider directiory
    os.chdir(os.getcwd() + f"\\{provider}\\{service}\\")

    if service == "vm":
        vm = 1
        tf.create_vm_instances(vm_name=vm_names, vm_number=vm)
        containers.ssh_to_vm()
        containers.pull_and_run_images(image_name_tag=images, container_valid_names=names)

    if service == 'k8s':
        k8s=2
        tf.create_k8s_cluster(nodes_number=k8s)
        helm.run_helm(names=names, images=images, ports=ports)
    return "done"
        

# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)