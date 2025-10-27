"""REST API interface for ReflectDoc."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import os

from .core import generate_docs, ReflectDoc
from .models import GenerationRequest, GenerationResponse, DocumentationType

app = FastAPI(
    title="ReflectDoc API",
    description="AI-powered documentation generator with reflection capabilities",
    version="0.1.0"
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "ReflectDoc API",
        "version": "0.1.0",
        "description": "Generate comprehensive documentation using AI agents with reflection",
        "endpoints": {
            "POST /generate": "Generate documentation for a repository",
            "POST /analyze": "Analyze repository structure",
            "GET /health": "Health check endpoint"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    openai_key_set = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "status": "healthy",
        "openai_configured": openai_key_set
    }


@app.post("/generate", response_model=GenerationResponse)
async def generate_documentation(request: GenerationRequest) -> GenerationResponse:
    """Generate documentation for a repository.
    
    Args:
        request: Documentation generation request with path, type, and options
        
    Returns:
        GenerationResponse with documentation and metadata
        
    Example:
        ```json
        {
            "path": "./myproject",
            "doc_type": "architecture",
            "output_file": "docs.md",
            "include_diagrams": true
        }
        ```
    """
    try:
        response = generate_docs(
            repo_path=request.path,
            doc_type=request.doc_type.value,
            output_file=request.output_file,
            include_diagrams=request.include_diagrams,
            use_reflection=True,
            model="gpt-5-nano"
        )
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/generate/fast", response_model=GenerationResponse)
async def generate_documentation_fast(request: GenerationRequest) -> GenerationResponse:
    """Generate documentation quickly without reflection (faster but lower quality).
    
    Args:
        request: Documentation generation request
        
    Returns:
        GenerationResponse with documentation
    """
    try:
        response = generate_docs(
            repo_path=request.path,
            doc_type=request.doc_type.value,
            output_file=request.output_file,
            include_diagrams=request.include_diagrams,
            use_reflection=False,  # Disable reflection for speed
            model="gpt-5-nano"
        )
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.error)
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/analyze")
async def analyze_repository(path: str = ".") -> Dict[str, Any]:
    """Analyze repository structure without generating documentation.
    
    Args:
        path: Path to repository
        
    Returns:
        Repository analysis data
        
    Example:
        ```json
        {
            "path": "./myproject"
        }
        ```
    """
    try:
        reflectdoc = ReflectDoc(use_reflection=False)
        analysis = reflectdoc.analyze_repository(path)
        
        return {
            "path": analysis.path,
            "total_files": analysis.total_files,
            "total_lines": analysis.total_lines,
            "language": analysis.language,
            "modules": analysis.modules,
            "dependencies": analysis.dependencies,
            "files": analysis.files[:50]  # Limit to first 50 files for response size
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/generate/async")
async def generate_documentation_async(
    request: GenerationRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """Start asynchronous documentation generation (for large repositories).
    
    Args:
        request: Documentation generation request
        background_tasks: FastAPI background tasks
        
    Returns:
        Task ID for checking status
    """
    import uuid
    
    task_id = str(uuid.uuid4())
    
    def generate_in_background(task_id: str, req: GenerationRequest):
        """Background task for generation."""
        # In production, you'd want to store this in Redis or a database
        result = generate_docs(
            repo_path=req.path,
            doc_type=req.doc_type.value,
            output_file=req.output_file,
            include_diagrams=req.include_diagrams,
            use_reflection=True
        )
        # Store result somewhere for retrieval
        print(f"Task {task_id} completed: {result.success}")
    
    background_tasks.add_task(generate_in_background, task_id, request)
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": "Documentation generation started in background"
    }


# CORS middleware for browser access
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
