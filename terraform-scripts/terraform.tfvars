# ============================================================
# terraform.tfvars - Your configuration values
# ============================================================

aws_region      = "us-east-1"
instance_type   = "t3.micro"
key_pair_name   = "analytics-dashboard-key"
public_key_path = "~/.ssh/id_ed25519.pub"
docker_image    = "fredipolodev/business-analytics-dashboard:latest"
