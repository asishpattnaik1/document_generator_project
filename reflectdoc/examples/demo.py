"""Demo script showing ReflectDoc usage."""

from reflectdoc import generate_docs, DocumentationType

def main():
    """Run a simple documentation generation demo."""
    print("🚀 ReflectDoc Demo\n")
    
    # Example 1: Generate architecture documentation
    print("Generating architecture documentation...")
    response = generate_docs(
        repo_path=".",
        doc_type="architecture",
        output_file="demo_architecture.md",
        include_diagrams=True,
        use_reflection=False,  # Disable for demo speed
        model="gpt-4-turbo-preview"
    )
    
    if response.success:
        print(f"✅ Success! Documentation saved to: {response.output_file}")
        print(f"📊 Files analyzed: {response.metadata.get('total_files_analyzed', 0)}")
        print(f"📏 Total lines: {response.metadata.get('total_lines', 0)}")
    else:
        print(f"❌ Error: {response.error}")

if __name__ == "__main__":
    main()
