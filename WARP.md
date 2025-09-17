# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a multi-project repository containing two main components:

### 1. Bytebot - AI Desktop Agent
- **Location**: `/bytebot/`
- **Type**: TypeScript/NestJS microservices architecture with React UI
- **Purpose**: Open-source AI desktop agent that provides AI with its own virtual desktop environment
- **Architecture**: Multi-container application with agent, UI, desktop, and optional proxy components

### 2. Gemini Connector 
- **Location**: `/gemini-connector/`
- **Type**: Python tool with async support
- **Purpose**: Direct API connector to Google's Gemini AI (replacing web scraping methods)

## Development Environment Setup

### Prerequisites
- **Node.js**: 20+ (required for Bytebot)
- **Python**: 3.11+ (required for Gemini Connector)
- **Docker & Docker Compose**: For containerized development
- **bun**: Preferred package manager (as per user preference)

### Initial Setup Commands

#### For Bytebot Development:
```bash
cd bytebot/packages/bytebot-agent
bun install
bun run prisma:dev

cd ../bytebot-ui  
bun install

cd ../shared
bun install && bun run build
```

#### For Gemini Connector Development:
```bash
cd gemini-connector
chmod +x install.sh && ./install.sh
# Then edit config/user/.env with your Gemini API key
python3 src/gemini_connector.py --validate
```

## Common Development Commands

### Bytebot Commands

#### Local Development
```bash
# Start individual services
cd bytebot/packages/bytebot-agent
bun run start:dev                    # Start agent in development mode

cd bytebot/packages/bytebot-ui  
bun run dev                          # Start UI in development mode

# Build services
cd bytebot/packages/bytebot-agent
bun run build                        # Build agent service

cd bytebot/packages/bytebot-ui
bun run build                        # Build UI

# Database operations
cd bytebot/packages/bytebot-agent
bun run prisma:dev                   # Run migrations and generate client (dev)
bun run prisma:prod                  # Deploy migrations and generate client (prod)
```

#### Docker Development
```bash
cd bytebot

# Development environment
docker-compose -f docker/docker-compose.development.yml up -d

# Core services only  
docker-compose -f docker/docker-compose.core.yml up -d

# Full production stack
docker-compose -f docker/docker-compose.yml up -d

# With LLM proxy
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.proxy.yml up -d
```

#### Testing
```bash
cd bytebot/packages/bytebot-agent
bun run test                         # Run unit tests
bun run test:e2e                     # Run end-to-end tests
bun run test:cov                     # Run tests with coverage
bun run test:watch                   # Run tests in watch mode
```

#### Code Quality
```bash
cd bytebot/packages/bytebot-agent
bun run lint                         # Lint TypeScript code
bun run format                       # Format code with Prettier

cd bytebot/packages/bytebot-ui
bun run lint                         # Lint UI code
```

### Gemini Connector Commands

#### Basic Usage
```bash
cd gemini-connector

# Validate setup
python3 src/gemini_connector.py --validate

# Interactive chat
python3 src/gemini_connector.py --chat

# Generate text
python3 src/gemini_connector.py --prompt "Your prompt here"

# Streaming response  
python3 src/gemini_connector.py --prompt "Write a story" --stream

# Full validation suite
python3 scripts/validate_and_test.py
```

