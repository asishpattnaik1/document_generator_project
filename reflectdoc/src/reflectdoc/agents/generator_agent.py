"""Generator Agent - Creates initial documentation drafts."""

from typing import Dict, Any, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()

console = Console()


class GeneratorAgent:
    """Agent responsible for generating initial documentation."""
    
    def __init__(self, model: str = "gpt-5-nano"):
        """Initialize the generator agent.
        
        Args:
            model: OpenAI model to use for generation
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        # Determine if this is a newer model that uses max_completion_tokens
        self.use_completion_tokens = "gpt-5" in model or "o1" in model
        
        console.print(f"[bold green]✓ Generator Agent[/bold green] initialized with model: [cyan]{model}[/cyan]")
    
    def generate_architecture_doc(
        self, 
        repo_structure: str, 
        include_diagrams: bool = True
    ) -> str:
        """Generate architecture documentation.
        
        Args:
            repo_structure: Formatted repository structure
            include_diagrams: Whether to include Mermaid diagrams
            
        Returns:
            Generated documentation
        """
        console.print("\n[bold green]📝 Generator Agent:[/bold green] Creating architecture documentation...")
        
        diagram_instruction = ""
        if include_diagrams:
            diagram_instruction = """
Include Mermaid diagrams where appropriate:
- System architecture diagram
- Component relationships
- Data flow diagrams
"""
        
        prompt = f"""You are a technical documentation expert. Generate comprehensive architecture documentation for the following codebase.

**CRITICAL RULES:**
1. ONLY document classes, methods, and attributes that are explicitly listed below
2. DO NOT invent or assume any APIs, methods, or features not shown
3. Use EXACT method signatures provided (arguments and return types)
4. Use EXACT attribute names and types as shown
5. If unsure about something, describe it generically rather than inventing specifics

{repo_structure}

Create documentation with the following sections:
1. **Overview**: High-level summary of the system based on actual code
2. **Architecture**: Core architectural patterns visible in the code structure
3. **Components**: Key modules and their responsibilities (use actual class/function names)
4. **Data Flow**: How data moves through the system based on method calls
5. **Dependencies**: External libraries listed in imports
{diagram_instruction}
6. **Key Design Patterns**: Patterns evident in the code structure
7. **Extension Points**: How to extend the system based on current architecture

**IMPORTANT**: 
- Reference actual method signatures like `method_name(arg1: str, arg2: int) -> bool`
- Reference actual class attributes like `name: str`, `email: str`
- If a method or attribute is not listed above, DO NOT mention it
- Be specific with actual names, not generic descriptions

Format the output in Markdown with clear headings and structure.
"""
        
        # Prepare kwargs based on model type
        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert technical writer specializing in software architecture documentation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        }
        
        # Add appropriate token limit parameter and temperature
        if self.use_completion_tokens:
            kwargs["max_completion_tokens"] = 8000
            kwargs["temperature"] = 1
        else:
            kwargs["max_tokens"] = 8000
            kwargs["temperature"] = 0.7
        
        console.print("  [dim green]→ Sending request to OpenAI...[/dim green]")
        
        try:
            response = self.client.chat.completions.create(**kwargs)
            
            # Get response content
            content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            
            console.print(f"  [dim]→ API Response - Finish Reason: {finish_reason}[/dim]")
            
            # Debug: Show token usage if available
            if hasattr(response, 'usage') and response.usage:
                console.print(f"  [dim]→ Token Usage: prompt={response.usage.prompt_tokens}, completion={response.usage.completion_tokens}[/dim]")
            
            # Handle case where content might be None or empty
            if not content or len(content.strip()) < 50:
                console.print(f"  [bold yellow]⚠ Warning: OpenAI returned empty/minimal content.[/bold yellow]")
                console.print(f"  [yellow]→ This may indicate:[/yellow]")
                console.print(f"  [yellow]  1. Model '{self.model}' may not exist or has restrictions[/yellow]")
                console.print(f"  [yellow]  2. Token limits may be too low for this model[/yellow]")
                console.print(f"  [yellow]  3. Input prompt may be too large[/yellow]")
                console.print(f"  [yellow]→ Suggestion: Try with --model gpt-4-turbo-preview or gpt-3.5-turbo[/yellow]")
                content = "# Documentation\n\nNo content generated. Please try a different model."
            
            console.print(f"  [bold green]✓ Generated {len(content)} characters[/bold green] of architecture documentation")
            
            # Display the actual generated content
            console.print("\n[bold green]" + "="*80 + "[/bold green]")
            console.print("[bold green]📄 Generator Agent Output:[/bold green]")
            console.print("[bold green]" + "="*80 + "[/bold green]")
            from rich.markdown import Markdown
            from rich.panel import Panel
            md = Markdown(content)
            console.print(Panel(md, title="[green]Architecture Documentation (Initial Draft)[/green]", border_style="green"))
            console.print("[bold green]" + "="*80 + "[/bold green]\n")
            
            return content
            
        except Exception as e:
            console.print(f"  [bold red]✗ Error calling OpenAI API:[/bold red] {str(e)}")
            console.print(f"  [yellow]→ Model: {self.model}[/yellow]")
            console.print(f"  [yellow]→ Try using a different model with --model flag[/yellow]")
            raise
    
    def generate_api_doc(self, repo_structure: str) -> str:
        """Generate API documentation.
        
        Args:
            repo_structure: Formatted repository structure
            
        Returns:
            Generated API documentation
        """
        console.print("\n[bold green]📝 Generator Agent:[/bold green] Creating API documentation...")
        
        prompt = f"""You are an API documentation expert. Generate comprehensive API documentation for the following codebase.

