# Ansible Configuration Management - Business Analytics Dashboard

## Overview
This Ansible project automates full server configuration: installs Docker,
enables it on boot, and deploys the containerised Flask application.

## Structure
```
ansible/
├── site.yml              # Master playbook - runs all roles
├── inventory.ini         # Target server definitions
└── roles/
    ├── docker/
    │   └── tasks/
    │       └── main.yml  # Installs & configures Docker
    └── app/
        └── tasks/
            └── main.yml  # Deploys the analytics dashboard container
```

## Usage

### 1. Update inventory with your EC2 IP
Edit `inventory.ini` and replace `YOUR_EC2_IP_HERE` with the IP output from `terraform apply`.

### 2. Test connection
```bash
ansible -i inventory.ini all -m ping
```

### 3. Run full playbook
```bash
ansible-playbook -i inventory.ini site.yml
```

## Automation Flow
```
ansible-playbook site.yml
        ↓
[Docker Role]
  - Install Docker Engine
  - Enable Docker on boot
  - Add ubuntu user to docker group
        ↓
[App Role]
  - Pull fredipolodev/business-analytics-dashboard:latest
  - Stop & remove any existing container
  - Deploy container (port 80→5000, restart always)
  - Health check
        ↓
✅ Dashboard live at http://YOUR_EC2_IP
```
