# Gemini AI Connector - Quick Reference Guide

## 🚀 Installation & Setup Commands

### One-Line Installation
```bash
cd /home/ichigo/workspace_code/bluePC/gemini-connector
chmod +x install.sh && ./install.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup directories
mkdir -p logs config/user

# Copy configuration templates
cp config/.env.template config/user/.env
cp config/config.template.json config/user/config.json
```

## 🔑 Configuration Setup

### 1. Get Your API Key
- Visit: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the generated key

### 2. Configure Environment Variables
Edit `config/user/.env`:
```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-pro
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048
GEMINI_LOG_LEVEL=INFO
```

## 📋 Essential Commands

### Validation & Testing
```bash
# Basic connection test
python3 src/gemini_connector.py --validate

# Full validation suite
python3 scripts/validate_and_test.py

# Offline validation (skip API tests)
python3 scripts/validate_and_test.py --offline

# Rollback changes
python3 scripts/validate_and_test.py --rollback
```

### Basic Usage
```bash
# Simple text generation
python3 src/gemini_connector.py --prompt "Explain quantum computing"

# Interactive chat mode
python3 src/gemini_connector.py --chat

# Streaming response
python3 src/gemini_connector.py --prompt "Write a story" --stream

# Get model information
python3 src/gemini_connector.py --model-info

# Use custom config file
python3 src/gemini_connector.py --config config/user/config.json --prompt "Hello"
```

## 🐍 Python API Usage

### Quick Start
```python
import asyncio
from src.gemini_connector import GeminiConnector, load_config_from_env

async def main():
    config = load_config_from_env()
    connector = GeminiConnector(config)
    
    response = await connector.generate_text("Hello Gemini!")
    print(response['text'])

asyncio.run(main())
```

### Advanced Usage
```python
import asyncio
from src.gemini_connector import GeminiConnector, GeminiConfig

async def advanced_example():
    # Custom configuration
    config = GeminiConfig(
        api_key="your_key_here",
        model_name="gemini-pro",
        temperature=0.9,
        max_tokens=4096
    )
    
    connector = GeminiConnector(config)
    
    # Streaming response
    async for chunk in connector.generate_text_stream("Write a poem"):
        print(chunk, end='', flush=True)
    
    # Chat conversation
    messages = [
        {"role": "user", "content": "Hello!"},
        {"role": "user", "content": "What's the weather like?"}
    ]
    response = await connector.chat_conversation(messages)
    print(response['text'])

asyncio.run(advanced_example())
```

## 🔧 Troubleshooting Commands

### Common Issues & Solutions

#### API Key Issues
```bash
# Check if environment variable is set
echo $GEMINI_API_KEY

# Validate connection
python3 src/gemini_connector.py --validate
```

#### Permission Issues
```bash
# Make scripts executable
chmod +x src/gemini_connector.py
chmod +x install.sh
chmod +x scripts/validate_and_test.py
```

#### Python Dependencies
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check specific package
python3 -c "import google.generativeai; print('OK')"
```

#### Log Debugging
```bash
# Enable debug logging
export GEMINI_LOG_LEVEL=DEBUG
python3 src/gemini_connector.py --validate

# Check logs
tail -f logs/gemini_connector.log
```

## 📁 Project Structure Reference

```
gemini-connector/
├── src/
│   └── gemini_connector.py        # Main connector script
├── config/
│   ├── .env.template             # Environment config template
│   ├── config.template.json      # JSON config template
│   └── user/                     # User configurations (create this)
│       ├── .env                  # Your actual config
│       └── config.json           # Your JSON config
├── docs/
│   └── README.md                 # Full documentation
├── scripts/
│   └── validate_and_test.py      # Validation & testing script
├── logs/                         # Log files (auto-created)
├── backups/                      # Automatic backups (auto-created)
├── tests/                        # Test files
├── requirements.txt              # Python dependencies
├── install.sh                    # Installation script
└── QUICK_REFERENCE.md           # This file
```

## 🚨 Emergency Commands

### If Something Goes Wrong
```bash
# Rollback all changes
python3 scripts/validate_and_test.py --rollback

# Reset to clean state
git checkout -- .
git clean -fd

# Reinstall from scratch
rm -rf .venv
./install.sh
```

### Backup & Recovery
```bash
# Manual backup
cp -r config/user/ config/backup_$(date +%Y%m%d_%H%M%S)/

# Restore from backup
cp -r config/backup_YYYYMMDD_HHMMSS/ config/user/
```

## 💡 Pro Tips

### Performance Optimization
- Use `gemini-1.5-flash` for faster responses
- Use streaming for long content
- Batch multiple requests with `asyncio.gather()`

### Security Best Practices
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor usage and costs

### Development Workflow
```bash
# 1. Make changes
# 2. Validate
python3 scripts/validate_and_test.py

# 3. Test functionality
python3 src/gemini_connector.py --chat

# 4. Commit changes
git add .
git commit -m "Your changes"

# 5. Push to remote (if configured)
git push origin main
```

## 🔗 Useful Links & Resources

- **Gemini API Documentation**: https://ai.google.dev/docs
- **API Key Management**: https://makersuite.google.com/app/apikey
- **Python SDK**: https://github.com/google/generative-ai-python
- **Rate Limits**: https://ai.google.dev/docs/rate_limits
- **Safety Settings**: https://ai.google.dev/docs/safety_setting_gemini

## 📞 Support & Issues

### Getting Help
1. Check the troubleshooting section above
2. Review the full documentation in `docs/README.md`
3. Run validation: `python3 scripts/validate_and_test.py`
4. Check logs in the `logs/` directory

### Reporting Issues
Include the following information:
- Output of `python3 --version`
- Contents of validation report
- Error messages and stack traces
- Steps to reproduce the issue

---

## 📝 Quick Copy-Paste Commands

**Complete Setup:**
```bash
cd /home/ichigo/workspace_code/bluePC/gemini-connector
chmod +x install.sh && ./install.sh
# Edit config/user/.env with your API key
python3 src/gemini_connector.py --validate
```

**Basic Test:**
```bash
python3 src/gemini_connector.py --prompt "Hello, are you working?"
```

**Interactive Chat:**
```bash
python3 src/gemini_connector.py --chat
```

**Full Validation:**
```bash
python3 scripts/validate_and_test.py
```

Save this file for quick reference! 🚀