{repo_structure}

Create documentation with the following sections:
1. **API Overview**: Purpose and scope
2. **Endpoints**: List all API endpoints with methods and descriptions
3. **Request/Response Examples**: Sample requests and responses
4. **Authentication**: Authentication requirements
5. **Error Handling**: Common errors and status codes
6. **Rate Limits**: Any rate limiting policies

Format the output in Markdown with clear examples.
"""
        
        # Prepare kwargs based on model type
        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert API documentation writer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        }
        
        # Add appropriate token limit parameter and temperature
        if self.use_completion_tokens:
            kwargs["max_completion_tokens"] = 8000
            kwargs["temperature"] = 1
        else:
            kwargs["max_tokens"] = 8000
            kwargs["temperature"] = 0.7
        
        console.print("  [dim green]→ Sending request to OpenAI...[/dim green]")
        response = self.client.chat.completions.create(**kwargs)
        
        # Debug: Check the full response structure
        content = response.choices[0].message.content
        
        # Handle case where content might be None or empty
        if not content:
            console.print(f"  [yellow]⚠ Warning: OpenAI returned empty content. Response status: {response.choices[0].finish_reason}[/yellow]")
            content = "# API Documentation\n\nNo content generated."
        
        console.print(f"  [bold green]✓ Generated {len(content)} characters[/bold green] of API documentation")
        
        return content
    
    def generate_troubleshooting_doc(self, repo_structure: str) -> str:
        """Generate troubleshooting documentation.
        
        Args:
            repo_structure: Formatted repository structure
            
        Returns:
            Generated troubleshooting documentation
        """
        console.print("\n[bold green]📝 Generator Agent:[/bold green] Creating troubleshooting documentation...")
        
        prompt = f"""You are a troubleshooting expert. Generate a troubleshooting guide for the following codebase.

{repo_structure}

Create documentation with the following sections:
1. **Common Issues**: Most frequent problems users encounter
2. **Troubleshooting Matrix**: Table format with Issue | Cause | Resolution
3. **Debug Guide**: How to debug the system
4. **Configuration Issues**: Common configuration problems
5. **Performance Issues**: Performance-related problems
6. **FAQ**: Frequently asked questions

Format the output in Markdown with tables where appropriate.
"""
        
        # Prepare kwargs based on model type
        kwargs = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in technical troubleshooting and support documentation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        }
        
        # Add appropriate token limit parameter and temperature
        if self.use_completion_tokens:
            kwargs["max_completion_tokens"] = 8000
            kwargs["temperature"] = 1
        else:
            kwargs["max_tokens"] = 8000
            kwargs["temperature"] = 0.7
        
        console.print("  [dim green]→ Sending request to OpenAI...[/dim green]")
        response = self.client.chat.completions.create(**kwargs)
        
        # Debug: Check the full response structure
        content = response.choices[0].message.content
        
        # Handle case where content might be None or empty
        if not content:
            console.print(f"  [yellow]⚠ Warning: OpenAI returned empty content. Response status: {response.choices[0].finish_reason}[/yellow]")
            content = "# Troubleshooting Guide\n\nNo content generated."
        
        console.print(f"  [bold green]✓ Generated {len(content)} characters[/bold green] of troubleshooting documentation")
        
        return content
    
    def generate_full_documentation(
        self, 
        repo_structure: str, 
        include_diagrams: bool = True
    ) -> str:
        """Generate complete documentation.
        
        Args:
            repo_structure: Formatted repository structure
            include_diagrams: Whether to include diagrams
            
        Returns:
            Complete documentation
        """
        console.print("\n[bold green]📝 Generator Agent:[/bold green] Generating full documentation suite...")
        
        arch_doc = self.generate_architecture_doc(repo_structure, include_diagrams)
        api_doc = self.generate_api_doc(repo_structure)
        trouble_doc = self.generate_troubleshooting_doc(repo_structure)
        
        full_doc = f"""# Complete Documentation

{arch_doc}

---

{api_doc}

---

{trouble_doc}
"""
        console.print(f"\n[bold green]✓ Full documentation suite completed[/bold green] ([cyan]{len(full_doc)}[/cyan] characters total)")
        return full_doc
