import os
import logging
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
from langmanus import Agent, Task, Message, AgentRole

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrchestratorAgent(Agent):
    """
    Main orchestrator agent that coordinates other specialized agents.
    """
    
    def __init__(self, name: str, model: str, api_key: Optional[str] = None):
        """
        Initialize the orchestrator agent.
        
        Args:
            name: The name of the agent
            model: The LLM model to use
            api_key: API key for the LLM provider
        """
        super().__init__(
            name=name,
            role=AgentRole.ORCHESTRATOR,
            model=model,
            api_key=api_key or os.environ.get("OPENAI_API_KEY")
        )
        self.available_agents = {}
        self.running_tasks = {}
        
    def register_agent(self, agent: Agent) -> None:
        """
        Register a specialized agent with the orchestrator.
        
        Args:
            agent: Agent instance to register
        """
        self.available_agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name} with role {agent.role}")
        
    def create_task(self, description: str, context: Dict[str, Any] = None) -> Task:
        """
        Create a new task and determine which agents should handle it.
        
        Args:
            description: The task description
            context: Additional context for the task
            
        Returns:
            A Task object
        """
        # Create task with unique ID
        task = Task(description=description, context=context or {})
        self.running_tasks[task.id] = task
        
        # Determine which agent should handle this task
        assigned_agent = self._select_agent_for_task(task)
        if assigned_agent:
            logger.info(f"Assigning task {task.id} to {assigned_agent.name}")
            assigned_agent.assign_task(task)
        else:
            logger.warning(f"No suitable agent found for task: {task.description}")
            
        return task
        
    def _select_agent_for_task(self, task: Task) -> Optional[Agent]:
        """
        Select the most appropriate agent for a given task.
        
        Args:
            task: The task to assign
            
        Returns:
            The selected agent or None if no suitable agent found
        """
        # This is a simplified agent selection strategy
        # In a full implementation, you would use the LLM to analyze the task
        # and determine which agent is best suited
        
        task_description = task.description.lower()
        
        if any(keyword in task_description for keyword in ["research", "browse", "search"]):
            return self.available_agents.get("researcher")
        elif any(keyword in task_description for keyword in ["execute", "run", "implement"]):
            return self.available_agents.get("executor")
        elif any(keyword in task_description for keyword in ["code", "program", "develop"]):
            return self.available_agents.get("coder")
        
        # Default to the executor if available
        return self.available_agents.get("executor")
        
    def handle_message(self, message: Message) -> Message:
        """
        Process incoming messages and coordinate responses.
        
        Args:
            message: The incoming message
            
        Returns:
            A response message
        """
        # Extract task from message if it exists
        task_id = message.metadata.get("task_id")
        task = self.running_tasks.get(task_id) if task_id else None
        
        if task and task.status == "completed":
            return Message(
                content=f"Task {task_id} has already been completed.",
                metadata={"task_id": task_id}
            )
            
        # Use the LLM to analyze the message and determine next steps
        # This is a placeholder for the actual LLM call
        response_content = f"Received message: {message.content}"
        
        return Message(
            content=response_content,
            metadata={"task_id": task_id if task else None}
        )


if __name__ == "__main__":
    # Example usage
    orchestrator = OrchestratorAgent(
        name="main_orchestrator",
        model="gpt-4",
    )
    
    # Create a simple task
    task = orchestrator.create_task(
        description="Research the latest developments in AI orchestration frameworks",
        context={"priority": "high"}
    )
    
    print(f"Created task: {task.id}")