#### Configuration
```bash
# Setup from scratch
./install.sh

# Manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Architecture Overview

### Bytebot Architecture

The Bytebot project follows a microservices architecture with four main components:

1. **bytebot-agent**: NestJS backend service that coordinates AI and desktop actions
   - Handles task creation and management
   - Integrates with multiple AI providers (Anthropic, OpenAI, Google Gemini)
   - Uses Prisma ORM with PostgreSQL
   - WebSocket support for real-time communication

2. **bytebot-ui**: Next.js frontend application  
   - Task management interface
   - Real-time desktop view via VNC
   - Built with Radix UI components and Tailwind CSS

3. **bytebot-desktop**: Ubuntu desktop environment (containerized)
   - Provides the virtual desktop where AI operates
   - Includes Firefox, VS Code, and other tools
   - Accessed via VNC/websockify

4. **bytebot-llm-proxy**: Optional LiteLLM proxy service
   - Enables integration with 100+ AI providers
   - Rate limiting and cost management

### Key Modules in bytebot-agent:
- **AgentModule**: Core agent logic and coordination
- **TasksModule**: Task creation, execution, and management  
- **MessagesModule**: Message handling and storage
- **AnthropicModule/OpenAIModule/GoogleModule**: AI provider integrations
- **PrismaModule**: Database access layer
- **ProxyModule**: LLM proxy integration

### Shared Package Architecture:
The `packages/shared` directory contains common types, utilities, and schemas used across services.

## Deployment Patterns

### Local Development
- Use individual service commands for active development
- Docker Compose for integrated testing

### Production Deployment Options

#### Docker Compose (Recommended for self-hosting):
```bash
cd bytebot
echo "ANTHROPIC_API_KEY=sk-ant-..." > docker/.env
docker-compose -f docker/docker-compose.yml up -d
```

#### Kubernetes with Helm:
```bash  
cd bytebot
helm install bytebot ./helm \
  --set agent.env.ANTHROPIC_API_KEY=sk-ant-...
```

#### Railway (One-click deployment):
Use the Railway deployment button in the README.

## Environment Configuration

### Bytebot Environment Variables
- `ANTHROPIC_API_KEY`: Anthropic Claude API key
- `OPENAI_API_KEY`: OpenAI GPT API key  
- `GEMINI_API_KEY`: Google Gemini API key
- `DATABASE_URL`: PostgreSQL connection string
- `PORT`: Service port (defaults: agent=9991, ui=9992, desktop=9990)

### Gemini Connector Environment Variables (in `gemini-connector/config/user/.env`):
- `GEMINI_API_KEY`: Your Google AI Studio API key
- `GEMINI_MODEL`: Model to use (default: gemini-pro)
- `GEMINI_TEMPERATURE`: Response temperature (default: 0.7)
- `GEMINI_MAX_TOKENS`: Maximum tokens (default: 2048)
- `GEMINI_LOG_LEVEL`: Logging level (default: INFO)

## Important Development Notes

### Bytebot Specific:
- **Build Order**: Always build `shared` package before other packages
- **Database**: Prisma migrations must be run when schema changes
- **AI Providers**: The agent supports multiple AI providers simultaneously
- **File Uploads**: Configured for 50MB payload limit
- **WebSocket**: Real-time communication between UI and agent

### Gemini Connector Specific:  
- **Async First**: Built with async/await patterns for performance
- **Error Handling**: Comprehensive retry logic and error recovery
- **Security**: Never commit API keys; use environment variables
- **Validation**: Always run validation before production use

### Cross-Project Integration:
The Gemini Connector can be integrated into Bytebot as an additional AI provider module if needed.

## Troubleshooting Common Issues

### Bytebot Issues:
```bash  
# Database connection issues
cd bytebot/packages/bytebot-agent
bun run prisma:dev

# Port conflicts
# Check ports 9990, 9991, 9992 are available

# Docker issues
docker-compose down && docker-compose up -d --build
```

### Gemini Connector Issues:
```bash
# API key issues  
python3 src/gemini_connector.py --validate

# Dependency issues
pip install --upgrade -r requirements.txt

# Permission issues
chmod +x install.sh scripts/validate_and_test.py

# Reset to clean state
python3 scripts/validate_and_test.py --rollback
```

## Testing Strategy

### Bytebot Testing:
- Unit tests in each service using Jest
- E2E tests for critical user journeys
- Integration tests for AI provider modules
- Docker-based testing environment

### Gemini Connector Testing:
- Built-in validation suite (`scripts/validate_and_test.py`)
- API connectivity tests
- Configuration validation
- Offline testing capabilities

## Security Considerations

### API Key Management:
- Use environment variables for all API keys
- Never commit secrets to version control  
- Use Kubernetes secrets in production deployments
- Rotate keys regularly

### Network Security:
- CORS properly configured in development
- Use HTTPS in production
- Proper ingress configuration for Kubernetes deployments

This architecture supports rapid development while maintaining production readiness through containerization and comprehensive testing strategies.