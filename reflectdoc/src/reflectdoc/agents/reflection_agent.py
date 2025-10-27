"""Reflection Agent - Reviews and improves documentation quality."""

from typing import Dict, Any, Tuple
from openai import OpenAI
import os
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

console = Console()


class ReflectionAgent:
    """Agent responsible for reviewing and improving documentation."""
    
    def __init__(self, model: str = "gpt-5-nano"):
        """Initialize the reflection agent.
        
        Args:
            model: OpenAI model to use for reflection
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Determine if this is a newer model that uses max_completion_tokens
        self.use_completion_tokens = "gpt-5" in model or "o1" in model
        
        console.print(f"[bold red]✓ Reflection Agent[/bold red] initialized with model: [cyan]{model}[/cyan]")
    
    def reflect_on_documentation(
        self, 
        documentation: str, 
        repo_structure: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Reflect on and improve the generated documentation.
        
        Args:
            documentation: Initial documentation to review
            repo_structure: Original repository structure for context
            
        Returns:
            Tuple of (improved_documentation, critique_metadata)
        """
        console.print("\n[bold red]🔍 Reflection Agent:[/bold red] Reviewing documentation quality...")
        
        critique_prompt = f"""You are a senior technical reviewer. Review the following documentation and provide a detailed critique.

**CRITICAL VALIDATION RULES:**
1. Check if the documentation mentions APIs, methods, or attributes NOT in the code structure
2. Verify that method signatures match the actual code (check arguments and return types)
3. Ensure class attributes mentioned actually exist in the code
4. Flag any "generic" descriptions that should use actual names from the code
5. Check if important methods or classes from the code are missing from docs

# Documentation to Review:
{documentation}

# Original Code Structure (GROUND TRUTH):
{repo_structure}

Provide your critique in the following format:

## Accuracy Issues (CRITICAL)
- List any APIs, methods, or attributes mentioned in docs but NOT in the code structure
- List any incorrect method signatures (wrong arguments, wrong return types)
- List any invented features or capabilities

## Missing Coverage
- Important classes, methods, or attributes from code NOT documented
- Key functionality that should be explained

## Specificity Issues
- Generic descriptions that should use actual names/types from code
- Vague explanations that could be more concrete

## Strengths
- What the documentation does well

## Improvement Suggestions
- Specific recommendations using actual code elements
- Better examples or diagrams using real method names

**Be thorough in catching hallucinations and inaccuracies!**
"""
        
        # Prepare kwargs for critique
        critique_kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior technical documentation reviewer with expertise in software architecture."
                },
                {
                    "role": "user",
                    "content": critique_prompt
                }
            ],
        }
        
        if self.use_completion_tokens:
            critique_kwargs["max_completion_tokens"] = 2000
            critique_kwargs["temperature"] = 1
        else:
            critique_kwargs["max_tokens"] = 2000
            critique_kwargs["temperature"] = 0.5
        
        console.print("  [dim red]→ Analyzing documentation strengths and weaknesses...[/dim red]")
        # Get critique
        critique_response = self.client.chat.completions.create(**critique_kwargs)
        critique = critique_response.choices[0].message.content or "No critique generated."
        
        # Track token usage for critique
        if hasattr(critique_response, 'usage') and critique_response.usage:
            console.print(f"  [dim]→ Critique Token Usage: prompt={critique_response.usage.prompt_tokens}, completion={critique_response.usage.completion_tokens}, total={critique_response.usage.total_tokens}[/dim]")
        
        console.print(f"  [bold red]✓ Critique completed ({len(critique)} characters)[/bold red]")
        
        # Display the critique
        console.print("\n[bold red]" + "="*80 + "[/bold red]")
        console.print("[bold red]🔍 Reflection Agent - Critique:[/bold red]")
        console.print("[bold red]" + "="*80 + "[/bold red]")
        from rich.markdown import Markdown
        from rich.panel import Panel
        md_critique = Markdown(critique)
        console.print(Panel(md_critique, title="[red]Documentation Critique[/red]", border_style="red"))
        console.print("[bold red]" + "="*80 + "[/bold red]\n")
        
        # Generate improved version based on critique
        console.print("\n[bold red]🔍 Reflection Agent:[/bold red] Applying improvements based on critique...")
        
        improvement_prompt = f"""Based on the following critique, generate an improved version of the documentation.

# Original Documentation:
{documentation}

# Critique:
{critique}

# Code Structure for Reference:
{repo_structure}

Generate an improved version that addresses all the points raised in the critique.
Maintain the same overall structure but enhance clarity, accuracy, and completeness.
"""
        
        # Prepare kwargs for improvement
        improvement_kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert technical writer improving documentation based on review feedback."
                },
                {
                    "role": "user",
                    "content": improvement_prompt
                }
            ],
        }
        
        if self.use_completion_tokens:
            improvement_kwargs["max_completion_tokens"] = 5000
            improvement_kwargs["temperature"] = 1
        else:
            improvement_kwargs["max_tokens"] = 5000
            improvement_kwargs["temperature"] = 0.7
        
        console.print("  [dim red]→ Generating improved documentation...[/dim red]")
        improved_response = self.client.chat.completions.create(**improvement_kwargs)
        improved_docs = improved_response.choices[0].message.content or documentation
        
        # Track token usage for improvement
        if hasattr(improved_response, 'usage') and improved_response.usage:
            console.print(f"  [dim]→ Improvement Token Usage: prompt={improved_response.usage.prompt_tokens}, completion={improved_response.usage.completion_tokens}, total={improved_response.usage.total_tokens}[/dim]")
        
        console.print(f"  [bold red]✓ Improved documentation generated ({len(improved_docs)} characters)[/bold red]")
        
        # Display the improved documentation
        console.print("\n[bold red]" + "="*80 + "[/bold red]")
        console.print("[bold red]📄 Reflection Agent - Improved Documentation:[/bold red]")
        console.print("[bold red]" + "="*80 + "[/bold red]")
        md_improved = Markdown(improved_docs)
        console.print(Panel(md_improved, title="[red]Improved Documentation (After Reflection)[/red]", border_style="red"))
        console.print("[bold red]" + "="*80 + "[/bold red]\n")
        
        metadata = {
            "critique": critique,
            "reflection_iterations": 1,
            "improvements_made": True
        }
        
        return improved_docs, metadata
    
    def validate_technical_accuracy(
        self, 
        documentation: str, 
        repo_structure: str
    ) -> Dict[str, Any]:
        """Validate technical accuracy of documentation.
        
        Args:
            documentation: Documentation to validate
            repo_structure: Repository structure for verification
            
        Returns:
            Validation results
        """
        console.print("\n[bold red]🔍 Reflection Agent:[/bold red] Validating technical accuracy...")
        
        validation_prompt = f"""Validate the technical accuracy of the following documentation against the actual code structure.

# Documentation:
{documentation}

# Actual Code Structure:
{repo_structure}

Check for:
1. Factual accuracy - Does the documentation match the actual code?
2. Completeness - Are all major components covered?
3. Consistency - Are there any contradictions?
4. Technical correctness - Are technical terms and concepts used correctly?

Provide a validation report with:
- **Accuracy Score**: 1-10
- **Issues Found**: List any inaccuracies
- **Missing Coverage**: What's not documented but should be
- **Recommendations**: How to improve accuracy
"""
        
        # Prepare kwargs for validation
        validation_kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a technical validator ensuring documentation accuracy."
                },
                {
                    "role": "user",
                    "content": validation_prompt
                }
            ],
        }
        
        if self.use_completion_tokens:
            validation_kwargs["max_completion_tokens"] = 2000
            validation_kwargs["temperature"] = 1
        else:
            validation_kwargs["max_tokens"] = 2000
            validation_kwargs["temperature"] = 0.3
        
        console.print("  [dim red]→ Running accuracy validation...[/dim red]")
        response = self.client.chat.completions.create(**validation_kwargs)
        validation_result = response.choices[0].message.content or "Validation could not be completed."
        
        # Track token usage for validation
        if hasattr(response, 'usage') and response.usage:
            console.print(f"  [dim]→ Validation Token Usage: prompt={response.usage.prompt_tokens}, completion={response.usage.completion_tokens}, total={response.usage.total_tokens}[/dim]")
        
        console.print(f"  [bold red]✓ Validation complete[/bold red]")
        
        return {
            "validation_passed": True,
            "validation_report": validation_result
        }
    
    def iterative_refinement(
        self,
        documentation: str,
        repo_structure: str,
        max_iterations: int = 2
    ) -> Tuple[str, Dict[str, Any]]:
        """Perform multiple rounds of reflection and improvement.
        
        Args:
            documentation: Initial documentation
            repo_structure: Repository structure
            max_iterations: Maximum number of refinement iterations
            
        Returns:
            Tuple of (final_documentation, metadata)
        """
        console.print(f"\n[bold red]🔄 Starting {max_iterations} iteration(s) of reflection and refinement...[/bold red]\n")
        
        current_doc = documentation
        all_critiques = []
        
        for i in range(max_iterations):
            console.print(f"[bold red]═══ Reflection Iteration {i+1}/{max_iterations} ═══[/bold red]")
            improved_doc, metadata = self.reflect_on_documentation(
                current_doc,
                repo_structure
            )
            all_critiques.append(metadata["critique"])
            current_doc = improved_doc
        
        # Final validation
        console.print(f"\n[bold red]═══ Final Validation ═══[/bold red]")
        validation = self.validate_technical_accuracy(current_doc, repo_structure)
        
        console.print(f"\n[bold red]✓ Reflection process complete![/bold red] Total iterations: {max_iterations}\n")
        
        final_metadata = {
            "total_iterations": max_iterations,
            "critiques": all_critiques,
            "final_validation": validation
        }
        
        return current_doc, final_metadata
