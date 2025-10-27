"""Utility functions for ReflectDoc."""

from pathlib import Path
from typing import List, Dict, Any
import ast
import json
import inspect


def analyze_python_file(file_path: Path) -> Dict[str, Any]:
    """Analyze a Python file and extract its structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        classes = []
        functions = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                class_attributes = []
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        # Extract method signature
                        args = [arg.arg for arg in item.args.args]
                        returns = ast.unparse(item.returns) if item.returns else None
                        methods.append({
                            "name": item.name,
                            "args": args,
                            "returns": returns,
                            "line": item.lineno,
                            "docstring": ast.get_docstring(item)
                        })
                    elif isinstance(item, ast.AnnAssign):
                        # Extract class attributes with type hints
                        if isinstance(item.target, ast.Name):
                            class_attributes.append({
                                "name": item.target.id,
                                "type": ast.unparse(item.annotation) if item.annotation else None
                            })
                
                classes.append({
                    "name": node.name,
                    "methods": methods,
                    "attributes": class_attributes,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node),
                    "bases": [ast.unparse(base) for base in node.bases]
                })
                
            elif isinstance(node, ast.FunctionDef) and not isinstance(node, ast.AsyncFunctionDef):
                if node.col_offset == 0:  # Top-level function
                    args = [arg.arg for arg in node.args.args]
                    returns = ast.unparse(node.returns) if node.returns else None
                    functions.append({
                        "name": node.name,
                        "args": args,
                        "returns": returns,
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node)
                    })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                else:
                    imports.append(node.module if node.module else "")
        
        return {
            "classes": classes,
            "functions": functions,
            "imports": list(set(imports)),
            "lines": len(content.splitlines())
        }
    except Exception as e:
        return {"error": str(e), "lines": 0}


def scan_repository(repo_path: str) -> Dict[str, Any]:
    """Scan a repository and extract its structure."""
    path = Path(repo_path)
    
    if not path.exists():
        raise ValueError(f"Path {repo_path} does not exist")
    
    python_files = list(path.rglob("*.py"))
    
    structure = {
        "files": [],
        "modules": [],
        "dependencies": set(),
        "total_lines": 0,
        "file_details": {}
    }
    
    for py_file in python_files:
        rel_path = str(py_file.relative_to(path))
        structure["files"].append(rel_path)
        
        analysis = analyze_python_file(py_file)
        structure["file_details"][rel_path] = analysis
        structure["total_lines"] += analysis.get("lines", 0)
        
        # Extract dependencies from imports
        for imp in analysis.get("imports", []):
            if imp and not imp.startswith("."):
                structure["dependencies"].add(imp.split(".")[0])
        
        # Extract module names
        if "__init__.py" in rel_path:
            module_path = rel_path.replace("/__init__.py", "").replace("/", ".")
            structure["modules"].append(module_path)
    
    structure["dependencies"] = sorted(list(structure["dependencies"]))
    
    return structure


def extract_requirements(repo_path: str) -> List[str]:
    """Extract requirements from requirements.txt or pyproject.toml."""
    path = Path(repo_path)
    requirements = []
    
    # Check requirements.txt
    req_file = path / "requirements.txt"
    if req_file.exists():
        with open(req_file, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    # Check pyproject.toml
    pyproject_file = path / "pyproject.toml"
    if pyproject_file.exists():
        try:
            # Try using tomllib (Python 3.11+) first, then fall back to tomli
            try:
                import tomllib
                with open(pyproject_file, 'rb') as f:
                    data = tomllib.load(f)
                    deps = data.get("project", {}).get("dependencies", [])
                    requirements.extend(deps)
            except ImportError:
                # Python < 3.11, try tomli if available
                try:
                    import tomli  # type: ignore
                    with open(pyproject_file, 'rb') as f:
                        data = tomli.load(f)
                        deps = data.get("project", {}).get("dependencies", [])
                        requirements.extend(deps)
                except ImportError:
                    # Neither available, skip TOML parsing
                    pass
        except Exception:
            pass  # If TOML parsing fails, continue without it
    
    return requirements


def format_structure_for_llm(structure: Dict[str, Any]) -> str:
    """Format repository structure for LLM consumption."""
    output = []
    output.append(f"## Repository Structure")
    output.append(f"Total Files: {len(structure['files'])}")
    output.append(f"Total Lines: {structure['total_lines']}")
    output.append(f"\n## Modules")
    output.extend(structure['modules'])
    output.append(f"\n## Dependencies")
    output.extend(structure['dependencies'])
    output.append(f"\n## File Details")
    
    for file_path, details in structure.get('file_details', {}).items():
        if 'error' not in details:
            output.append(f"\n### {file_path}")
            output.append(f"Classes: {', '.join([c['name'] for c in details['classes']])}")
            output.append(f"Functions: {', '.join([f['name'] for f in details['functions']])}")
    
    return "\n".join(output)


def extract_detailed_structure(repo_path: str) -> Dict[str, Any]:
    """Extract detailed code structure with actual signatures and docstrings.
    
    This provides GROUND TRUTH for documentation validation.
    """
    path = Path(repo_path)
    python_files = list(path.rglob("*.py"))
    
    detailed_structure = {
        "files": [],
        "modules": {},
        "dependencies": set(),
        "total_lines": 0,
    }
    
    for py_file in python_files:
        rel_path = str(py_file.relative_to(path))
        analysis = analyze_python_file(py_file)
        
        detailed_structure["files"].append(rel_path)
        detailed_structure["modules"][rel_path] = analysis
        detailed_structure["total_lines"] += analysis.get("lines", 0)
        
        # Extract dependencies
        for imp in analysis.get("imports", []):
            if imp and not imp.startswith("."):
                detailed_structure["dependencies"].add(imp.split(".")[0])
    
    detailed_structure["dependencies"] = sorted(list(detailed_structure["dependencies"]))
    
    return detailed_structure


def format_detailed_structure_for_llm(structure: Dict[str, Any]) -> str:
    """Format detailed structure with ACTUAL code signatures for LLM.
    
    This prevents hallucinations by providing exact API details.
    """
    output = []
    output.append("# CODE STRUCTURE (GROUND TRUTH - DO NOT INVENT APIS)")
    output.append(f"Total Files: {len(structure['files'])}")
    output.append(f"Total Lines: {structure['total_lines']}")
    output.append("")
    
    output.append("## IMPORTANT: Only document what exists below. DO NOT invent methods or attributes.")
    output.append("")
    
    for file_path, details in structure.get("modules", {}).items():
        if "error" in details:
            continue
            
        output.append(f"\n### File: {file_path}")
        output.append(f"Lines: {details.get('lines', 0)}")
        
        # Document imports
        if details.get("imports"):
            output.append(f"\n**Imports**: {', '.join(details['imports'][:10])}")
        
        # Document classes with full details
        for cls in details.get("classes", []):
            output.append(f"\n**Class: {cls['name']}**")
            if cls.get("bases"):
                output.append(f"  - Inherits from: {', '.join(cls['bases'])}")
            if cls.get("docstring"):
                output.append(f"  - Docstring: {cls['docstring'][:100]}...")
            
            # Document attributes
            if cls.get("attributes"):
                output.append("  - Attributes:")
                for attr in cls["attributes"]:
                    output.append(f"    - {attr['name']}: {attr.get('type', 'Any')}")
            
            # Document methods with signatures
            if cls.get("methods"):
                output.append("  - Methods:")
                for method in cls["methods"]:
                    args_str = ", ".join(method["args"])
                    returns_str = f" -> {method['returns']}" if method['returns'] else ""
                    output.append(f"    - {method['name']}({args_str}){returns_str}")
                    if method.get("docstring"):
                        output.append(f"      Doc: {method['docstring'][:80]}...")
        
        # Document top-level functions
        for func in details.get("functions", []):
            args_str = ", ".join(func["args"])
            returns_str = f" -> {func['returns']}" if func['returns'] else ""
            output.append(f"\n**Function: {func['name']}({args_str}){returns_str}**")
            if func.get("docstring"):
                output.append(f"  - {func['docstring'][:100]}...")
    
    return "\n".join(output)
