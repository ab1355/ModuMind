# ModuMind

An intelligent agent orchestration system built with LangManus, NiceGUI, and PluginBoard.

## Overview

ModuMind is a no-code AI orchestration platform that integrates multiple AI agents to perform complex tasks. It leverages OVH Cloud for infrastructure, Supabase for authentication and database, and connects with Odoo for business process automation.

## Architecture

- **Brain Layer**: LangManus for agent orchestration
- **UI Layer**: NiceGUI for dashboard and configuration
- **Integration Layer**: PluginBoard/Wildcard for external tools and APIs
- **Infrastructure**: Kubernetes on OVH Cloud managed by Syself

## Components

- Agent Orchestration: Coordinated multi-agent system with specialized roles
- User Interface: Intuitive dashboard for configuring and monitoring agents
- External Integrations: Connections to Odoo ERP and other systems
- Monitoring: Real-time logs and performance metrics

## Development

### Prerequisites

- Docker and Docker Compose
- kubectl
- Helm
- OVH Cloud account
- Supabase account
- Odoo instance

### Local Setup

1. Clone this repository
2. Configure environment variables
3. Run `docker-compose up` for local development

### Deployment

The system is deployed on OVH Cloud Kubernetes service using GitOps principles.