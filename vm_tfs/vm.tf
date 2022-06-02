locals {
  project_id       = "elevated-valve-317623"
  network          =  "default"
  image            =  var.vm-instance-image 
  user_ssh         =   "${split("@", data.google_client_openid_userinfo.me.email)[0]}"
  web_servers      = {
    (var.vm-instance-name) = {
      machine_type = var.machine_type
      zone         = "us-central1-a"
    }
    # To add more servers just copy the above and change the details
  }
}

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "ssh_private_key_pem" {
  content         = tls_private_key.ssh_key.private_key_pem
  filename        = ".ssh/google_compute_engine"
  file_permission = "0400"
}

data "http" "devip" {
  url = "http://ipv4.icanhazip.com"
}

data "google_client_openid_userinfo" "me" {}

resource "google_compute_firewall" "http-server" {
  project = local.project_id
  name    = "default-allow-http-terraform"
  network = local.network

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  priority = 1000

  // Allow traffic from all IP to instances with an http-server tag
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"] 
}

resource "google_compute_firewall" "nginx-rule" {
  project = local.project_id
  name    = "default-allow-vault-terraform"
  network = local.network

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }

  priority = 1000

  // Allow traffic from all IP to instances with an http-server tag
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["nginx-rule"] 
}

resource "google_compute_firewall" "ssh-rule" {
  project = local.project_id
  name = "vm-terraform-starship"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports = ["22"]
  }
  // Allow traffic from my IP to instances with an http-server tag
  target_tags = ["vm-terraform-starship"]
  source_ranges = ["${chomp(data.http.devip.body)}/32"]
}

resource "google_compute_network" "vpc_network" {
  name = "vm-terraform-starship"
}

resource "google_compute_instance" "default" {
  for_each              = local.web_servers
  name                  = each.key
  machine_type          = each.value.machine_type
  zone                  = each.value.zone 
  project               = local.project_id
  tags = ["http-server", "ssh-rule", "nginx-rule"] // Apply the firewall rule to allow external IPs to access this instance

  boot_disk {
    initialize_params {
      image = local.image
    }
  }

  network_interface {
    network = local.network

    access_config {
      // Include this section to give the VM an external ip address
    }
  }

  metadata = {
    ssh-keys = "${local.user_ssh}:${tls_private_key.ssh_key.public_key_openssh}"
  }

  connection {
    type        = "ssh"
    user        = local.user_ssh
    host        = self.network_interface.0.access_config.0.nat_ip
    private_key = "${file("~/.ssh/google_compute_engine")}"
    timeout     = "5m"
  }  

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get -y  update",

       # installing docker on vm 
      "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",

      # sudo apt update
      "sudo apt-get install --yes docker-ce",

      # pull the image from docker hub
      "sudo docker pull ${var.image_name_tag}",
      "sudo docker run -p ${var.expose_container_port}:${var.expose_container_port} --name ${var.container_name} ${var.image_name_tag} -d"
    ]
  }
}
