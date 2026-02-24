# Business Analytics Dashboard

A Flask-based business analytics dashboard displaying revenue metrics, monthly trends, and top product performance. Deployed on AWS EC2 using a fully automated pipeline with Terraform, Ansible, Docker, and GitHub Actions.

## Features
- Real-time business metrics (Total Revenue, Units Sold, Avg Order Value)
- Monthly revenue trend chart
- Top products bar chart
- Dark themed responsive UI
- Health check endpoint at `/health`

## Tech Stack
| Layer | Tool |
|---|---|
| Infrastructure | Terraform |
| Configuration | Ansible |
| Containerisation | Docker |
| CI/CD | GitHub Actions |
| Cloud | AWS EC2 (t3.micro, us-east-1) |
| App | Python / Flask / Gunicorn |

## Run Locally

```bash
# Without Docker
pip install -r requirements.txt
python app.py

# With Docker
docker build -t business-analytics-dashboard .
docker run -p 5000:5000 business-analytics-dashboard
```
Visit: http://54.221.106.92/

## Deployment Steps

### 1. Provision Infrastructure
```bash
cd terraform-scripts
terraform init
terraform plan
terraform apply
# Note the public_ip from outputs
```

### 2. Configure Server
```bash
cd ansible
# Update inventory.ini with your EC2 IP
ansible-playbook -i inventory.ini site.yml
```

### 3. CI/CD - GitHub Actions
Set the following repository secrets in GitHub:
- `DOCKER_USERNAME` — Docker Hub username
- `DOCKER_PASSWORD` — Docker Hub access token
- `EC2_HOST` — your EC2 public IP
- `EC2_USERNAME` — `ubuntu`
- `EC2_SSH_KEY` — your private SSH key contents

Copy `cicd-files/.github/` to `.github/` in your repo root. Every push to `main` will automatically build, push, and deploy.

## Repository Structure
```
├── app.py                          # Flask application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container definition
├── ansible/                        # Configuration management
│   ├── site.yml                    # Master playbook
│   ├── inventory.ini               # Target servers
│   └── roles/
│       ├── docker/tasks/main.yml   # Docker installation
│       └── app/tasks/main.yml      # Container deployment
├── terraform-scripts/              # Infrastructure as code
│   ├── main.tf                     # EC2, SG, Key Pair
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
└── cicd-files/
    └── .github/workflows/
        └── deploy.yml              # GitHub Actions pipeline
```

## Author
GitHub: fredipolo  
Module: B9IS121 - Network Systems and Administration  
Dublin Business School
