#!/usr/bin/env python3
"""
MCP Server - Data Models
Defines the data models used in the MCP server application
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import uuid
from enum import Enum

class AgentStatus(str, Enum):
    """Agent status enum"""
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"

class TaskStatus(str, Enum):
    """Task status enum"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Agent(BaseModel):
    """Agent model representing an agent in the system"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    status: AgentStatus = AgentStatus.OFFLINE
    capabilities: List[str] = []
    last_heartbeat: Optional[datetime] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "worker-agent-1",
                "description": "General purpose worker agent",
                "capabilities": ["process_data", "run_analysis"],
                "metadata": {"region": "us-west", "version": "1.0.0"}
            }
        }
    }

class Task(BaseModel):
    """Task model representing a unit of work"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    type: str
    status: TaskStatus = TaskStatus.PENDING
    agent_id: Optional[str] = None
    priority: int = 0  # Higher number = higher priority
    parameters: Dict[str, Any] = {}
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Data Processing Task",
                "description": "Process customer data for Q1 2023",
                "type": "data_processing",
                "priority": 5,
                "parameters": {
                    "data_source": "s3://company-data/customers/q1_2023",
                    "output_format": "csv"
                }
            }
        }
    }

class TaskResult(BaseModel):
    """Task result model for reporting task completion"""
    task_id: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "task_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "completed",
                "result": {
                    "processed_records": 1254,
                    "output_location": "s3://company-data/processed/q1_2023_results.csv"
                }
            }
        }
    } 