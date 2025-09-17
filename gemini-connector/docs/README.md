# Gemini AI Connector Documentation

A comprehensive Python tool to connect and interact with Google's Gemini AI API instead of using web scraping methods.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Overview

The Gemini AI Connector provides a robust, production-ready interface to Google's Gemini AI models. It replaces web scraping approaches with direct API integration, offering better reliability, performance, and functionality.

### Key Benefits

- ✅ **Direct API Integration**: No web scraping required
- ✅ **Async Support**: High-performance asynchronous operations
- ✅ **Comprehensive Error Handling**: Robust retry mechanisms
- ✅ **Flexible Configuration**: Environment variables or JSON config
- ✅ **Multiple Interaction Modes**: Single prompts, streaming, and chat conversations
- ✅ **Security**: Secure API key management
- ✅ **Logging**: Comprehensive logging and monitoring

## Features

### Core Functionality
- **Text Generation**: Single-shot text generation with customizable parameters
- **Streaming Generation**: Real-time streaming responses for long content
- **Chat Conversations**: Multi-turn conversations with context preservation
- **Connection Validation**: Built-in connection testing
- **Model Information**: Query available models and their capabilities

### Advanced Features
- **Retry Logic**: Exponential backoff for failed requests
- **Safety Settings**: Configurable content filtering
- **Token Monitoring**: Track usage and costs
- **Async Processing**: Non-blocking operations for better performance
- **Comprehensive Logging**: Detailed logs for debugging and monitoring

## Installation

### Quick Install

```bash
# Clone or download the project
cd gemini-connector

# Run the installation script
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs config/user

# Copy configuration templates
cp config/.env.template config/user/.env
cp config/config.template.json config/user/config.json
```

## Configuration

### Option 1: Environment Variables (Recommended)

Edit `config/user/.env`:

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-pro
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048
GEMINI_LOG_LEVEL=INFO
```

### Option 2: JSON Configuration

Edit `config/user/config.json`:

```json
{
  "api_key": "your_actual_api_key_here",
  "model_name": "gemini-pro",
  "temperature": 0.7,
  "max_tokens": 2048,
  "log_level": "INFO"
}
```

### Getting Your API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key
4. Add it to your configuration file

### Available Models

- `gemini-pro`: General-purpose text generation
- `gemini-pro-vision`: Text + image input support
- `gemini-1.5-pro`: Latest version with enhanced capabilities
- `gemini-1.5-flash`: Faster, lighter version

## Usage

### Command Line Interface

#### Basic Text Generation
```bash
python3 src/gemini_connector.py --prompt "Explain quantum computing in simple terms"
```

#### Interactive Chat Mode
```bash
python3 src/gemini_connector.py --chat
```

#### Streaming Response
```bash
python3 src/gemini_connector.py --prompt "Write a long story about AI" --stream
```

#### Connection Validation
```bash
python3 src/gemini_connector.py --validate
```

#### Model Information
```bash
python3 src/gemini_connector.py --model-info
```

#### Using Configuration File
```bash
python3 src/gemini_connector.py --config config/user/config.json --prompt "Hello Gemini"
```

### Python API Usage

```python
import asyncio
from src.gemini_connector import GeminiConnector, GeminiConfig

async def example_usage():
    # Create configuration
    config = GeminiConfig(
        api_key="your_api_key_here",
        model_name="gemini-pro",
        temperature=0.7
    )
    
    # Initialize connector
    connector = GeminiConnector(config)
    
    # Generate text
    response = await connector.generate_text("Explain machine learning")
    print(response['text'])
    
    # Start a chat conversation
    messages = [
        {"role": "user", "content": "Hello!"},
        {"role": "user", "content": "What can you help me with?"}
    ]
    chat_response = await connector.chat_conversation(messages)
    print(chat_response['text'])

# Run the example
asyncio.run(example_usage())
```

## API Reference

### GeminiConfig

Configuration class for the Gemini AI connector.

```python
@dataclass
class GeminiConfig:
    api_key: str                    # Required: Your Gemini API key
    model_name: str = "gemini-pro"  # Model to use
    temperature: float = 0.7        # Creativity level (0.0-1.0)
    max_tokens: int = 2048         # Maximum response length
    timeout: int = 30              # Request timeout in seconds
    retry_attempts: int = 3        # Number of retry attempts
    retry_delay: float = 1.0       # Base delay between retries
    log_level: str = "INFO"        # Logging level
    log_file: Optional[str] = None # Log file path
