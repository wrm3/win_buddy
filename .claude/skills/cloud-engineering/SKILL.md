---
name: cloud-engineering
description: Comprehensive guide for cloud architecture, infrastructure as code, and cost optimization across AWS, GCP, and Azure. Covers Terraform, Kubernetes, serverless, and multi-cloud strategies. Use when working with cloud infrastructure or deployment.
triggers:
  - "AWS"
  - "GCP"
  - "Azure"
  - "cloud"
  - "Terraform"
  - "infrastructure"
  - "serverless"
  - "Lambda"
  - "EC2"
  - "cost optimization"
agents:
  - cloud-engineer
version: 1.0.0
---

# Cloud Engineering Skill

Comprehensive reference for cloud architecture, infrastructure as code, and cost optimization. This skill supports the `cloud-engineer` agent.

## Cloud Platform Comparison

### Quick Reference

| Feature | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Compute | EC2, ECS, Lambda | GCE, GKE, Cloud Run | VMs, AKS, Functions |
| Database | RDS, DynamoDB | Cloud SQL, Firestore | SQL DB, Cosmos DB |
| Storage | S3 | Cloud Storage | Blob Storage |
| Kubernetes | EKS | GKE | AKS |
| Serverless | Lambda | Cloud Functions | Functions |
| CDN | CloudFront | Cloud CDN | Azure CDN |
| DNS | Route 53 | Cloud DNS | Azure DNS |

### When to Choose Each

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Enterprise/Legacy | AWS or Azure | Mature, compliance |
| ML/Data | GCP | BigQuery, Vertex AI |
| Kubernetes | GCP (GKE) | Best managed K8s |
| Microsoft stack | Azure | Native integration |
| Startups | AWS | Widest adoption |
| Cost-sensitive | GCP | Sustained discounts |

---

## AWS Quick Reference

### Compute Options

| Service | Use Case | Pricing |
|---------|----------|---------|
| EC2 | General compute | Per-hour |
| ECS/Fargate | Containers | Per-vCPU/memory |
| Lambda | Event-driven | Per-invocation |
| App Runner | Simple containers | Per-vCPU/memory |

### EC2 Instance Selection

```
General Purpose (M-series): Balanced compute/memory
- m6i.large: 2 vCPU, 8 GB - $0.096/hr
- m6i.xlarge: 4 vCPU, 16 GB - $0.192/hr

Compute Optimized (C-series): CPU-intensive
- c6i.large: 2 vCPU, 4 GB - $0.085/hr
- c6i.xlarge: 4 vCPU, 8 GB - $0.170/hr

Memory Optimized (R-series): Memory-intensive
- r6i.large: 2 vCPU, 16 GB - $0.126/hr
- r6i.xlarge: 4 vCPU, 32 GB - $0.252/hr

GPU (P/G-series): ML/Graphics
- g4dn.xlarge: 4 vCPU, 16 GB, T4 GPU - $0.526/hr
- p4d.24xlarge: 96 vCPU, 1152 GB, 8x A100 - $32.77/hr
```

### Common Architectures

**Web Application (Standard)**
```
CloudFront → ALB → ECS/EC2 → RDS
                 ↓
              ElastiCache
```

**Serverless**
```
API Gateway → Lambda → DynamoDB
                    ↓
                   S3
```

**Event-Driven**
```
SQS/SNS → Lambda → DynamoDB
   ↑
EventBridge
```

---

## Terraform

### Project Structure

```
infrastructure/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs/
│   └── rds/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
├── backend.tf
└── versions.tf
```

### Essential Patterns

**Remote State (S3)**
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**VPC Module**
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true  # Cost savings for non-prod

  tags = {
    Environment = "production"
    Terraform   = "true"
  }
}
```

**ECS Service**
```hcl
resource "aws_ecs_service" "app" {
  name            = "my-app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8080
  }
}
```

### Terraform Commands

```bash
# Initialize
terraform init

# Plan (preview changes)
terraform plan -out=tfplan

# Apply
terraform apply tfplan

# Destroy (careful!)
terraform destroy

# Format
terraform fmt -recursive

# Validate
terraform validate

