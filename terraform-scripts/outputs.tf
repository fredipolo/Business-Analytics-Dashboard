# ============================================================
# outputs.tf - Useful information after deployment
# ============================================================

output "instance_id" {
  description = "The EC2 instance ID"
  value       = aws_instance.analytics_dashboard.id
}

output "public_ip" {
  description = "Public IP address of the analytics dashboard server"
  value       = aws_instance.analytics_dashboard.public_ip
}

output "public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.analytics_dashboard.public_dns
}

output "app_url" {
  description = "URL to access the Business Analytics Dashboard"
  value       = "http://${aws_instance.analytics_dashboard.public_ip}"
}

output "ssh_command" {
  description = "SSH command to connect to the server"
  value       = "ssh -i ~/.ssh/id_ed25519 ubuntu@${aws_instance.analytics_dashboard.public_ip}"
}

output "security_group_id" {
  description = "ID of the security group created"
  value       = aws_security_group.analytics_dashboard_sg.id
}
