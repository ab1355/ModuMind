# Agent Development Guide

This guide covers the process of creating, configuring, and deploying new AI agents within ModuMind.

## Understanding the ModuMind Agent Architecture

ModuMind follows the LangManus agent architecture with these principles:

1. **Agent Specialization**: Each agent has a specific role and capability set
2. **Orchestration**: The Orchestrator Agent coordinates all other agents
3. **Standardized Communication**: Agents communicate via REST API calls
4. **State Management**: Each agent maintains its own state and context
5. **Plugin Extensibility**: Agents can use PluginBoard for external tool access

## Agent Types

ModuMind supports the following agent types:

- **Orchestrator**: Coordinates tasks and manages agent workflows
- **Researcher**: Performs information gathering and analysis tasks
- **Executor**: Takes actions on external systems based on decisions
- **Communication**: Handles user interactions and content generation
- **Specialist**: Domain-specific agents for specialized tasks

## Creating a New Agent

### 1. Define Agent Capabilities

First, clearly define what your agent will do:

- What is the agent's specific role?
- What tasks will it perform?
- What external systems will it need to access?
- What inputs does it need and outputs will it produce?

### 2. Create Agent Directory Structure

Create a new directory for your agent with the following structure:

```
agents/
└── your-agent-name/
    ├── Dockerfile             # Container definition
    ├── requirements.txt       # Python dependencies
    ├── main.py                # Entry point
    ├── agent.py               # Agent implementation
    ├── prompt_templates/      # LLM prompts
    │   ├── system.txt
    │   └── user.txt
    ├── plugins/               # PluginBoard integrations
    └── tests/                 # Unit tests
```

### 3. Implement Agent Core

Create the agent implementation in `agent.py`:

```python
from langmanus.agent import BaseAgent
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os

class YourAgentConfig(BaseModel):
    """Configuration for your agent."""
    model_name: str = os.getenv("AGENT_MODEL", "gpt-4")
    temperature: float = 0.2
    max_tokens: int = 1000
    # Add custom configuration fields

class YourAgentState(BaseModel):
    """State for your agent."""
    conversation_history: List[Dict[str, str]] = []
    context: Dict[str, Any] = {}
    # Add custom state fields

class YourAgent(BaseAgent):
    """Implementation of your custom agent."""
    
    def __init__(self, config: Optional[YourAgentConfig] = None):
        """Initialize the agent with configuration."""
        self.config = config or YourAgentConfig()
        self.state = YourAgentState()
        # Initialize any other components
        
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming requests.
        
        Args:
            input_data: The input data from the request
            
        Returns:
            Dictionary with the agent's response
        """
        # 1. Update state with input
        self.update_state(input_data)
        
        # 2. Create LLM prompt
        prompt = self.create_prompt()
        
        # 3. Get LLM response
        llm_response = self.call_llm(prompt)
        
        # 4. Parse and process the response
        parsed_response = self.parse_response(llm_response)
        
        # 5. Update state with results
        self.update_state_with_results(parsed_response)
        
        # 6. Return the results
        return {
            "agent_response": parsed_response,
            "status": "success"
        }
    
    def create_prompt(self) -> str:
        """Create the prompt for the LLM."""
        # Load prompt templates
        with open("prompt_templates/system.txt", "r") as f:
            system_prompt = f.read()
            
        with open("prompt_templates/user.txt", "r") as f:
            user_prompt = f.read()
        
        # Format prompts with current state
        formatted_system = system_prompt.format(
            # Add variables from state
        )
        
        formatted_user = user_prompt.format(
            # Add variables from state and input
        )
        
        # Return combined prompt
        return f"{formatted_system}\n\n{formatted_user}"
    
    def call_llm(self, prompt: str) -> str:
        """Call the LLM with the prompt."""
        # Import based on your LLM provider
        import openai
        
        response = openai.chat.completions.create(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            messages=[
                {"role": "system", "content": prompt.split("\n\n")[0]},
                {"role": "user", "content": prompt.split("\n\n")[1]}
            ]
        )
        
        return response.choices[0].message.content
    
    def parse_response(self, llm_response: str) -> Dict[str, Any]:
        """Parse the LLM response into structured data."""
        # Implement parsing logic based on your agent's needs
        # This could involve JSON parsing, regex, or custom parsing
        return {
            "content": llm_response,
            "parsed_actions": []  # Add any structured data
        }
    
    def update_state(self, input_data: Dict[str, Any]) -> None:
        """Update agent state with new input."""
        # Add input to conversation history
        self.state.conversation_history.append({
            "role": "user",
            "content": input_data.get("message", "")
        })
        
        # Update context with any new information
        if "context" in input_data:
            self.state.context.update(input_data["context"])
    
    def update_state_with_results(self, results: Dict[str, Any]) -> None:
        """Update agent state with results."""
        # Add agent response to conversation history
        self.state.conversation_history.append({
            "role": "assistant",
            "content": results.get("content", "")
        })
```