# Import existing resource
terraform import aws_instance.example i-1234567890abcdef0
```

---

## Cost Optimization

### Quick Wins

| Strategy | Savings | Effort |
|----------|---------|--------|
| Reserved Instances (1yr) | 30-40% | Low |
| Spot Instances | 60-90% | Medium |
| Right-sizing | 20-50% | Medium |
| S3 Lifecycle Policies | 30-70% | Low |
| Scheduled scaling | 20-40% | Medium |

### Reserved vs Spot vs On-Demand

| Type | Best For | Savings | Risk |
|------|----------|---------|------|
| On-Demand | Variable, testing | 0% | None |
| Reserved (1yr) | Steady workloads | 30-40% | Commitment |
| Reserved (3yr) | Long-term | 50-60% | Commitment |
| Spot | Fault-tolerant | 60-90% | Interruption |
| Savings Plans | Flexible commitment | 30-40% | Commitment |

### Cost Allocation Tags

```hcl
# Always tag resources
resource "aws_instance" "example" {
  # ... config ...

  tags = {
    Name        = "web-server-1"
    Environment = "production"
    Team        = "platform"
    CostCenter  = "engineering"
    Project     = "main-app"
  }
}
```

### S3 Cost Optimization

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
```

### Monthly Cost Checklist

```
□ Review AWS Cost Explorer
  □ Check for unexpected spikes
  □ Identify unused resources
  □ Review Reserved Instance coverage

□ Right-sizing
  □ Check EC2 CPU/memory utilization
  □ Review RDS instance sizes
  □ Check Lambda memory settings

□ Storage
  □ Review S3 storage classes
  □ Delete old snapshots
  □ Clean up unused EBS volumes

□ Network
  □ Check NAT Gateway usage
  □ Review data transfer costs
  □ Optimize CloudFront caching
```

---

## Security Best Practices

### IAM Principles

```
1. Least Privilege
   - Grant minimum permissions needed
   - Use specific resource ARNs
   - Avoid wildcards (*)

2. No Root Access
   - Never use root account
   - Enable MFA on root
   - Use IAM users/roles

3. Use Roles, Not Keys
   - EC2 instance profiles
   - ECS task roles
   - Lambda execution roles
```

### Security Group Rules

```hcl
# Good: Specific rules
resource "aws_security_group" "web" {
  name = "web-sg"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Bad: Too permissive
resource "aws_security_group" "bad" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Never do this!
  }
}
```

### Secrets Management

```hcl
# Use AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  # ... config ...
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}

# Or use SSM Parameter Store
data "aws_ssm_parameter" "api_key" {
  name            = "/prod/api/key"
  with_decryption = true
}
```

---

## Monitoring & Observability

### CloudWatch Essentials

```hcl
# CloudWatch Alarm
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-utilization-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "CPU utilization exceeded 80%"
  alarm_actions       = [aws_sns_topic.alerts.arn]

  dimensions = {
    InstanceId = aws_instance.web.id
  }
}
```

### Key Metrics to Monitor

| Service | Metric | Alert Threshold |
|---------|--------|-----------------|
| EC2 | CPUUtilization | >80% |
| RDS | CPUUtilization | >80% |
| RDS | FreeStorageSpace | <20% |
| ALB | TargetResponseTime | >1s (P95) |
| ALB | HTTPCode_ELB_5XX | >1% |
| Lambda | Errors | >1% |
| Lambda | Duration | >80% timeout |

---

## Multi-Cloud Strategy

### When to Go Multi-Cloud

**Do Multi-Cloud If:**
- Regulatory requirements
- Vendor negotiation leverage
- Best-of-breed services needed
- Disaster recovery requirements

**Don't Multi-Cloud If:**
- Small team
- Limited budget
- No specific requirement
- Complexity would hurt velocity

### Cloud-Agnostic Approach

```
Use portable technologies:
✓ Kubernetes (runs anywhere)
✓ Terraform (multi-cloud IaC)
✓ PostgreSQL (managed or self-hosted)
✓ Redis (managed or self-hosted)
✓ S3-compatible storage
```

### Terraform Multi-Cloud

```hcl
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "google" {
  project = "my-project"
  region  = "us-central1"
}
```

---

## Templates & Resources

### Reference Documents
- `reference/aws_services.md` - AWS service guide
- `reference/gcp_services.md` - GCP service guide
- `reference/cost_optimization.md` - Cost reduction strategies
- `reference/security_checklist.md` - Security best practices

### Templates
- `templates/vpc.tf` - VPC Terraform template
- `templates/ecs_service.tf` - ECS service template
- `templates/lambda.tf` - Lambda function template
- `templates/rds.tf` - RDS database template

### External Resources
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)
- [Terraform Registry](https://registry.terraform.io)
- [AWS Pricing Calculator](https://calculator.aws)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)

---
*This skill supports: cloud-engineer agent*
