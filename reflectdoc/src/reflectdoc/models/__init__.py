"""Data models for ReflectDoc."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class DocumentationType(str, Enum):
    """Types of documentation that can be generated."""
    ARCHITECTURE = "architecture"
    API = "api"
    TROUBLESHOOTING = "troubleshooting"
    FULL = "full"


class RepoAnalysis(BaseModel):
    """Structure of analyzed repository."""
    path: str
    files: List[str] = Field(default_factory=list)
    modules: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    structure: Dict[str, Any] = Field(default_factory=dict)
    language: str = "python"
    total_files: int = 0
    total_lines: int = 0


class GenerationRequest(BaseModel):
    """Request model for documentation generation."""
    path: str = Field(default=".", description="Path to repository")
    doc_type: DocumentationType = Field(
        default=DocumentationType.FULL,
        description="Type of documentation to generate"
    )
    output_file: Optional[str] = Field(
        default=None,
        description="Output file path"
    )
    include_diagrams: bool = Field(
        default=True,
        description="Include Mermaid diagrams"
    )


class GenerationResponse(BaseModel):
    """Response model for documentation generation."""
    success: bool
    documentation: str
    output_file: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
