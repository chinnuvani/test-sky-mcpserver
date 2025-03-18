#!/usr/bin/env python3
"""
MCP Server - API Routes
Defines the API endpoints for the MCP server
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

# Local imports
from config import settings
from models import Agent, Task, TaskStatus, AgentStatus
from skysql_api import skysql_client

# Configure logger
logger = logging.getLogger("mcp_server.routes")

# Initialize router
api_router = APIRouter(prefix="/api/v1")

# Authentication dependency
async def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key for protected endpoints"""
    if not settings.API_KEYS:  # If no API keys configured, skip auth
        return True
    
    if x_api_key not in settings.API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return True

# In-memory storage for demo purposes (would use a database in production)
agents: Dict[str, Agent] = {}
tasks: Dict[str, Task] = {}

# SkySQL API endpoints
@api_router.get("/skysql/topologies")
async def get_skysql_topologies(
    service_type: str = "transactional",
    _: bool = Depends(verify_api_key)
) -> Dict[str, Any]:
    """Get available SkySQL topologies for a service type"""
    try:
        return await skysql_client.get_topologies(service_type)
    except httpx.HTTPError as e:
        logger.error(f"Error fetching SkySQL topologies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch SkySQL topologies"
        )
    except Exception as e:
        logger.error(f"Unexpected error fetching SkySQL topologies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Agent management endpoints
@api_router.post("/agents", response_model=Agent, status_code=status.HTTP_201_CREATED)
async def register_agent(agent: Agent, _: bool = Depends(verify_api_key)):
    """Register a new agent with the MCP server"""
    agent.last_heartbeat = datetime.utcnow()
    agent.status = AgentStatus.IDLE
    agents[agent.id] = agent
    logger.info(f"Agent registered: {agent.id} ({agent.name})")
    return agent

@api_router.get("/agents", response_model=List[Agent])
async def list_agents(_: bool = Depends(verify_api_key)):
    """Get all registered agents"""
    return list(agents.values())

@api_router.get("/agents/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str, _: bool = Depends(verify_api_key)):
    """Get agent details by ID"""
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents[agent_id]

@api_router.put("/agents/{agent_id}/heartbeat", response_model=Agent)
async def agent_heartbeat(
    agent_id: str, 
    status: Optional[AgentStatus] = None, 
    _: bool = Depends(verify_api_key)
):
    """Update agent heartbeat and optionally status"""
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agents[agent_id].last_heartbeat = datetime.utcnow()
    if status:
        agents[agent_id].status = status
    
    return agents[agent_id]

# Task management endpoints
@api_router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task, _: bool = Depends(verify_api_key)):
    """Create a new task"""
    task.created_at = datetime.utcnow()
    task.status = TaskStatus.PENDING
    tasks[task.id] = task
    logger.info(f"Task created: {task.id}")
    return task

@api_router.get("/tasks", response_model=List[Task])
async def list_tasks(_: bool = Depends(verify_api_key)):
    """Get all tasks"""
    return list(tasks.values())

@api_router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, _: bool = Depends(verify_api_key)):
    """Get task details by ID"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@api_router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: str, 
    update_data: Dict[str, Any],
    _: bool = Depends(verify_api_key)
):
    """Update task details"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    
    # Update task fields
    for key, value in update_data.items():
        if hasattr(task, key):
            setattr(task, key, value)
    
    # Always update the modified timestamp
    task.updated_at = datetime.utcnow()
    
    return task

@api_router.post("/tasks/{task_id}/assign/{agent_id}", response_model=Task)
async def assign_task(
    task_id: str, 
    agent_id: str,
    _: bool = Depends(verify_api_key)
):
    """Assign a task to an agent"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if agents[agent_id].status != AgentStatus.IDLE:
        raise HTTPException(status_code=400, detail="Agent is not available")
    
    # Update task and agent
    tasks[task_id].agent_id = agent_id
    tasks[task_id].status = TaskStatus.ASSIGNED
    tasks[task_id].updated_at = datetime.utcnow()
    
    agents[agent_id].status = AgentStatus.BUSY
    
    logger.info(f"Task {task_id} assigned to agent {agent_id}")
    return tasks[task_id] 