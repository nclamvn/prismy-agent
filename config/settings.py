# config/settings.py
"""
SDIP Configuration Settings
Centralized configuration management for all components
"""

import os
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class APIConfig:
    """API configuration settings"""
    claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    claude_model: str = "claude-3-sonnet-20240229"
    openai_model: str = "gpt-4-turbo-preview"
    max_retries: int = 3
    timeout: int = 30

@dataclass
class ChunkingConfig:
    """Semantic Chunking Engine™ configuration"""
    max_chunk_size: int = 2000        # Maximum characters per chunk
    min_chunk_size: int = 100         # Minimum characters per chunk
    overlap_size: int = 200           # Overlap between chunks
    confidence_threshold: float = 0.7  # Minimum semantic confidence
    enable_cross_references: bool = True
    preserve_code_blocks: bool = True
    preserve_tables: bool = True

class SDIPConfig:
    """Main SDIP configuration class"""
    
    def __init__(self):
        self.api = APIConfig()
        self.chunking = ChunkingConfig()
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration settings"""
        if not self.api.claude_api_key:
            print("WARNING: CLAUDE_API_KEY not found in environment")
        
        if self.chunking.max_chunk_size <= self.chunking.min_chunk_size:
            raise ValueError("max_chunk_size must be greater than min_chunk_size")

# Global configuration instance
config = SDIPConfig()

# Supported languages mapping
SUPPORTED_LANGUAGES = {
    "en": "English",
    "vi": "Vietnamese", 
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "zh": "Chinese",
    "ja": "Japanese",
}
