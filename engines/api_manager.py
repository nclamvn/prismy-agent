import os
import streamlit as st
from typing import Dict, Optional, Any
import logging
from dataclasses import dataclass
import json

@dataclass
class APIConfig:
    """Configuration for API services"""
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    google_vision_key: Optional[str] = None
    aws_access_key: Optional[str] = None
    aws_secret_key: Optional[str] = None

class APIManager:
    """
    Centralized API key management and configuration
    Xử lý: secure key storage, validation, cost tracking
    """
    
    def __init__(self):
        """Initialize API Manager"""
        self.logger = logging.getLogger(__name__)
        self.config = APIConfig()
        self.load_api_keys()
        
        # Cost tracking
        self.usage_stats = {
            'openai_tokens': 0,
            'anthropic_tokens': 0,
            'estimated_cost': 0.0,
            'requests_made': 0
        }
    
    def load_api_keys(self):
        """Load API keys from various sources"""
        try:
            # Method 1: Environment variables (most secure)
            self.config.openai_key = os.getenv('OPENAI_API_KEY')
            self.config.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
            self.config.google_vision_key = os.getenv('GOOGLE_CLOUD_VISION_API_KEY')
            self.config.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
            self.config.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            
            # Method 2: Streamlit secrets (for deployment)
            if hasattr(st, 'secrets'):
                try:
                    if not self.config.openai_key:
                        self.config.openai_key = st.secrets.get('OPENAI_API_KEY')
                    if not self.config.anthropic_key:
                        self.config.anthropic_key = st.secrets.get('ANTHROPIC_API_KEY')
                    if not self.config.google_vision_key:
                        self.config.google_vision_key = st.secrets.get('GOOGLE_CLOUD_VISION_API_KEY')
                except Exception as e:
                    self.logger.warning(f"Could not load from Streamlit secrets: {e}")
            
            # Method 3: Streamlit session state (user input)
            if hasattr(st, 'session_state'):
                if not self.config.openai_key and 'openai_api_key' in st.session_state:
                    self.config.openai_key = st.session_state.openai_api_key
                if not self.config.anthropic_key and 'anthropic_api_key' in st.session_state:
                    self.config.anthropic_key = st.session_state.anthropic_api_key
            
            self.logger.info("API keys loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading API keys: {e}")
    
    def validate_api_key(self, service: str, api_key: str) -> Dict[str, Any]:
        """
        Validate API key for specific service
        
        Args:
            service: Service name ('openai', 'anthropic', etc.)  
            api_key: API key to validate
            
        Returns:
            Validation result with status and details
        """
        try:
            if service == 'openai':
                return self._validate_openai_key(api_key)
            elif service == 'anthropic':
                return self._validate_anthropic_key(api_key)
            elif service == 'google_vision':
                return self._validate_google_vision_key(api_key)
            else:
                return {
                    'valid': False,
                    'error': f'Unknown service: {service}'
                }
                
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def _validate_openai_key(self, api_key: str) -> Dict[str, Any]:
        """Validate OpenAI API key"""
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            
            # Test with a minimal request
            response = client.models.list()
            
            return {
                'valid': True,
                'service': 'openai',
                'models_available': [model.id for model in response.data[:5]],
                'message': 'OpenAI API key is valid'
            }
            
        except openai.AuthenticationError:
            return {
                'valid': False,
                'error': 'Invalid OpenAI API key'
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'OpenAI validation error: {str(e)}'
            }
    
    def _validate_anthropic_key(self, api_key: str) -> Dict[str, Any]:
        """Validate Anthropic API key"""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            # Test with a minimal request
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            
            return {
                'valid': True,
                'service': 'anthropic',
                'message': 'Anthropic API key is valid',
                'test_response': response.content[0].text if response.content else 'OK'
            }
            
        except anthropic.AuthenticationError:
            return {
                'valid': False,
                'error': 'Invalid Anthropic API key'
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Anthropic validation error: {str(e)}'
            }
    
    def _validate_google_vision_key(self, api_key: str) -> Dict[str, Any]:
        """Validate Google Cloud Vision API key"""
        try:
            # This would require google-cloud-vision library
            # For now, just check format
            if api_key and len(api_key) > 10:
                return {
                    'valid': True,
                    'service': 'google_vision',
                    'message': 'Google Vision API key format appears valid (full validation requires test request)'
                }
            else:
                return {
                    'valid': False,
                    'error': 'Invalid Google Vision API key format'
                }
                
        except Exception as e:
            return {
                'valid': False,
                'error': f'Google Vision validation error: {str(e)}'
            }
    
    def get_available_services(self) -> Dict[str, bool]:
        """
        Check which AI services are available
        
        Returns:
            Dictionary of service availability
        """
        services = {
            'openai': bool(self.config.openai_key),
            'anthropic': bool(self.config.anthropic_key),
            'google_vision': bool(self.config.google_vision_key),
            'aws_textract': bool(self.config.aws_access_key and self.config.aws_secret_key)
        }
        
        return services
    
    def set_api_key(self, service: str, api_key: str, validate: bool = True) -> Dict[str, Any]:
        """
        Set API key for a service
        
        Args:
            service: Service name
            api_key: API key to set
            validate: Whether to validate the key
            
        Returns:
            Result of setting the key
        """
        try:
            # Validate key if requested
            if validate:
                validation_result = self.validate_api_key(service, api_key)
                if not validation_result['valid']:
                    return validation_result
            
            # Set the key
            if service == 'openai':
                self.config.openai_key = api_key
                if hasattr(st, 'session_state'):
                    st.session_state.openai_api_key = api_key
            elif service == 'anthropic':
                self.config.anthropic_key = api_key
                if hasattr(st, 'session_state'):
                    st.session_state.anthropic_api_key = api_key
            elif service == 'google_vision':
                self.config.google_vision_key = api_key
                if hasattr(st, 'session_state'):
                    st.session_state.google_vision_api_key = api_key
            
            return {
                'success': True,
                'message': f'{service} API key set successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_api_key(self, service: str) -> Optional[str]:
        """
        Get API key for a service
        
        Args:
            service: Service name
            
        Returns:
            API key or None if not available
        """
        if service == 'openai':
            return self.config.openai_key
        elif service == 'anthropic':
            return self.config.anthropic_key
        elif service == 'google_vision':
            return self.config.google_vision_key
        elif service == 'aws_access':
            return self.config.aws_access_key
        elif service == 'aws_secret':
            return self.config.aws_secret_key
        else:
            return None
    
    def estimate_cost(self, service: str, input_tokens: int, output_tokens: int = None) -> Dict[str, Any]:
        """
        Estimate cost for API usage
        
        Args:
            service: Service name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens (estimated if None)
            
        Returns:
            Cost estimation
        """
        try:
            if output_tokens is None:
                output_tokens = int(input_tokens * 1.3)  # Estimate 30% more for output
            
            # Pricing per 1K tokens (as of 2024)
            pricing = {
                'openai': {
                    'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
                    'gpt-4': {'input': 0.03, 'output': 0.06},
                    'gpt-4-turbo': {'input': 0.01, 'output': 0.03}
                },
                'anthropic': {
                    'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
                    'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
                    'claude-3-opus': {'input': 0.015, 'output': 0.075}
                }
            }
            
            if service not in pricing:
                return {'error': f'Pricing not available for {service}'}
            
            # Use default model for service
            default_models = {
                'openai': 'gpt-3.5-turbo',
                'anthropic': 'claude-3-haiku'
            }
            
            model = default_models[service]
            rates = pricing[service][model]
            
            input_cost = (input_tokens / 1000) * rates['input']
            output_cost = (output_tokens / 1000) * rates['output']
            total_cost = input_cost + output_cost
            
            return {
                'service': service,
                'model': model,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'input_cost': input_cost,
                'output_cost': output_cost,
                'total_cost': total_cost,
                'currency': 'USD'
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def track_usage(self, service: str, tokens_used: int, cost: float = 0):
        """
        Track API usage
        
        Args:
            service: Service name
            tokens_used: Number of tokens used
            cost: Actual cost (if known)
        """
        try:
            self.usage_stats['requests_made'] += 1
            
            if service == 'openai':
                self.usage_stats['openai_tokens'] += tokens_used
            elif service == 'anthropic':
                self.usage_stats['anthropic_tokens'] += tokens_used
            
            if cost > 0:
                self.usage_stats['estimated_cost'] += cost
            
        except Exception as e:
            self.logger.error(f"Error tracking usage: {e}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return self.usage_stats.copy()
    
    def create_api_settings_ui(self):
        """
        Create Streamlit UI for API settings
        
        Returns:
            None (creates UI components)
        """
        try:
            st.subheader("🔐 API Configuration")
            
            # Check current status
            available_services = self.get_available_services()
            
            # Display current status
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if available_services['openai']:
                    st.success("✅ OpenAI Connected")
                else:
                    st.warning("⚠️ OpenAI Not Connected")
            
            with col2:
                if available_services['anthropic']:
                    st.success("✅ Anthropic Connected")
                else:
                    st.warning("⚠️ Anthropic Not Connected")
            
            with col3:
                total_connected = sum(available_services.values())
                st.info(f"📊 {total_connected}/4 Services Connected")
            
            # API Key input section
            st.markdown("---")
            st.markdown("### Enter API Keys")
            
            # OpenAI API Key
            openai_key = st.text_input(
                "OpenAI API Key",
                value=self.config.openai_key[:10] + "..." if self.config.openai_key else "",
                type="password",
                help="Get your API key from https://platform.openai.com/api-keys"
            )
            
            if st.button("Validate OpenAI Key", key="validate_openai"):
                if openai_key and not openai_key.endswith("..."):
                    result = self.set_api_key('openai', openai_key, validate=True)
                    if result.get('success') or result.get('valid'):
                        st.success("✅ OpenAI API key validated successfully!")
                    else:
                        st.error(f"❌ {result.get('error', 'Unknown error')}")
            
            # Anthropic API Key  
            anthropic_key = st.text_input(
                "Anthropic API Key",
                value=self.config.anthropic_key[:10] + "..." if self.config.anthropic_key else "",
                type="password",
                help="Get your API key from https://console.anthropic.com/"
            )
            
            if st.button("Validate Anthropic Key", key="validate_anthropic"):
                if anthropic_key and not anthropic_key.endswith("..."):
                    result = self.set_api_key('anthropic', anthropic_key, validate=True)
                    if result.get('success') or result.get('valid'):
                        st.success("✅ Anthropic API key validated successfully!")
                    else:
                        st.error(f"❌ {result.get('error', 'Unknown error')}")
            
            # Usage Statistics
            if st.checkbox("Show Usage Statistics"):
                stats = self.get_usage_stats()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Requests", stats['requests_made'])
                with col2:
                    st.metric("OpenAI Tokens", f"{stats['openai_tokens']:,}")
                with col3:
                    st.metric("Anthropic Tokens", f"{stats['anthropic_tokens']:,}")
                with col4:
                    st.metric("Estimated Cost", f"${stats['estimated_cost']:.4f}")
            
            # Help section
            with st.expander("ℹ️ How to get API Keys"):
                st.markdown("""
                **OpenAI:**
                1. Go to https://platform.openai.com/api-keys
                2. Sign up or log in
                3. Create a new API key
                4. Copy and paste it above
                
                **Anthropic (Claude):**
                1. Go to https://console.anthropic.com/
                2. Sign up or log in  
                3. Create a new API key
                4. Copy and paste it above
                
                **Cost Estimates:**
                - GPT-3.5-turbo: ~$0.002 per 1K tokens
                - GPT-4: ~$0.06 per 1K tokens  
                - Claude Haiku: ~$0.0013 per 1K tokens
                - Claude Sonnet: ~$0.018 per 1K tokens
                """)
            
        except Exception as e:
            st.error(f"Error creating API settings UI: {e}")
            self.logger.error(f"UI creation error: {e}")

# Global API manager instance
api_manager = APIManager()
