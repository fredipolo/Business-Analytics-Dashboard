# ============================================================
# main.tf - Business Analytics Dashboard Infrastructure
# Provisions EC2 instance, Security Group, and Key Pair on AWS
# ============================================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

# Get latest Ubuntu 22.04 LTS AMI automatically
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Security Group
resource "aws_security_group" "analytics_dashboard_sg" {
  name        = "analytics-dashboard-sg"
  description = "Security group for Business Analytics Dashboard EC2 instance"

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP web traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Flask/Gunicorn application port"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "analytics-dashboard-sg"
    Project     = "Business Analytics Dashboard"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# SSH Key Pair
resource "aws_key_pair" "analytics_dashboard_key" {
  key_name   = var.key_pair_name
  public_key = file(var.public_key_path)

  tags = {
    Name      = "analytics-dashboard-key"
    ManagedBy = "Terraform"
  }
}

# EC2 Instance
resource "aws_instance" "analytics_dashboard" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.analytics_dashboard_key.key_name
  vpc_security_group_ids = [aws_security_group.analytics_dashboard_sg.id]

  # Bootstrap: install Docker and run container on first boot
  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get upgrade -y

    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh

    usermod -aG docker ubuntu
    systemctl enable docker
    systemctl start docker

    # Pull and run the analytics dashboard container
    docker pull ${var.docker_image}
    docker run -d \
      --name analytics-dashboard \
      --restart always \
      -p 80:5000 \
      ${var.docker_image}
  EOF

  tags = {
    Name        = "analytics-dashboard-server"
    Project     = "Business Analytics Dashboard"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}
