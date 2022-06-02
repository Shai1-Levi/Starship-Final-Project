variable "project_id" {
  type        = string
  description = "name of the project_id on gcp console"
  default     = "elevated-valve-317623"
}
variable "region" {
  type        = string
  description = "the ragion the project is loacted"
  default     = "us-central-1"
}

variable "vm-instance-image" {
  type        = string
  description = "instance machine type"
  default     = "ubuntu-1804-bionic-v20220331a" 
}

variable "machine_type" {
  type        = string
  description = "The kind of the machine type to create"
  default     = "f1-micro"
}

variable "vm-instance-name" {
  type        = string
  description = "instance name should be unique"
  default     = "vm-terraform-starship-000-staging"
}


variable "container_name" {
  type        = string
  description = "name of the container can iclude only letters and digits"
  default     = "samba"
}

variable "image_name_tag" {
  type        = string
  description = "name of the iamge that should run on the vm"
  default     = "dperson/samba:latest"
}


variable "expose_container_port" {
  type        = number
  description = "the port to expose the conatiner"
  default     = 80
}