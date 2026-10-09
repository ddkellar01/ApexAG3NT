import asyncio
from typing import List, Dict, Any

class MorpheusOrchestrator:
    """Asynchronous multi-agent orchestration backend coordinating parallel agentic loops."""

    def __init__(self, agent_roles: List[str]):
        self.roles = agent_roles
        self.channel: asyncio.Queue = asyncio.Queue()

    async def agent_worker(self, name: str):
        """Worker loop processing messages from the shared agent channel."""
        while True:
            task = await self.channel.get()
            # Simulate specialized task processing based on role
            await asyncio.sleep(0.2)
            task["completed_by"] = name
            self.channel.task_done()

    async def coordinate(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Dispatches tasks concurrently across the agent swarm."""
        for task in tasks:
            await self.channel.put(task)

        workers = [asyncio.create_task(self.agent_worker(role)) for role in self.roles]
        await self.channel.join()
        
        for w in workers:
            w.cancel()
            
        return tasks
