# ModuMind

ModuMind is a powerful AI agent orchestration system designed for non-technical users. Built with LangManus, NiceGUI, and integrated with OVH Cloud services, it enables the creation and management of intelligent agents for automation, research, and business process optimization.

## Features

- **Multi-Agent Orchestration**: Coordinate multiple AI agents with different specializations
- **No-Code Interface**: Configure and manage agents through an intuitive UI
- **Business Integration**: Connect with Odoo for business processes and Pimcore for digital experiences
- **API Management**: Leverage RapidAPI for unified API access and potential monetization
- **Cloud-Optimized**: Built for OVH Cloud with managed services for reduced operational overhead
- **Scalable Architecture**: Kubernetes-based deployment with horizontal scaling capabilities

## Architecture

ModuMind follows a layered architecture:

```
Infrastructure Layer → Agent Brain Layer → UI Layer → Business Integration Layer
```

For a detailed architecture overview, see [Architecture Documentation](./docs/architecture.md).

## Getting Started

### Prerequisites

- An OVH Cloud account with Kubernetes and managed database services
- Docker and kubectl installed on your local machine
- GitHub account for repository access
- API keys for OpenAI or other LLM providers

### Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/ab1355/ModuMind.git
cd ModuMind
```

2. **Configure Environment Variables**

Create a `.env` file in the root directory:

```
# LLM API Keys
OPENAI_API_KEY=your-openai-key

# OVH Cloud Configuration
OVH_PROJECT_ID=your-project-id
OVH_DATABASE_ID=your-database-id
OVH_STORAGE_ID=your-storage-id

# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# Agent Configuration
ORCHESTRATOR_BASE_URL=http://orchestrator:5000
RESEARCHER_BASE_URL=http://researcher:5001
EXECUTOR_BASE_URL=http://executor:5002
```

3. **Local Development with Docker Compose**

```bash
docker-compose up
```

This will start all necessary services including:
- Frontend UI (NiceGUI) on port 8080
- Orchestrator Agent on port 5000
- Researcher Agent on port 5001
- Executor Agent on port 5002
- Integration API on port 5003
- Monitoring stack (Prometheus/Grafana) on ports 9090/3000

4. **Kubernetes Deployment**

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment/
kubectl apply -f k8s/service/
```

5. **Access the UI**

For local development:
- Open `http://localhost:8080` in your browser

For Kubernetes deployment:
- Get the external IP: `kubectl get svc modumind-ui -n modumind`
- Open `http://<EXTERNAL_IP>:8080` in your browser

## Development Guide

### Project Structure

```
ModuMind/
├── agents/                # Agent implementations
│   ├── orchestrator/      # Orchestrator agent code
│   ├── researcher/        # Researcher agent code
│   └── executor/          # Executor agent code
├── api/                   # API definitions and integration layer
├── ui/                    # NiceGUI dashboard code
├── integration/           # Integration connectors
│   ├── odoo/              # Odoo connector
│   └── pimcore/           # Pimcore connector
├── k8s/                   # Kubernetes manifests
├── docs/                  # Documentation
└── docker-compose.yml     # Local development setup
```

### Adding a New Agent

1. Create a new directory in `agents/`
2. Implement the agent using LangManus patterns
3. Add the agent to `docker-compose.yml`
4. Create Kubernetes manifests in `k8s/deployment/` and `k8s/service/`

### Customizing the UI

The NiceGUI dashboard can be customized by modifying files in the `ui/` directory:

```python
# Example UI customization in ui/dashboard.py
from nicegui import ui

def create_dashboard():
    with ui.card():
        ui.label('Agent Status')
        # Add your custom UI components here
```

## Using OVH Managed Services

### Setting Up OVH Workflow Management

1. Access the OVH Cloud Control Panel
2. Navigate to Managed & Automated Services > Workflow Management
3. Create workflows for common operations:
   - Database backups
   - Infrastructure scaling
   - Log archiving
   - Service health monitoring

### Configuring OVH Managed Databases

1. Create a managed database instance
2. Configure access credentials
3. Update the connection details in your `.env` file
4. Ensure Kubernetes services can access the database

### Leveraging OVH Object Storage

1. Create a storage bucket for assets
2. Configure access credentials
3. Update the storage configuration in your `.env` file
4. Use the provided SDK for uploading and retrieving objects

## Business System Integration

### Odoo Integration

ModuMind integrates with Odoo for business operations:

1. Configure Odoo connection details in `.env`
2. Use the `/integration/odoo/connector.py` module
3. Map agent actions to Odoo business processes

### Pimcore Integration

For digital asset management and customer experiences:

1. Configure Pimcore connection details in `.env`
2. Use the `/integration/pimcore/connector.py` module
3. Leverage Pimcore's API for content management

## Monitoring and Logging

ModuMind includes a comprehensive monitoring stack:

- **Prometheus**: Collects metrics from all services
- **Grafana**: Visualizes metrics with pre-configured dashboards
- **Structured Logging**: All agents output JSON-formatted logs
- **OVH Log Management**: Optional integration for centralized logging

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [LangManus](https://github.com/langmanus/langmanus) for agent orchestration
- [NiceGUI](https://github.com/zauberzeug/nicegui) for the UI framework
- [OVH Cloud](https://www.ovhcloud.com/) for managed cloud services
- And all other open-source projects that made this possible