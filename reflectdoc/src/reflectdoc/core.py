"""Core orchestrator for ReflectDoc - coordinates Generator and Reflection agents."""

from typing import Optional
from pathlib import Path
from rich.console import Console

from .agents import GeneratorAgent, ReflectionAgent
from .models import RepoAnalysis, GenerationResponse, DocumentationType
from .utils import scan_repository, format_structure_for_llm, extract_detailed_structure, format_detailed_structure_for_llm

console = Console()

class ReflectDoc:
    """Main orchestrator for documentation generation with reflection."""
    
    def __init__(
        self, 
        use_reflection: bool = True,
        model: str = "gpt-5-nano",
        max_iterations: int = 2
    ):
        """Initialize ReflectDoc.
        
        Args:
            use_reflection: Whether to use reflection agent for quality improvement
            model: OpenAI model to use
            max_iterations: Maximum reflection iterations
        """
        self.use_reflection = use_reflection
        self.model = model
        self.max_iterations = max_iterations
        
        # Initialize agents (only if we need them)
        self.generator: Optional[GeneratorAgent] = None
        self.reflector: Optional[ReflectionAgent] = None
    
    def _ensure_agents(self):
        """Lazy initialization of agents."""
        if self.generator is None:
            self.generator = GeneratorAgent(model=self.model)
        if self.use_reflection and self.reflector is None:
            self.reflector = ReflectionAgent(model=self.model)
    
    def analyze_repository(self, repo_path: str) -> RepoAnalysis:
        """Analyze repository structure.
        
        Args:
            repo_path: Path to repository
            
        Returns:
            RepoAnalysis object with repository structure
        """
        structure = scan_repository(repo_path)
        
        return RepoAnalysis(
            path=repo_path,
            files=structure["files"],
            modules=structure["modules"],
            dependencies=structure["dependencies"],
            structure=structure["file_details"],
            language="python",
            total_files=len(structure["files"]),
            total_lines=structure["total_lines"]
        )
    
    def generate_documentation(
        self,
        repo_path: str,
        doc_type: str = "full",
        include_diagrams: bool = True
    ) -> tuple[str, dict]:
        """Generate documentation with optional reflection.
        
        Args:
            repo_path: Path to repository
            doc_type: Type of documentation (architecture/api/troubleshooting/full)
            include_diagrams: Whether to include Mermaid diagrams
            
        Returns:
            Tuple of (documentation_string, metadata_dict)
        """
        self._ensure_agents()
        
        # Ensure generator is initialized
        if self.generator is None:
            raise RuntimeError("Generator agent failed to initialize")
        
        # Step 1: Analyze repository
        analysis = self.analyze_repository(repo_path)
        
        # Get DETAILED structure with actual signatures (GROUND TRUTH)
        console.print("[dim]→ Extracting detailed code structure...[/dim]")
        detailed_structure = extract_detailed_structure(repo_path)
        repo_structure = format_detailed_structure_for_llm(detailed_structure)
        
        # Step 2: Generate initial documentation
        if doc_type == "architecture":
            docs = self.generator.generate_architecture_doc(repo_structure, include_diagrams)
        elif doc_type == "api":
            docs = self.generator.generate_api_doc(repo_structure)
        elif doc_type == "troubleshooting":
            docs = self.generator.generate_troubleshooting_doc(repo_structure)
        else:  # full
            docs = self.generator.generate_full_documentation(repo_structure, include_diagrams)
        
        # Validate that we actually generated content
        if not docs or len(docs.strip()) < 50:
            console.print(f"[yellow]⚠ Warning: Generator produced minimal content ({len(docs)} chars). Skipping reflection.[/yellow]")
            metadata = {
                "total_files_analyzed": analysis.total_files,
                "total_lines": analysis.total_lines,
                "doc_type": doc_type,
                "reflection_used": False,
                "warning": "Insufficient content generated"
            }
            return docs, metadata
        
        metadata = {
            "total_files_analyzed": analysis.total_files,
            "total_lines": analysis.total_lines,
            "doc_type": doc_type,
            "reflection_used": self.use_reflection
        }
        
        # Step 3: Apply reflection if enabled
        if self.use_reflection and self.reflector is not None:
            improved_docs, reflection_metadata = self.reflector.iterative_refinement(
                docs,
                repo_structure,
                max_iterations=self.max_iterations
            )
            metadata.update(reflection_metadata)
            return improved_docs, metadata
        
        return docs, metadata


def generate_docs(
    repo_path: str = ".",
    doc_type: str = "full",
    output_file: Optional[str] = None,
    include_diagrams: bool = True,
    use_reflection: bool = True,
    model: str = "gpt-5-nano",
    max_iterations: int = 2
) -> GenerationResponse:
    """Convenience function to generate documentation.
    
    Args:
        repo_path: Path to repository to analyze
        doc_type: Type of documentation (architecture/api/troubleshooting/full)
        output_file: Optional output file path
        include_diagrams: Whether to include Mermaid diagrams
        use_reflection: Whether to use reflection agent
        model: OpenAI model to use
        max_iterations: Maximum reflection iterations
        
    Returns:
        GenerationResponse with documentation and metadata
        
    Example:
        >>> response = generate_docs("./myproject", doc_type="architecture")
        >>> if response.success:
        ...     print(f"Docs saved to: {response.output_file}")
    """
    try:
        # Initialize ReflectDoc
        reflectdoc = ReflectDoc(
            use_reflection=use_reflection,
            model=model,
            max_iterations=max_iterations
        )
        
        # Generate documentation
        documentation, metadata = reflectdoc.generate_documentation(
            repo_path=repo_path,
            doc_type=doc_type,
            include_diagrams=include_diagrams
        )
        
        # Save to file if specified
        if output_file:
            output_path = Path(output_file)
            output_path.write_text(documentation, encoding='utf-8')
        else:
            # Default output file based on doc type
            output_file = f"{doc_type.upper()}_DOCS.md"
            Path(output_file).write_text(documentation, encoding='utf-8')
        
        return GenerationResponse(
            success=True,
            documentation=documentation,
            output_file=output_file,
            metadata=metadata
        )
        
    except Exception as e:
        return GenerationResponse(
            success=False,
            documentation="",
            error=str(e),
            metadata={}
        )
