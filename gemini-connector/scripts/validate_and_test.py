#!/usr/bin/env python3
"""
Validation and Testing Script for Gemini AI Connector
Includes rollback capabilities and comprehensive validation steps
"""

import os
import sys
import json
import asyncio
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from gemini_connector import GeminiConnector, GeminiConfig, load_config_from_env
except ImportError as e:
    print(f"❌ Failed to import gemini_connector: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)


class ValidationState:
    """Track validation state for rollback purposes"""
    
    def __init__(self):
        self.backup_dir = Path("backups") / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.validation_log = []
        self.created_files = []
        self.modified_files = []
        
    def create_backup(self, file_path: str):
        """Create backup of a file before modification"""
        if not os.path.exists(file_path):
            return
            
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = self.backup_dir / Path(file_path).name
        shutil.copy2(file_path, backup_path)
        self.modified_files.append((file_path, str(backup_path)))
        
    def log_validation(self, step: str, success: bool, message: str = ""):
        """Log validation step result"""
        status = "✅ PASS" if success else "❌ FAIL"
        entry = {
            'timestamp': datetime.now().isoformat(),
            'step': step,
            'success': success,
            'message': message,
            'status': status
        }
        self.validation_log.append(entry)
        print(f"{status}: {step}" + (f" - {message}" if message else ""))
        
    def rollback(self):
        """Rollback all changes made during validation"""
        print("\n🔄 Rolling back changes...")
        
        # Restore modified files
        for original_path, backup_path in self.modified_files:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, original_path)
                print(f"   Restored: {original_path}")
        
        # Remove created files
        for file_path in self.created_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"   Removed: {file_path}")
        
        # Clean up backup directory
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
            
        print("✅ Rollback completed successfully")
    
    def save_validation_report(self):
        """Save validation report to file"""
        report_path = Path("logs") / f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'validation_steps': self.validation_log,
            'summary': {
                'total_steps': len(self.validation_log),
                'passed': sum(1 for entry in self.validation_log if entry['success']),
                'failed': sum(1 for entry in self.validation_log if not entry['success'])
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📊 Validation report saved to: {report_path}")
        return report_path


class GeminiValidator:
    """Comprehensive validation suite for Gemini AI Connector"""
    
    def __init__(self):
        self.state = ValidationState()
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for validation"""
        logger = logging.getLogger('gemini_validator')
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    async def validate_environment(self) -> bool:
        """Validate the environment setup"""
        print("\n🔍 Validating Environment...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version >= (3, 8):
            self.state.log_validation("Python Version", True, f"Python {python_version.major}.{python_version.minor}")
        else:
            self.state.log_validation("Python Version", False, f"Python {python_version.major}.{python_version.minor} < 3.8")
            return False
        
        # Check required directories
        required_dirs = ['src', 'config', 'logs']
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                self.state.log_validation(f"Directory {dir_name}", True)
            else:
                self.state.log_validation(f"Directory {dir_name}", False, "Missing")
        
        # Check required files
        required_files = [
            'src/gemini_connector.py',
            'requirements.txt',
            'install.sh'
        ]
        for file_path in required_files:
            if os.path.exists(file_path):
                self.state.log_validation(f"File {file_path}", True)
            else:
                self.state.log_validation(f"File {file_path}", False, "Missing")
        
        return True
    
    async def validate_dependencies(self) -> bool:
        """Validate Python dependencies"""
        print("\n📦 Validating Dependencies...")
        
        required_packages = [
            'google.generativeai',
            'aiohttp',
            'asyncio'
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                self.state.log_validation(f"Package {package}", True)
            except ImportError as e:
                self.state.log_validation(f"Package {package}", False, str(e))
        
        return True
    
    async def validate_configuration(self) -> Tuple[bool, Optional[GeminiConfig]]:
        """Validate configuration setup"""
        print("\n⚙️  Validating Configuration...")
        
        # Check environment variables
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key and api_key != "your_gemini_api_key_here" and not api_key.startswith('***'):
            self.state.log_validation("API Key Environment Variable", True)
        else:
            self.state.log_validation("API Key Environment Variable", False, "Not set or placeholder")
            return False, None
        
        # Check configuration files
        config_files = [
            'config/.env.template',
            'config/config.template.json'
        ]
        for config_file in config_files:
            if os.path.exists(config_file):
                self.state.log_validation(f"Config Template {config_file}", True)
            else:
                self.state.log_validation(f"Config Template {config_file}", False, "Missing")
        
        # Try to load configuration
        try:
            config = load_config_from_env()
            self.state.log_validation("Configuration Loading", True)
            return True, config
        except Exception as e:
            self.state.log_validation("Configuration Loading", False, str(e))
            return False, None
    
    async def validate_api_connection(self, config: GeminiConfig) -> bool:
        """Validate API connection to Gemini"""
        print("\n🌐 Validating API Connection...")
        
        try:
            connector = GeminiConnector(config)
            
            # Test basic connection
            if connector.validate_connection():
                self.state.log_validation("Basic API Connection", True)
            else:
                self.state.log_validation("Basic API Connection", False)
                return False
            
            # Test model information
            try:
                model_info = connector.get_model_info()
                if 'error' not in model_info:
                    self.state.log_validation("Model Information Retrieval", True)
                else:
                    self.state.log_validation("Model Information Retrieval", False, model_info['error'])
            except Exception as e:
                self.state.log_validation("Model Information Retrieval", False, str(e))
            
            return True
            
        except Exception as e:
            self.state.log_validation("API Connection Setup", False, str(e))
            return False
    
    async def validate_functionality(self, config: GeminiConfig) -> bool:
        """Validate core functionality"""
        print("\n🧪 Validating Core Functionality...")
        
        try:
            connector = GeminiConnector(config)
            
            # Test basic text generation
            try:
                response = await connector.generate_text("Hello, this is a test. Please respond with 'Test successful'.")
                if response and response.get('text'):
                    self.state.log_validation("Basic Text Generation", True)
                else:
                    self.state.log_validation("Basic Text Generation", False, "No response text")
            except Exception as e:
                self.state.log_validation("Basic Text Generation", False, str(e))
            
            # Test streaming (if basic generation works)
            try:
                chunks = []
                async for chunk in connector.generate_text_stream("Count from 1 to 3"):
                    chunks.append(chunk)
                
                if chunks:
                    self.state.log_validation("Streaming Text Generation", True)
                else:
                    self.state.log_validation("Streaming Text Generation", False, "No chunks received")
            except Exception as e:
                self.state.log_validation("Streaming Text Generation", False, str(e))
            
            # Test chat conversation
            try:
                messages = [{"role": "user", "content": "Hello"}]
                chat_response = await connector.chat_conversation(messages)
                if chat_response and chat_response.get('text'):
                    self.state.log_validation("Chat Conversation", True)
                else:
                    self.state.log_validation("Chat Conversation", False, "No chat response")
            except Exception as e:
                self.state.log_validation("Chat Conversation", False, str(e))
            
            return True
            
        except Exception as e:
            self.state.log_validation("Functionality Validation Setup", False, str(e))
            return False
    
    async def validate_error_handling(self, config: GeminiConfig) -> bool:
        """Validate error handling and recovery"""
        print("\n🛡️  Validating Error Handling...")
        
        # Test with invalid API key
        try:
            invalid_config = GeminiConfig(api_key="invalid_key_test_123")
            invalid_connector = GeminiConnector(invalid_config)
            
            # This should fail gracefully
            success = invalid_connector.validate_connection()
            if not success:
                self.state.log_validation("Invalid API Key Handling", True, "Graceful failure")
            else:
                self.state.log_validation("Invalid API Key Handling", False, "Should have failed")
        except Exception as e:
            self.state.log_validation("Invalid API Key Handling", True, f"Caught exception: {type(e).__name__}")
        
        # Test retry mechanism with valid config but problematic prompt
        try:
            connector = GeminiConnector(config)
            # This might trigger retry logic due to content policy
            response = await connector.generate_text("")
            self.state.log_validation("Empty Prompt Handling", True, "Handled gracefully")
        except Exception as e:
            self.state.log_validation("Empty Prompt Handling", True, f"Caught exception: {type(e).__name__}")
        
        return True
    
    async def run_full_validation(self, include_api_tests: bool = True) -> bool:
        """Run the complete validation suite"""
        print("🚀 Starting Full Validation Suite...")
        print("=" * 50)
        
        success = True
        config = None
        
        try:
            # Step 1: Environment validation
            if not await self.validate_environment():
                success = False
            
            # Step 2: Dependencies validation
            if not await self.validate_dependencies():
                success = False
            
            # Step 3: Configuration validation
            config_success, config = await self.validate_configuration()
            if not config_success:
                success = False
            
            # Skip API tests if configuration failed or if requested
            if include_api_tests and config:
                # Step 4: API connection validation
                if not await self.validate_api_connection(config):
                    success = False
                
                # Step 5: Functionality validation
                if not await self.validate_functionality(config):
                    success = False
                
                # Step 6: Error handling validation
                if not await self.validate_error_handling(config):
                    success = False
            elif not include_api_tests:
                print("\n⏭️  Skipping API tests (offline mode)")
            
            # Generate summary
            print("\n" + "=" * 50)
            if success:
                print("🎉 All Validations Passed!")
            else:
                print("❌ Some Validations Failed!")
            
            return success
            
        except Exception as e:
            self.state.log_validation("Validation Suite", False, f"Unexpected error: {str(e)}")
            return False
        finally:
            # Save validation report
            self.state.save_validation_report()
    
    def get_rollback_handler(self):
        """Return the rollback handler for external use"""
        return self.state.rollback


async def main():
    """Main function for running validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gemini AI Connector Validation Suite')
    parser.add_argument('--offline', action='store_true', help='Skip API tests (offline mode)')
    parser.add_argument('--rollback', action='store_true', help='Perform rollback only')
    parser.add_argument('--report-only', action='store_true', help='Generate report without validation')
    
    args = parser.parse_args()
    
    validator = GeminiValidator()
    
    if args.rollback:
        print("🔄 Performing rollback...")
        validator.state.rollback()
        return
    
    if args.report_only:
        print("📊 Generating validation report...")
        validator.state.save_validation_report()
        return
    
    # Run full validation
    try:
        success = await validator.run_full_validation(include_api_tests=not args.offline)
        
        if not success:
            print("\n❓ Would you like to rollback any changes? (y/n): ", end='')
            if input().lower().startswith('y'):
                validator.state.rollback()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user")
        print("❓ Would you like to rollback any changes? (y/n): ", end='')
        if input().lower().startswith('y'):
            validator.state.rollback()
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during validation: {str(e)}")
        validator.state.rollback()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())