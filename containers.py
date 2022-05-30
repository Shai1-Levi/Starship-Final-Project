import docker
  

class Containers:
    def __init__(self):
        self.client = docker.from_env()

    def get_all_containers_name(self):
        running_container = self.client.containers.list(all=True)
        print([container.name for container in running_container])
        return [container.name for container in running_container]

    def pull_image(self, image_name):
        self.img = self.client.images.pull(image_name)

    def run_container(self, image_name, container_name, port, target_port):
       
        self.client.containers.run(image_name, detach=True, ports={port: target_port}, name=container_name)
        # return "can't run image, may be image not exist."