### 4. Create API Entry Point

Create `main.py` as the FastAPI entry point:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from agent import YourAgent, YourAgentConfig

# Initialize FastAPI app
app = FastAPI(title="Your Agent Service")

# Initialize the agent
agent_config = YourAgentConfig()
agent = YourAgent(config=agent_config)

class AgentRequest(BaseModel):
    """Request model for agent endpoints."""
    message: str
    context: Optional[Dict[str, Any]] = {}

class AgentResponse(BaseModel):
    """Response model for agent endpoints."""
    agent_response: Dict[str, Any]
    status: str

@app.post("/process", response_model=AgentResponse)
async def process_request(request: AgentRequest):
    """Process a request with the agent."""
    try:
        result = agent.process(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Run the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

### 5. Define Prompt Templates

Create `prompt_templates/system.txt`:

```
You are an AI agent specialized in [describe agent role]. Your task is to [describe main function].

You have access to the following tools:
- Tool 1: [Description]
- Tool 2: [Description]

Guidelines:
1. [Guideline 1]
2. [Guideline 2]
3. [Guideline 3]

Current context:
{context}
```

Create `prompt_templates/user.txt`:

```
User request: {message}

Please respond with:
1. Your analysis of the request
2. The actions you will take
3. The final response to the user

Ensure your response follows the required format for proper parsing.
```

### 6. Create Dockerfile

Create a `Dockerfile` for containerization:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
```

Create `requirements.txt`:

```
fastapi==0.95.1
uvicorn==0.22.0
openai==0.27.6
pydantic==1.10.7
langmanus==0.1.0
```

## Testing Your Agent

### 1. Unit Tests

Create test files in the `tests/` directory:

```python
# tests/test_agent.py
import unittest
from unittest.mock import patch, MagicMock
from agent import YourAgent, YourAgentConfig

class TestYourAgent(unittest.TestCase):
    
    def setUp(self):
        self.agent = YourAgent()
    
    @patch('agent.YourAgent.call_llm')
    def test_process(self, mock_call_llm):
        # Mock LLM response
        mock_call_llm.return_value = "Test LLM response"
        
        # Test input
        input_data = {
            "message": "Test message",
            "context": {"key": "value"}
        }
        
        # Call process
        result = self.agent.process(input_data)
        
        # Assert results
        self.assertEqual(result["status"], "success")
        self.assertIn("agent_response", result)

if __name__ == '__main__':
    unittest.main()
```

### 2. Run Tests

Run tests with pytest:

```bash
cd agents/your-agent-name
pytest
```

## Registering Your Agent with the Orchestrator

Update the Orchestrator Agent's configuration to include your new agent:

```python
# In orchestrator/agent.py

REGISTERED_AGENTS = {
    "researcher": {
        "base_url": os.getenv("RESEARCHER_BASE_URL", "http://researcher:5001"),
        "capabilities": ["search", "analyze", "summarize"]
    },
    "executor": {
        "base_url": os.getenv("EXECUTOR_BASE_URL", "http://executor:5002"),
        "capabilities": ["execute", "notify", "schedule"]
    },
    # Add your new agent
    "your-agent-name": {
        "base_url": os.getenv("YOUR_AGENT_BASE_URL", "http://your-agent-name:5000"),
        "capabilities": ["capability1", "capability2"]
    }
}
```

## Deploying Your Agent

### 1. Add to Docker Compose

Update `docker-compose.yml` to include your agent:

```yaml
services:
  # Existing services...
  
  your-agent-name:
    build:
      context: ./agents/your-agent-name
    ports:
      - "5004:5000"  # Adjust port as needed
    env_file:
      - .env
    environment:
      - AGENT_MODEL=gpt-4
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - orchestrator
```

### 2. Create Kubernetes Manifests

Create Kubernetes deployment manifest in `k8s/deployment/your-agent-name.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-agent-name
  namespace: modumind
spec:
  replicas: 1
  selector:
    matchLabels:
      app: your-agent-name
  template:
    metadata:
      labels:
        app: your-agent-name
    spec:
      containers:
      - name: your-agent-name
        image: ${YOUR_REGISTRY}/modumind-your-agent-name:latest
        ports:
        - containerPort: 5000
        env:
        - name: AGENT_MODEL
          value: "gpt-4"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

Create Kubernetes service manifest in `k8s/service/your-agent-name.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: your-agent-name
  namespace: modumind
spec:
  selector:
    app: your-agent-name
  ports:
  - port: 5000
    targetPort: 5000
  type: ClusterIP
```

## Advanced Agent Features

### Adding PluginBoard Capabilities

To enable your agent to use external tools via PluginBoard:

1. Create plugin connectors in the `plugins/` directory
2. Add plugin loading and invocation to your agent

Example plugin connector:

```python
# plugins/example_plugin.py
from typing import Dict, Any

class ExamplePlugin:
    """Example plugin for external tool usage."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize with configuration."""
        self.config = config
        # Set up any necessary authentication
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the plugin with the given parameters."""
        # Implement plugin logic
        return {
            "status": "success",
            "results": "Example result"
        }
```

Update your agent to use plugins:

```python
# In agent.py

from plugins.example_plugin import ExamplePlugin

class YourAgent(BaseAgent):
    def __init__(self, config=None):
        # Existing initialization
        
        # Initialize plugins
        self.plugins = {
            "example_plugin": ExamplePlugin(config={
                "api_key": os.getenv("EXAMPLE_PLUGIN_API_KEY")
            })
        }
    
    def execute_plugin(self, plugin_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a plugin with parameters."""
        if plugin_name not in self.plugins:
            return {"status": "error", "message": f"Plugin {plugin_name} not found"}
        
        try:
            result = self.plugins[plugin_name].execute(params)
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}
```

### Implementing Agent Memory

For long-term agent memory:

1. Configure a database connection
2. Add memory management methods

Example memory implementation:

```python
# In agent.py

from databases import Database
import json

class YourAgent(BaseAgent):
    def __init__(self, config=None):
        # Existing initialization
        
        # Initialize database connection
        self.db = Database(os.getenv("DATABASE_URL"))
    
    async def store_memory(self, key: str, data: Dict[str, Any]) -> None:
        """Store data in agent memory."""
        await self.db.execute(
            "INSERT INTO agent_memory (agent_id, key, data) VALUES (:agent_id, :key, :data)",
            {
                "agent_id": "your-agent-name",
                "key": key,
                "data": json.dumps(data)
            }
        )
    
    async def retrieve_memory(self, key: str) -> Dict[str, Any]:
        """Retrieve data from agent memory."""
        result = await self.db.fetch_one(
            "SELECT data FROM agent_memory WHERE agent_id = :agent_id AND key = :key",
            {
                "agent_id": "your-agent-name",
                "key": key
            }
        )
        
        if result:
            return json.loads(result["data"])
        return {}
```

## Best Practices for Agent Development

1. **Clear Separation of Concerns**: Each agent should have a single, well-defined purpose
2. **Robust Error Handling**: Handle LLM errors, API failures, and unexpected inputs
3. **Extensive Logging**: Log all agent actions for debugging and monitoring
4. **Testing**: Write unit tests for all agent components
5. **Prompt Engineering**: Carefully design prompts for consistent agent behavior
6. **Resource Efficiency**: Optimize LLM calls to reduce costs and latency
7. **Security**: Never expose sensitive information in prompts or logs
8. **Version Control**: Track changes to agent behavior and configuration
9. **Documentation**: Document agent capabilities, inputs, and outputs
10. **Monitoring**: Implement health checks and performance metrics