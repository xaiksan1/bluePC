#!/usr/bin/env python3
"""
Gemini AI Connector Script
A comprehensive tool to connect and interact with Google's Gemini AI API
instead of using web scraping methods.
"""

import os
import sys
import json
import logging
import argparse
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from pathlib import Path
import asyncio
import aiohttp
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import time
from datetime import datetime


@dataclass
class GeminiConfig:
    """Configuration class for Gemini AI connector"""
    api_key: str
    model_name: str = "gemini-pro"
    temperature: float = 0.7
    max_tokens: int = 2048
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    log_level: str = "INFO"
    log_file: Optional[str] = None
    safety_settings: Optional[Dict] = None


class GeminiConnector:
    """Main connector class for Gemini AI interactions"""
    
    def __init__(self, config: GeminiConfig):
        self.config = config
        self.logger = self._setup_logging()
        self.model = None
        self._initialize_gemini()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler if specified
        if self.config.log_file:
            file_handler = logging.FileHandler(self.config.log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        return logger
    
    def _initialize_gemini(self):
        """Initialize Gemini AI with configuration"""
        try:
            genai.configure(api_key=self.config.api_key)
            
            # Set up safety settings
            safety_settings = self.config.safety_settings or {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
            
            # Initialize the model
            generation_config = genai.types.GenerationConfig(
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_tokens,
            )
            
            self.model = genai.GenerativeModel(
                model_name=self.config.model_name,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            self.logger.info(f"Gemini AI initialized with model: {self.config.model_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini AI: {str(e)}")
            raise
    
    async def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate text using Gemini AI
        
        Args:
            prompt: The input prompt for text generation
            **kwargs: Additional generation parameters
            
        Returns:
            Dict containing the response and metadata
        """
        start_time = time.time()
        
        for attempt in range(self.config.retry_attempts):
            try:
                self.logger.info(f"Generating text (attempt {attempt + 1}/{self.config.retry_attempts})")
                
                response = await asyncio.to_thread(
                    self.model.generate_content, 
                    prompt
                )
                
                end_time = time.time()
                
                result = {
                    'text': response.text if response.text else '',
                    'prompt_feedback': response.prompt_feedback,
                    'candidates': [
                        {
                            'content': candidate.content.parts[0].text if candidate.content.parts else '',
                            'finish_reason': candidate.finish_reason,
                            'safety_ratings': [
                                {
                                    'category': rating.category,
                                    'probability': rating.probability
                                } for rating in candidate.safety_ratings
                            ]
                        } for candidate in response.candidates
                    ],
                    'usage_metadata': {
                        'prompt_token_count': getattr(response, 'usage_metadata', {}).get('prompt_token_count', 0),
                        'candidates_token_count': getattr(response, 'usage_metadata', {}).get('candidates_token_count', 0),
                        'total_token_count': getattr(response, 'usage_metadata', {}).get('total_token_count', 0),
                    },
                    'generation_time': end_time - start_time,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.logger.info(f"Text generated successfully in {result['generation_time']:.2f}s")
                return result
                
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.config.retry_attempts - 1:
                    await asyncio.sleep(self.config.retry_delay * (2 ** attempt))
                else:
                    self.logger.error(f"All retry attempts failed: {str(e)}")
                    raise
    
    async def generate_text_stream(self, prompt: str, **kwargs):
        """
        Generate text using streaming for long responses
        
        Args:
            prompt: The input prompt for text generation
            **kwargs: Additional generation parameters
            
        Yields:
            Text chunks as they are generated
        """
        try:
            self.logger.info("Starting streaming text generation")
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            self.logger.error(f"Streaming generation failed: {str(e)}")
            raise
    
    async def chat_conversation(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Conduct a chat conversation with multiple messages
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Dict containing the response and metadata
        """
        try:
            self.logger.info(f"Starting chat conversation with {len(messages)} messages")
            
            chat = self.model.start_chat()
            
            # Process conversation history
            for message in messages[:-1]:  # All but the last message
                if message['role'] == 'user':
                    chat.send_message(message['content'])
            
            # Send the final message and get response
            final_message = messages[-1]['content']
            response = await asyncio.to_thread(chat.send_message, final_message)
            
            result = {
                'text': response.text if response.text else '',
                'conversation_history': [
                    {'role': 'user' if i % 2 == 0 else 'model', 'content': msg.parts[0].text}
                    for i, msg in enumerate(chat.history)
                ],
                'timestamp': datetime.now().isoformat()
            }
            
            self.logger.info("Chat conversation completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Chat conversation failed: {str(e)}")
            raise
    
    def validate_connection(self) -> bool:
        """
        Validate the connection to Gemini AI
        
        Returns:
            True if connection is valid, False otherwise
        """
        try:
            self.logger.info("Validating Gemini AI connection")
            
            # Simple test prompt
            test_response = self.model.generate_content("Hello, are you working?")
            
            if test_response and test_response.text:
                self.logger.info("Connection validation successful")
                return True
            else:
                self.logger.error("Connection validation failed: No response text")
                return False
                
        except Exception as e:
            self.logger.error(f"Connection validation failed: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        
        Returns:
            Dict containing model information
        """
        try:
            models = genai.list_models()
            current_model_info = None
            
            for model in models:
                if model.name.endswith(self.config.model_name):
                    current_model_info = {
                        'name': model.name,
                        'display_name': model.display_name,
                        'description': model.description,
                        'input_token_limit': model.input_token_limit,
                        'output_token_limit': model.output_token_limit,
                        'supported_generation_methods': model.supported_generation_methods,
                        'temperature': model.temperature,
                        'top_p': model.top_p,
                        'top_k': model.top_k
                    }
                    break
            
            return current_model_info or {'error': 'Model information not found'}
            
        except Exception as e:
            self.logger.error(f"Failed to get model info: {str(e)}")
            return {'error': str(e)}


def load_config_from_file(config_path: str) -> GeminiConfig:
    """Load configuration from a JSON file"""
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        return GeminiConfig(**config_data)
    except Exception as e:
        print(f"Error loading config from {config_path}: {str(e)}")
        sys.exit(1)


def load_config_from_env() -> GeminiConfig:
    """Load configuration from environment variables"""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        sys.exit(1)
    
    return GeminiConfig(
        api_key=api_key,
        model_name=os.getenv('GEMINI_MODEL', 'gemini-pro'),
        temperature=float(os.getenv('GEMINI_TEMPERATURE', '0.7')),
        max_tokens=int(os.getenv('GEMINI_MAX_TOKENS', '2048')),
        timeout=int(os.getenv('GEMINI_TIMEOUT', '30')),
        log_level=os.getenv('GEMINI_LOG_LEVEL', 'INFO')
    )


async def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='Gemini AI Connector')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--prompt', '-p', help='Prompt for text generation')
    parser.add_argument('--chat', action='store_true', help='Start interactive chat mode')
    parser.add_argument('--validate', action='store_true', help='Validate connection')
    parser.add_argument('--model-info', action='store_true', help='Get model information')
    parser.add_argument('--stream', action='store_true', help='Use streaming generation')
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        config = load_config_from_file(args.config)
    else:
        config = load_config_from_env()
    
    # Initialize connector
    connector = GeminiConnector(config)
    
    try:
        if args.validate:
            success = connector.validate_connection()
            print(f"Connection validation: {'SUCCESS' if success else 'FAILED'}")
            
        elif args.model_info:
            info = connector.get_model_info()
            print(json.dumps(info, indent=2))
            
        elif args.chat:
            print("Starting interactive chat mode. Type 'quit' to exit.")
            while True:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                try:
                    response = await connector.generate_text(user_input)
                    print(f"\nGemini: {response['text']}")
                except Exception as e:
                    print(f"Error: {str(e)}")
                    
        elif args.prompt:
            if args.stream:
                print("Streaming response:")
                async for chunk in connector.generate_text_stream(args.prompt):
                    print(chunk, end='', flush=True)
                print()  # New line at the end
            else:
                response = await connector.generate_text(args.prompt)
                print(f"Response: {response['text']}")
                print(f"Tokens used: {response['usage_metadata']['total_token_count']}")
                print(f"Generation time: {response['generation_time']:.2f}s")
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())