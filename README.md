# MCP Server (Master Control Program)

A centralized control server for managing and coordinating distributed agents and tasks.

## Overview

The MCP Server provides a central coordination point for distributed agents, allowing for:

- Agent registration and monitoring
- Task creation and assignment
- Status tracking and reporting
- Secure API-based communication

This implementation is a skeletal structure that can be extended for specific use cases such as distributed computing, workflow orchestration, or agent-based systems.

## Features

- **Agent Management**: Register, monitor, and control distributed agents
- **Task Management**: Create, assign, and track tasks
- **API-First Design**: RESTful API with FastAPI
- **Authentication**: API key-based authentication
- **Configuration**: Environment-based configuration

## Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone the repository
```
git clone https://github.com/yourusername/mcp-server.git
cd mcp-server
```

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Configure environment variables
```
cp .env.example .env
# Edit .env with your settings
```

### Running the Server

Start the development server:
```
python server.py
```

Or using uvicorn directly:
```
uvicorn server:app --reload
```

The server will be available at http://localhost:8000. API documentation is available at http://localhost:8000/docs.

## API Documentation

Once the server is running, visit http://localhost:8000/docs for Swagger UI API documentation, or http://localhost:8000/redoc for ReDoc documentation.

### Key Endpoints

- `GET /health` - Health check endpoint
- `GET /api/v1/agents` - List all registered agents
- `POST /api/v1/agents` - Register a new agent
- `GET /api/v1/tasks` - List all tasks
- `POST /api/v1/tasks` - Create a new task
- `POST /api/v1/tasks/{task_id}/assign/{agent_id}` - Assign a task to an agent

## Development

### Project Structure

```
mcp-server/
├── server.py           # Main application entry point
├── config.py           # Configuration management
├── models.py           # Data models
├── routes.py           # API routes
├── requirements.txt    # Dependencies
├── .env.example        # Example environment variables
└── README.md           # Documentation
```

### Future Enhancements

- Database integration for persistent storage
- User authentication and multi-tenancy
- WebSocket support for real-time updates
- Advanced task scheduling and prioritization
- Agent capabilities matching for task assignment
- Monitoring dashboard

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 