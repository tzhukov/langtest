#!/usr/bin/env python3
"""Extract code files from generated markdown documentation."""

import os
import re
import sys
from pathlib import Path


def extract_code_blocks(markdown_content):
    """Extract code blocks from markdown content."""
    # Pattern to match code blocks with optional file names
    pattern = r'```(\w+)?\s*(?:// (.+?)\s*)?\n(.*?)```'
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    
    code_blocks = []
    for match in matches:
        language = match[0] if match[0] else 'text'
        filename = match[1] if match[1] else None
        content = match[2]
        
        code_blocks.append({
            'language': language,
            'filename': filename,
            'content': content
        })
    
    return code_blocks


def create_project_structure():
    """Create the basic project directory structure."""
    directories = [
        'backend',
        'frontend/src',
        'frontend/public', 
        'k8s',
        'scripts'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")


def extract_and_create_files(markdown_file, output_dir="."):
    """Extract code from markdown and create actual files."""
    
    print(f"🔍 Reading {markdown_file}...")
    
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {markdown_file}")
        return
    
    # Extract code blocks
    code_blocks = extract_code_blocks(content)
    
    if not code_blocks:
        print(f"⚠️  No code blocks found in {markdown_file}")
        return
    
    print(f"📝 Found {len(code_blocks)} code blocks")
    
    # Define file mappings based on content and context
    file_mappings = {
        # Go files
        'main.go': ('backend/main.go', 'go'),
        'go.mod': ('backend/go.mod', 'go'),
        'go.sum': ('backend/go.sum', 'go'),
        
        # React files  
        'App.js': ('frontend/src/App.js', 'jsx'),
        'App.tsx': ('frontend/src/App.tsx', 'tsx'),
        'index.js': ('frontend/src/index.js', 'jsx'),
        'index.tsx': ('frontend/src/index.tsx', 'tsx'),
        'package.json': ('frontend/package.json', 'json'),
        'index.html': ('frontend/public/index.html', 'html'),
        
        # Docker files
        'Dockerfile': ('backend/Dockerfile', 'dockerfile'),
        'Dockerfile.frontend': ('frontend/Dockerfile', 'dockerfile'),
        'docker-compose.yml': ('docker-compose.yml', 'yaml'),
        
        # Tilt files
        'Tiltfile': ('Tiltfile', 'python'),
        
        # Kubernetes files
        'deployment.yaml': ('k8s/deployment.yaml', 'yaml'),
        'service.yaml': ('k8s/service.yaml', 'yaml'),
        'configmap.yaml': ('k8s/configmap.yaml', 'yaml'),
        
        # Scripts
        'Makefile': ('Makefile', 'makefile'),
        'setup.sh': ('scripts/setup.sh', 'bash'),
        'start.sh': ('scripts/start.sh', 'bash'),
    }
    
    created_files = []
    
    for block in code_blocks:
        content = block['content'].strip()
        language = block['language'].lower()
        filename = block['filename']
        
        # Skip empty blocks
        if not content:
            continue
        
        # Determine file path based on filename or content analysis
        file_path = None
        
        if filename and filename in file_mappings:
            file_path = file_mappings[filename][0]
        else:
            # Try to infer from content
            if 'package main' in content and 'gin.New()' in content:
                file_path = 'backend/main.go'
            elif 'module ' in content and language == 'go':
                file_path = 'backend/go.mod'
            elif 'import React' in content or 'function App' in content:
                file_path = 'frontend/src/App.js'
            elif '"name":' in content and '"scripts":' in content:
                file_path = 'frontend/package.json'
            elif 'FROM golang' in content:
                file_path = 'backend/Dockerfile'
            elif 'FROM node' in content:
                file_path = 'frontend/Dockerfile'
            elif 'version:' in content and 'services:' in content:
                file_path = 'docker-compose.yml'
            elif 'docker_build' in content or 'k8s_yaml' in content:
                file_path = 'Tiltfile'
            elif 'apiVersion:' in content and 'kind:' in content:
                if 'Deployment' in content:
                    file_path = 'k8s/deployment.yaml'
                elif 'Service' in content:
                    file_path = 'k8s/service.yaml'
                elif 'ConfigMap' in content:
                    file_path = 'k8s/configmap.yaml'
            elif content.startswith('<!DOCTYPE html'):
                file_path = 'frontend/public/index.html'
            elif '.PHONY:' in content or 'build:' in content:
                file_path = 'Makefile'
            elif content.startswith('#!/bin/bash'):
                if 'setup' in content.lower():
                    file_path = 'scripts/setup.sh'
                else:
                    file_path = 'scripts/start.sh'
        
        # Create file if we determined a path
        if file_path:
            # Ensure directory exists
            dir_path = os.path.dirname(file_path)
            if dir_path:  # Only create if there's actually a directory
                os.makedirs(dir_path, exist_ok=True)
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Make scripts executable
            if file_path.endswith('.sh') or file_path == 'Tiltfile':
                os.chmod(file_path, 0o755)
            
            created_files.append(file_path)
            print(f"✅ Created: {file_path}")
        else:
            print(f"⚠️  Couldn't determine file path for {language} block")
            if len(content) < 200:
                print(f"   Content preview: {content[:100]}...")
    
    return created_files


def create_additional_files():
    """Create additional required files that might not be in the markdown."""
    
    additional_files = []
    
    # Create .gitignore
    gitignore_content = """# Dependencies
node_modules/
*.log

# Build outputs
/dist/
/build/

# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
go.work

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Tilt
.tiltbuild/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    additional_files.append('.gitignore')
    
    # Create README.md for the project
    readme_content = """# Full-Stack Web Service

A task management application built with Go backend and React frontend.

## Quick Start

### Prerequisites
- Go 1.19+
- Node.js 18+
- Docker & Docker Compose
- Tilt (https://tilt.dev)

### Development with Tilt
```bash
tilt up
```

### Manual Development
```bash
# Terminal 1 - Backend
cd backend
go mod tidy
go run main.go

# Terminal 2 - Frontend  
cd frontend
npm install
npm start
```

## Services
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- Tilt UI: http://localhost:10350

## API Endpoints
- GET /health - Health check
- GET /tasks - List all tasks
- POST /tasks - Create a task
- PUT /tasks/:id - Update a task
- DELETE /tasks/:id - Delete a task
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    additional_files.append('README.md')
    
    print("\n📄 Created additional files:")
    for file in additional_files:
        print(f"✅ {file}")
    
    return additional_files


def main():
    """Main function to extract code and set up project."""
    
    print("🚀 Extracting Full-Stack Web Service Code")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('02_code_implementation.md'):
        print("❌ 02_code_implementation.md not found!")
        print("   Make sure you're running this script from the generated_fullstack_service/ directory")
        return 1
    
    # Create project structure
    print("\n📁 Creating project structure...")
    create_project_structure()
    
    # Extract code from implementation markdown
    print("\n🔧 Extracting code files...")
    created_files = extract_and_create_files('02_code_implementation.md')
    
    # Create additional necessary files
    print("\n📄 Creating additional files...")
    additional_files = create_additional_files()
    
    # Summary
    total_files = len(created_files) + len(additional_files)
    print(f"\n🎉 SUCCESS! Created {total_files} files")
    
    print("\n💡 Next Steps:")
    print("1. Review the generated files")
    print("2. Install dependencies:")
    print("   cd backend && go mod tidy")
    print("   cd frontend && npm install")
    print("3. Start development with Tilt:")
    print("   tilt up")
    print("4. Or start services manually:")
    print("   Backend: cd backend && go run main.go")
    print("   Frontend: cd frontend && npm start")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
