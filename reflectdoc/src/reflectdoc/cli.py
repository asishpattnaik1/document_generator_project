"""CLI interface for ReflectDoc."""

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from .core import generate_docs
from .models import DocumentationType

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """ReflectDoc - AI-powered documentation generator with reflection.
    
    Generate comprehensive documentation for your codebase using
    advanced LLM agents with self-reflection capabilities.
    """
    pass


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    default="ARCHITECTURE_DOC.md",
    help="Output file path for generated documentation"
)
@click.option(
    "--type",
    "-t",
    "doc_type",
    type=click.Choice(["architecture", "api", "troubleshooting", "full"], case_sensitive=False),
    default="full",
    help="Type of documentation to generate"
)
@click.option(
    "--no-diagrams",
    is_flag=True,
    help="Disable Mermaid diagram generation"
)
@click.option(
    "--no-reflection",
    is_flag=True,
    help="Disable reflection agent (faster but lower quality)"
)
@click.option(
    "--model",
    "-m",
    default="gpt-5-nano",
    help="OpenAI model to use (e.g., gpt-5-nano, gpt-4-turbo-preview, gpt-3.5-turbo, o1-mini)"
)
@click.option(
    "--show-content",
    is_flag=True,
    help="Display the generated documentation content in terminal"
)
def generate(path, output, doc_type, no_diagrams, no_reflection, model, show_content):
    """Generate documentation for a repository.
    
    Examples:
    
        reflectdoc generate .
        
        reflectdoc generate ./myproject --output docs.md --type architecture
        
        reflectdoc generate . --no-reflection --model gpt-5-nano
        
        reflectdoc generate . --show-content  # Display content in terminal
    """
    console.print(f"\n[bold blue]🚀 ReflectDoc Documentation Generator[/bold blue]\n")
    console.print(f"📁 Repository: [cyan]{path}[/cyan]")
    console.print(f"📄 Output: [cyan]{output}[/cyan]")
    console.print(f"📝 Type: [cyan]{doc_type}[/cyan]")
    console.print(f"🔄 Reflection: [cyan]{'disabled' if no_reflection else 'enabled'}[/cyan]")
    console.print(f"🤖 Model: [cyan]{model}[/cyan]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        task1 = progress.add_task("[yellow]Analyzing repository...", total=None)
        
        try:
            response = generate_docs(
                repo_path=path,
                doc_type=doc_type,
                output_file=output,
                include_diagrams=not no_diagrams,
                use_reflection=not no_reflection,
                model=model
            )
            
            progress.update(task1, completed=True)
            
            if response.success:
                console.print(f"\n[bold green]✅ Documentation generated successfully![/bold green]\n")
                console.print(f"📊 Files analyzed: [cyan]{response.metadata.get('total_files_analyzed', 0)}[/cyan]")
                console.print(f"📏 Total lines: [cyan]{response.metadata.get('total_lines', 0)}[/cyan]")
                console.print(f"📝 Document length: [cyan]{len(response.documentation)}[/cyan] characters")
                
                if not no_reflection:
                    iterations = response.metadata.get('total_iterations', 0)
                    console.print(f"🔄 Reflection iterations: [cyan]{iterations}[/cyan]")
                
                console.print(f"\n💾 Saved to: [bold cyan]{output}[/bold cyan]")
                
                # Display content if requested
                if show_content:
                    console.print("\n" + "="*80)
                    console.print("[bold yellow]📄 Generated Documentation Content:[/bold yellow]")
                    console.print("="*80 + "\n")
                    
                    from rich.markdown import Markdown
                    from rich.panel import Panel
                    
                    # Display as formatted markdown
                    md = Markdown(response.documentation)
                    console.print(Panel(md, title="Generated Documentation", border_style="cyan"))
                    
                    console.print("\n" + "="*80 + "\n")
            else:
                console.print(f"\n[bold red]❌ Error:[/bold red] {response.error}")
                
        except Exception as e:
            progress.update(task1, completed=True)
            console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}")
            raise click.Abort()


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def analyze(path):
    """Analyze repository structure without generating documentation.
    
    Example:
        reflectdoc analyze ./myproject
    """
    from .utils import scan_repository
    
    console.print(f"\n[bold blue]🔍 Analyzing Repository[/bold blue]\n")
    
    try:
        structure = scan_repository(path)
        
        console.print(f"[bold]Repository:[/bold] {path}")
        console.print(f"[bold]Total Files:[/bold] {len(structure['files'])}")
        console.print(f"[bold]Total Lines:[/bold] {structure['total_lines']}")
        console.print(f"[bold]Language:[/bold] python")
        
        console.print(f"\n[bold]Modules ({len(structure['modules'])}):[/bold]")
        for module in structure['modules'][:10]:
            console.print(f"  • {module}")
        if len(structure['modules']) > 10:
            console.print(f"  ... and {len(structure['modules']) - 10} more")
        
        console.print(f"\n[bold]Dependencies ({len(structure['dependencies'])}):[/bold]")
        for dep in structure['dependencies'][:15]:
            console.print(f"  • {dep}")
        if len(structure['dependencies']) > 15:
            console.print(f"  ... and {len(structure['dependencies']) - 15} more")
        
        console.print(f"\n[bold]Files ({len(structure['files'])}):[/bold]")
        for file in structure['files'][:10]:
            console.print(f"  • {file}")
        if len(structure['files']) > 10:
            console.print(f"  ... and {len(structure['files']) - 10} more")
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise click.Abort()


@cli.command()
def info():
    """Show information about ReflectDoc."""
    console.print("\n[bold blue]ReflectDoc - AI Documentation Generator[/bold blue]\n")
    console.print("Version: 0.1.0")
    console.print("A reflection-based documentation generator using LLM agents.\n")
    console.print("[bold]Features:[/bold]")
    console.print("  • Automatic code analysis and documentation generation")
    console.print("  • Self-reflection for improved quality")
    console.print("  • Multiple documentation types (architecture, API, troubleshooting)")
    console.print("  • Mermaid diagram generation")
    console.print("  • CLI and REST API interfaces")
    console.print("\n[bold]Usage:[/bold]")
    console.print("  reflectdoc generate <path>")
    console.print("  reflectdoc analyze <path>")
    console.print("\nFor more information: reflectdoc --help\n")


if __name__ == "__main__":
    cli()
