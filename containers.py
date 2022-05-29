import docker
  

class Containers:
    def __init__(self):
        self.client = docker.from_env()

    def get_all_containers_name(self):
        running_container = self.client.containers.list(all=True)
        print([container.name for container in running_container])
        return [container.name for container in running_container]

    def run_container(self, container_name, port, target_port):
        img = self.client.images.pull(container_name)
        self.client.containers.run(img, detach=True, ports={port: target_port}, name=container_name)