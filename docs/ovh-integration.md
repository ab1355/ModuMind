# OVH Cloud Integration Guide

This document provides detailed instructions for setting up and integrating OVH Cloud managed services with ModuMind.

## Overview of OVH Services Used

ModuMind leverages the following OVH Cloud services:

1. **Kubernetes Service**: For container orchestration
2. **Managed Database**: For reliable data storage
3. **Object Storage**: For file and asset management
4. **Workflow Management**: For automation and scheduled tasks

## Setting Up OVH Kubernetes Service

### Initial Setup

1. Log in to your OVH Control Panel
2. Navigate to Public Cloud > Containers & Orchestration > Managed Kubernetes Service
3. Click "Create a Kubernetes cluster"
4. Select your region and version (recommended: latest stable version)
5. Configure node pool:
   - Select a flavor (recommended: B2-7 for production)
   - Define number of nodes (minimum 3 for production)
   - Configure autoscaling settings if needed
6. Complete the creation process

### Connecting to Your Cluster

1. Download your kubeconfig file from the OVH Control Panel
2. Set the KUBECONFIG environment variable:
   ```bash
   export KUBECONFIG=/path/to/your-kubeconfig.yaml
   ```
3. Verify connection:
   ```bash
   kubectl cluster-info
   ```

### Deploying ModuMind to OVH Kubernetes

1. Create the ModuMind namespace:
   ```bash
   kubectl apply -f k8s/namespace.yaml
   ```
2. Create ConfigMaps and Secrets:
   ```bash
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/secrets.yaml
   ```
3. Deploy the applications:
   ```bash
   kubectl apply -f k8s/deployment/
   kubectl apply -f k8s/service/
   ```
4. Verify the deployment:
   ```bash
   kubectl get pods -n modumind
   ```

## Setting Up OVH Managed Database

### Creating a PostgreSQL Database

1. Navigate to Public Cloud > Databases > PostgreSQL
2. Click "Create a database instance"
3. Configure your database:
   - Select PostgreSQL version (recommended: 14+)
   - Choose a plan based on your needs
   - Set up initial user credentials
   - Configure network access
4. Complete the creation process

### Connecting ModuMind to the Database

1. Retrieve the connection information from the OVH Cloud Panel
2. Update the `.env` file with database credentials:
   ```
   DB_HOST=your-postgresql-host.ovh.com
   DB_PORT=5432
   DB_NAME=modumind
   DB_USER=your-username
   DB_PASSWORD=your-password
   ```
3. Configure the Kubernetes secret for database access:
   ```bash
   kubectl create secret generic db-credentials \
     --from-literal=host=your-postgresql-host.ovh.com \
     --from-literal=port=5432 \
     --from-literal=dbname=modumind \
     --from-literal=user=your-username \
     --from-literal=password=your-password \
     -n modumind
   ```

## Setting Up OVH Object Storage

### Creating Storage Containers

1. Navigate to Public Cloud > Storage > Object Storage
2. Click "Create a container"
3. Create the following containers:
   - `modumind-assets`: For general application assets
   - `modumind-backups`: For database and config backups
   - `modumind-logs`: For application logs
4. Configure access policies as needed

### Configuring Object Storage Access

1. Create API credentials in the OVH Cloud Panel
2. Update the `.env` file with storage credentials:
   ```
   OBJECT_STORAGE_REGION=your-region
   OBJECT_STORAGE_USER=your-user
   OBJECT_STORAGE_KEY=your-key
   OBJECT_STORAGE_TENANT=your-tenant
   OBJECT_STORAGE_AUTH_URL=https://auth.cloud.ovh.net/v3
   ```
3. Create the corresponding Kubernetes secret:
   ```bash
   kubectl create secret generic object-storage-credentials \
     --from-literal=region=your-region \
     --from-literal=user=your-user \
     --from-literal=key=your-key \
     --from-literal=tenant=your-tenant \
     --from-literal=auth-url=https://auth.cloud.ovh.net/v3 \
     -n modumind
   ```

## Setting Up OVH Workflow Management

OVH Workflow Management allows you to automate routine operations with scheduled workflows.

### Creating Workflows

#### Database Backup Workflow

