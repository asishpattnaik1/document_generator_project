"""LLM Client Factory - Unified interface for OpenAI and Azure OpenAI."""

from typing import Union, Literal, Dict, Any
from openai import OpenAI, AzureOpenAI
import os
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

console = Console()

# Type alias for provider
LLMProvider = Literal["openai", "azure"]


class LLMClientFactory:
    """Factory for creating LLM clients (OpenAI or Azure OpenAI)."""
    
    @staticmethod
    def create_client(
        provider: LLMProvider = "openai",
        model: str = "gpt-5-nano"
    ) -> Union[OpenAI, AzureOpenAI]:
        """Create an LLM client based on the provider.
        
        Args:
            provider: LLM provider ("openai" or "azure")
            model: Model name (used for Azure deployment mapping)
            
        Returns:
            OpenAI or AzureOpenAI client instance
            
        Raises:
            ValueError: If required environment variables are missing
        """
        if provider == "azure":
            return LLMClientFactory._create_azure_client(model)
        else:
            return LLMClientFactory._create_openai_client()
    
    @staticmethod
    def _create_openai_client() -> OpenAI:
        """Create an OpenAI client.
        
        Returns:
            OpenAI client instance
            
        Raises:
            ValueError: If OPENAI_API_KEY is not set
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file or environment."
            )
        
        console.print("[dim]→ Using OpenAI API[/dim]")
        return OpenAI(api_key=api_key)
    
    @staticmethod
    def _create_azure_client(model: str) -> AzureOpenAI:
        """Create an Azure OpenAI client.
        
        Args:
            model: Model name (used to determine deployment)
            
        Returns:
            AzureOpenAI client instance
            
        Raises:
            ValueError: If required Azure environment variables are not set
        """
        # Required Azure OpenAI environment variables
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        if not azure_endpoint:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT not found in environment variables. "
                "Please set it in your .env file (e.g., https://your-resource.openai.azure.com/)"
            )
        
        if not api_key:
            raise ValueError(
                "AZURE_OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file."
            )
        
        console.print(f"[dim]→ Using Azure OpenAI API: {azure_endpoint}[/dim]")
        
        return AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
    
    @staticmethod
    def get_model_config(model: str, provider: LLMProvider = "openai") -> Dict[str, Any]:
        """Get model configuration including deployment name for Azure.
        
        Args:
            model: Model name
            provider: LLM provider
            
        Returns:
            Dictionary with model configuration
        """
        # Determine if model uses max_completion_tokens
        use_completion_tokens = "gpt-5" in model or "o1" in model
        
        if provider == "azure":
            # For Azure, we need to map model names to deployment names
            # The deployment name can be customized per Azure resource
            deployment_name = os.getenv(f"AZURE_OPENAI_DEPLOYMENT_{model.upper().replace('-', '_')}")
            
            if not deployment_name:
                # Fallback: use generic deployment name env vars or the model name itself
                deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT") or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or model
            
            return {
                "model": deployment_name,
                "use_completion_tokens": use_completion_tokens,
                "provider": "azure"
            }
        else:
            return {
                "model": model,
                "use_completion_tokens": use_completion_tokens,
                "provider": "openai"
            }
    
    @staticmethod
    def validate_configuration(provider: LLMProvider = "openai") -> bool:
        """Validate that required environment variables are set.
        
        Args:
            provider: LLM provider to validate
            
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        try:
            if provider == "azure":
                LLMClientFactory._create_azure_client("gpt-4")
            else:
                LLMClientFactory._create_openai_client()
            return True
        except ValueError:
            raise
