# Gemini AI Connector

A comprehensive Python tool to connect and interact with Google's Gemini AI API instead of using web scraping methods.

## 🚀 Quick Start

1. **Install and Setup**
   ```bash
   chmod +x install.sh && ./install.sh
   ```

2. **Configure API Key**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Edit `config/user/.env` and add your API key

3. **Test Connection**
   ```bash
   python3 src/gemini_connector.py --validate
   ```

4. **Start Using**
   ```bash
   python3 src/gemini_connector.py --chat
   ```

## 📖 Documentation

- **[Quick Reference](QUICK_REFERENCE.md)** - Commands and usage examples
- **[Full Documentation](docs/README.md)** - Comprehensive guide
- **[API Reference](docs/README.md#api-reference)** - Python API documentation

## ✨ Features

- ✅ Direct Gemini API integration (no web scraping)
- ✅ Async support for high performance
- ✅ Streaming responses for long content
- ✅ Interactive chat mode
- ✅ Comprehensive error handling and retries
- ✅ Flexible configuration options
- ✅ Security best practices
- ✅ Validation and rollback capabilities

## 🛠️ Quick Commands

```bash
# Basic text generation
python3 src/gemini_connector.py --prompt "Explain AI"

# Interactive chat
python3 src/gemini_connector.py --chat

# Streaming response
python3 src/gemini_connector.py --prompt "Write a story" --stream

# Validate setup
python3 scripts/validate_and_test.py
```

## 📁 Project Structure

```
gemini-connector/
├── src/gemini_connector.py      # Main connector
├── config/                      # Configuration templates
├── docs/README.md              # Full documentation  
├── scripts/validate_and_test.py # Validation suite
├── QUICK_REFERENCE.md          # Command reference
└── install.sh                 # Installation script
```

## 🆘 Need Help?

1. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for common commands
2. Review [docs/README.md](docs/README.md) for detailed documentation
3. Run validation: `python3 scripts/validate_and_test.py`

## 📄 License

This project is licensed under the MIT License.

---

**🚀 Get started in seconds - replace web scraping with reliable API access!**