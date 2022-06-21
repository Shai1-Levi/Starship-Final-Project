import docker
from ssh_connect import RemoteClient
 

class Containers:
    def __init__(self):
        self.client = docker.from_env()
        self.ssh = RemoteClient("35.192.14.163", "shai4458", "vm\\.ssh\\google_compute_engine")
        self.ssh.connection()


    def get_all_containers_name(self):
        running_container = self.client.containers.list(all=True)
        print([container.name for container in running_container])
        return [container.name for container in running_container]

    def pull_image(self, image_name):
        self.img = self.client.images.pull(image_name)

    def run_container(self, image_name, container_name, port, target_port):
       
        self.client.containers.run(image_name, detach=True, ports={port: target_port}, name=container_name)
        # return "can't run image, may be image not exist."

    def pull_and_run_images(self,image_name_tag, container_valid_names):
        # pull and run images
        for image_name, container_name in list(zip(image_name_tag,container_valid_names)):
            print(image_name)
            self.ssh.exec_command("sudo docker pull {}".format(image_name))
            print(container_name)
            self.ssh.exec_command("sudo docker run -d --name {} {}".format(container_name, image_name))