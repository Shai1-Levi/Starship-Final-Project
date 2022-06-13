import requests
import os
from flask import Flask, request , jsonify
import json
import pymongo
import hvac
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
@cross_origin()
def hello():
    return str({"hello":"world"}),200


def image_container():

    valid_name = genrate_valid_name(img)
    containers.pull_image(img)
    containers.run_container(img, valid_name, 80, 8080)


@app.route("/vmInstance/", methods=['POST'])
@cross_origin()
def create_vm_instances():
    response = request.get_json()
    print(response)
    img = response['image_tag']
    version = response['version'] 
    vm_number = response['vm_instance_number']
    vm_name = response['vm_name']

    return 200

    # if (vm_number > 0):
    #     valid_name = genrate_valid_name(img)
    #     tf.create_vm_instances(vm_number)
    #     tf.create_vm_instances(vm_name=vm_name, image_name_tag="{}:{}".format(img, version), container_name=valid_name, vm_number=vm_number)


@app.route("/k8sCluster/", methods=['POST'])
@cross_origin()
def create_k8s_cluster(node_count):
    if request.method == 'POST':
        node_count = request.form.get('node_count')
        img = request.form.get('image_tag')
        version = request.form.get('version')
    else:
        return jsonify(isError= True,
                    message= "bad access",
                    statusCode= 404,
                    data= ""), 404
    
    if (node_count>0):
        valid_name = genrate_valid_name(img)
        tf.create_k8s_cluster(node_count)
        helm.run_helm(name=valid_name, image_name=img, image_tag=version)

        

# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500, debug=False)