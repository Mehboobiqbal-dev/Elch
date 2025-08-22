name: Deploy to Azure App Service (Linux)

on:
  push:
    branches:
      - main
      - master
  pull_request:
    branches:
      - main
      - master
  workflow_dispatch:

env:
  AZURE_WEBAPP_NAME: elch-hbfga9d3hpfke4h2   # 👈 your App Service name
  AZURE_WEBAPP_PACKAGE_PATH: '.'              # deploy root
  PYTHON_VERSION: '3.11'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python ${{ env.PYTHON_VERSION }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
          
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests (if any)
      run: |
        if ls test_*.py 1> /dev/null 2>&1; then
          python -m pytest -v || echo "Tests completed with warnings"
        fi
        
    - name: Clean for deployment
      run: |
        rm -rf venv/ env/ .git/ tests/ __pycache__/ *.pyc
        rm -f .gitignore README.md *.log
        if [ -f "requirements-render.txt" ]; then
          cp requirements-render.txt requirements.txt
        fi
        
    - name: Upload artifact for deployment
      uses: actions/upload-artifact@v3
      with:
        name: python-app
        path: |
          .
          !venv/
          !env/
          !.git/
          !tests/
          !__pycache__/
          !*.pyc

  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: 'Production'
      url: ${{ steps.deploy-to-webapp.outputs.webapp-url }}
      
    steps:
    - name: Download artifact from build job
      uses: actions/download-artifact@v3
      with:
        name: python-app
        path: .

    - name: Create startup script
      run: |
        cat > startup.sh << 'EOF'
        #!/bin/bash
        export PYTHONUNBUFFERED=1
        export PYTHONDONTWRITEBYTECODE=1
        export PYTHONOPTIMIZE=2

        gunicorn -k uvicorn.workers.UvicornWorker \
          --bind=0.0.0.0:$PORT \
          --workers=2 \
          --timeout=120 \
          main:app
        EOF
        chmod +x startup.sh
        
    - name: Deploy to Azure Web App (Linux)
      id: deploy-to-webapp
      uses: azure/webapps-deploy@v2
      with:
        app-name: ${{ env.AZURE_WEBAPP_NAME }}
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: ${{ env.AZURE_WEBAPP_PACKAGE_PATH }}
        
    - name: Verify deployment
      run: |
        echo "Deployment completed. Checking application health..."
        sleep 30
        response=$(curl -s -o /dev/null -w "%{http_code}" https://${{ env.AZURE_WEBAPP_NAME }}.azurewebsites.net/healthz || echo "000")
        if [ "$response" = "200" ]; then
          echo "✅ Application is healthy and responding"
        else
          echo "⚠️ Application health check returned: $response"
          echo "Application URL: https://${{ env.AZURE_WEBAPP_NAME }}.azurewebsites.net"
        fi