```

### GeminiConnector

Main connector class for interacting with Gemini AI.

#### Methods

##### `async generate_text(prompt: str, **kwargs) -> Dict[str, Any]`

Generate text from a single prompt.

**Parameters:**
- `prompt`: The input text prompt
- `**kwargs`: Additional generation parameters

**Returns:**
- Dictionary containing response text, metadata, and usage statistics

##### `async generate_text_stream(prompt: str, **kwargs)`

Generate text using streaming for real-time responses.

**Parameters:**
- `prompt`: The input text prompt
- `**kwargs`: Additional generation parameters

**Yields:**
- Text chunks as they are generated

##### `async chat_conversation(messages: List[Dict[str, str]]) -> Dict[str, Any]`

Conduct a multi-turn conversation.

**Parameters:**
- `messages`: List of message dictionaries with 'role' and 'content'

**Returns:**
- Dictionary containing response and conversation history

##### `validate_connection() -> bool`

Test the connection to Gemini AI.

**Returns:**
- `True` if connection is valid, `False` otherwise

##### `get_model_info() -> Dict[str, Any]`

Get information about the current model.

**Returns:**
- Dictionary containing model capabilities and limits

## Examples

### Example 1: Simple Text Generation

```python
import asyncio
from src.gemini_connector import GeminiConnector, load_config_from_env

async def simple_generation():
    config = load_config_from_env()
    connector = GeminiConnector(config)
    
    prompt = "Write a Python function to calculate fibonacci numbers"
    response = await connector.generate_text(prompt)
    
    print("Generated Code:")
    print(response['text'])
    print(f"Tokens used: {response['usage_metadata']['total_token_count']}")

asyncio.run(simple_generation())
```

### Example 2: Interactive Chat Bot

```python
import asyncio
from src.gemini_connector import GeminiConnector, load_config_from_env

async def chatbot():
    config = load_config_from_env()
    connector = GeminiConnector(config)
    
    conversation_history = []
    
    print("Chatbot started. Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
            
        conversation_history.append({"role": "user", "content": user_input})
        
        response = await connector.chat_conversation(conversation_history)
        bot_response = response['text']
        
        print(f"Bot: {bot_response}")
        
        conversation_history.append({"role": "assistant", "content": bot_response})

asyncio.run(chatbot())
```

### Example 3: Streaming Response

```python
import asyncio
from src.gemini_connector import GeminiConnector, load_config_from_env

async def streaming_example():
    config = load_config_from_env()
    connector = GeminiConnector(config)
    
    prompt = "Write a detailed explanation of how neural networks work"
    
    print("Streaming response:")
    async for chunk in connector.generate_text_stream(prompt):
        print(chunk, end='', flush=True)
    print()  # New line at the end

asyncio.run(streaming_example())
```

### Example 4: Batch Processing

```python
import asyncio
from src.gemini_connector import GeminiConnector, load_config_from_env

async def batch_processing():
    config = load_config_from_env()
    connector = GeminiConnector(config)
    
    prompts = [
        "Summarize the benefits of renewable energy",
        "Explain the basics of cryptocurrency",
        "Describe the process of photosynthesis"
    ]
    
    tasks = [connector.generate_text(prompt) for prompt in prompts]
    responses = await asyncio.gather(*tasks)
    
    for i, response in enumerate(responses):
        print(f"Response {i+1}:")
        print(response['text'])
        print("-" * 50)

asyncio.run(batch_processing())
```

## Best Practices

### Security
- **Never hardcode API keys** in your source code
- Use environment variables or secure configuration files
- Rotate API keys regularly
- Implement proper access controls

### Performance
- Use streaming for long responses
- Implement proper error handling and retries
- Monitor token usage to control costs
- Use batch processing for multiple requests

### Error Handling
- Always wrap API calls in try-catch blocks
- Implement exponential backoff for retries
- Log errors for debugging and monitoring
- Provide meaningful error messages to users

### Configuration
- Use separate configurations for development and production
- Validate configuration before starting
- Document all configuration options
- Use reasonable defaults

## Troubleshooting

### Common Issues

#### Authentication Errors
```
Error: 403 Forbidden
```
**Solution:** Check your API key is valid and has proper permissions.

#### Rate Limiting
```
Error: 429 Too Many Requests
```
**Solution:** Implement proper retry logic or reduce request frequency.

#### Model Not Found
```
Error: Model not found
```
**Solution:** Verify the model name in your configuration.

#### Connection Timeouts
```
Error: Connection timeout
```
**Solution:** Increase the timeout value or check your network connection.

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
config = GeminiConfig(
    api_key="your_key",
    log_level="DEBUG"
)
```

### Validation Script

Use the validation script to test your setup:

```bash
python3 src/gemini_connector.py --validate
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd gemini-connector

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
trunk check
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the examples and API documentation

## Changelog

### v1.0.0
- Initial release
- Basic text generation functionality
- Streaming support
- Chat conversations
- Configuration management
- Comprehensive error handling