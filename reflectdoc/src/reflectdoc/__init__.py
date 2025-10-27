"""ReflectDoc - AI-powered documentation generator with reflection."""

from .core import ReflectDoc, generate_docs
from .models import (
    DocumentationType,
    RepoAnalysis,
    GenerationRequest,
    GenerationResponse
)

__version__ = "0.1.0"
__all__ = [
    "ReflectDoc",
    "generate_docs",
    "DocumentationType",
    "RepoAnalysis",
    "GenerationRequest",
    "GenerationResponse"
]
