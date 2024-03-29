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
  name    = "http-server"
  network = local.network

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "403"]
  }

  priority = 1000

  // Allow traffic from all IP to instances with an http-server tag
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"] 
}

resource "google_compute_firewall" "web-rule" {
  project = local.project_id
  name    = "web-rule"
  network = local.network

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }

  priority = 1000

  // Allow traffic from all IP to instances with an http-server tag
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-rule"] 
}

resource "google_compute_firewall" "ssh-rule" {
  project = local.project_id
  name = "ssh-rule"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports = ["22"]
  }
  // Allow traffic from my IP to instances with an http-server tag
  target_tags = ["ssh-rule"]
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
  tags = ["http-server", "https-server", "ssh-rule", "web-rule"] // Apply the firewall rule to allow external IPs to access this instance

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

  provisioner "file"{
    source      = "../docker-compose.yaml"
    destination = "docker-compose.yaml"  
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get -y  update",

      # installing docker-compose on vm 
      "mkdir -p ~/.docker/cli-plugins/",
      "curl -SL https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose",
      "chmod +x ~/.docker/cli-plugins/docker-compose",

      # installing docker on vm 
      "sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",

      # sudo apt update
      "sudo apt-get install --yes docker-ce",

      # run hermes on VM
      "sudo docker compose up -d"
    ]
  }
}