1. Navigate to Public Cloud > Managed & Automated Services > Workflow Management
2. Click "Create a workflow"
3. Define a database backup workflow:
   ```yaml
   name: database-backup
   description: Daily backup of ModuMind PostgreSQL database
   schedule: "0 2 * * *"  # 2 AM daily
   tasks:
     - name: backup-database
       action: modumind/backup-database
       input:
         database_id: "{{ variables.database_id }}"
         backup_container: modumind-backups
         backup_prefix: pg-backup-
     - name: cleanup-old-backups
       action: modumind/cleanup-backups
       input:
         container: modumind-backups
         prefix: pg-backup-
         retention_days: 7
   ```

#### Infrastructure Scaling Workflow

```yaml
name: scale-workloads
description: Scale resources based on workday patterns
schedule: "0 8 * * 1-5"  # 8 AM weekdays
tasks:
  - name: scale-up-for-workday
    action: kubernetes/scale
    input:
      namespace: modumind
      deployment: modumind-ui
      replicas: 3
```

### Integrating with ModuMind

1. Create workflow action scripts in the `workflows/` directory
2. Use the OVH API to register custom actions
3. Configure workflow triggers in the ModuMind UI

## Using OVH Managed Services from ModuMind

### Database Access

Example Python code for connecting to OVH Managed PostgreSQL:

```python
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn
```

### Object Storage Access

Example Python code using the OpenStack Swift client:

```python
import os
import swiftclient
from dotenv import load_dotenv

load_dotenv()

def get_swift_connection():
    conn = swiftclient.Connection(
        authurl=os.getenv('OBJECT_STORAGE_AUTH_URL'),
        user=os.getenv('OBJECT_STORAGE_USER'),
        key=os.getenv('OBJECT_STORAGE_KEY'),
        tenant_name=os.getenv('OBJECT_STORAGE_TENANT'),
        auth_version='3'
    )
    return conn

def upload_file(container_name, file_path, object_name):
    conn = get_swift_connection()
    with open(file_path, 'rb') as file_obj:
        conn.put_object(
            container_name,
            object_name,
            contents=file_obj,
            content_type='application/octet-stream'
        )
```

### Workflow Management API Integration

Example Python code for triggering OVH workflows:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def trigger_workflow(workflow_id, variables=None):
    if variables is None:
        variables = {}
    
    api_key = os.getenv('OVH_API_KEY')
    api_secret = os.getenv('OVH_API_SECRET')
    consumer_key = os.getenv('OVH_CONSUMER_KEY')
    
    # This is a simplified example - actual OVH API calls require proper authentication
    headers = {
        'X-Ovh-Application': api_key,
        'Content-Type': 'application/json',
        # Add other required headers for OVH API authentication
    }
    
    payload = {
        'variables': variables
    }
    
    response = requests.post(
        f'https://api.ovh.com/1.0/cloud/project/{os.getenv("OVH_PROJECT_ID")}/workflow/{workflow_id}/execute',
        headers=headers,
        json=payload
    )
    
    return response.json()
```

## Best Practices for OVH Integration

### Security Best Practices

1. Use OVH API keys with the minimum required permissions
2. Rotate credentials regularly
3. Store secrets in Kubernetes secrets, not in code
4. Use network policies to restrict access to databases

### Cost Optimization

1. Use OVH's built-in cost estimation tools
2. Set up budget alerts
3. Configure auto-scaling for Kubernetes nodes
4. Use workflows to scale down resources during off-hours

### Monitoring and Logs

1. Configure OVH Logs Data Platform for centralized logging
2. Set up Prometheus and Grafana for monitoring
3. Create dashboards for OVH service metrics
4. Configure alerts for unusual resource usage

## Troubleshooting Common Issues

### Database Connectivity

1. Check that the IP whitelist includes your Kubernetes nodes
2. Verify that credentials are correct
3. Check database service status in OVH Control Panel

### Object Storage Access

1. Verify that API credentials have the correct permissions
2. Check container access policies
3. Ensure the correct endpoint is being used

### Workflow Execution Failures

1. Check workflow execution logs in OVH Control Panel
2. Verify that workflow variables are correctly set
3. Check that workflow permissions are sufficient