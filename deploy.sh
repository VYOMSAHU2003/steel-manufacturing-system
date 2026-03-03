#!/bin/bash

# 🚀 Steel Manufacturing System - Deployment Script
# This script automates the deployment process for different platforms

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Script configuration
PROJECT_NAME="steel-manufacturing-system"
GITHUB_USER=${GITHUB_USER:-"yourusername"}
REPO_URL="https://github.com/$GITHUB_USER/$PROJECT_NAME.git"

# Function to display help
show_help() {
    echo "🏭 Steel Manufacturing System - Deployment Script"
    echo ""
    echo "Usage: ./deploy.sh [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  setup         Initial project setup and git configuration"
    echo "  github        Push to GitHub (creates remote if needed)"
    echo "  streamlit     Deploy to Streamlit Cloud"
    echo "  heroku        Deploy to Heroku"
    echo "  docker        Build and run Docker containers"
    echo "  railway       Deploy to Railway"
    echo "  local         Run locally for testing"
    echo "  clean         Clean build artifacts and cache"
    echo "  test          Run tests and quality checks"
    echo "  backup        Create project backup"
    echo ""
    echo "Options:"
    echo "  --github-user  Set GitHub username"
    echo "  --branch       Set git branch (default: main)"
    echo "  --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./deploy.sh setup"
    echo "  ./deploy.sh github --github-user myusername"
    echo "  ./deploy.sh docker"
    echo "  ./deploy.sh streamlit"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    # Check if python is installed
    if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
        error "Python is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    # Check Python version
    python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
    required_version="3.8"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
        error "Python 3.8+ is required. Current version: $python_version"
        exit 1
    fi
    
    log "Prerequisites check passed ✅"
}

# Function to setup project
setup_project() {
    log "Setting up Steel Manufacturing System project..."
    
    check_prerequisites
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate || source venv/Scripts/activate
    
    # Install dependencies
    log "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Initialize database
    log "Initializing database..."
    python scripts/init_db.py
    
    # Setup git if not already done
    if [ ! -d ".git" ]; then
        log "Initializing Git repository..."
        git init
        git add .
        git commit -m "🏭 Initial commit: Steel Manufacturing Plant Management System"
        git branch -M main
    fi
    
    log "Project setup completed successfully! ✅"
    info "You can now run: ./deploy.sh local"
}

# Function to push to GitHub
deploy_github() {
    log "Deploying to GitHub..."
    
    # Parse GitHub username
    while [[ $# -gt 0 ]]; do
        case $1 in
            --github-user)
                GITHUB_USER="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
    
    if [ "$GITHUB_USER" = "yourusername" ]; then
        warning "Please set your GitHub username with --github-user flag"
        echo "Example: ./deploy.sh github --github-user myusername"
        exit 1
    fi
    
    REPO_URL="https://github.com/$GITHUB_USER/$PROJECT_NAME.git"
    
    # Add remote if not exists
    if ! git remote get-url origin &> /dev/null; then
        log "Adding GitHub remote..."
        git remote add origin "$REPO_URL"
    fi
    
    # Push to GitHub
    log "Pushing to GitHub repository: $REPO_URL"
    git add .
    git commit -m "🚀 Deploy: $(date +'%Y-%m-%d %H:%M:%S')" || true
    git push -u origin main
    
    log "Successfully pushed to GitHub! ✅"
    info "Repository URL: $REPO_URL"
    info "Next steps:"
    info "1. Go to https://share.streamlit.io"
    info "2. Connect your GitHub repository"
    info "3. Deploy your app!"
}

# Function to deploy to Streamlit Cloud
deploy_streamlit() {
    log "Preparing for Streamlit Cloud deployment..."
    
    # Ensure streamlit config exists
    mkdir -p .streamlit
    
    # Check if requirements.txt exists and is up to date
    log "Verifying requirements.txt..."
    pip freeze > requirements.txt
    
    info "Streamlit Cloud deployment preparation complete! ✅"
    info ""
    info "Manual steps to complete deployment:"
    info "1. Ensure your code is pushed to GitHub"
    info "2. Go to https://share.streamlit.io"
    info "3. Sign in with your GitHub account"
    info "4. Click 'Deploy an app'"
    info "5. Select repository: $GITHUB_USER/$PROJECT_NAME"
    info "6. Set main file path: app.py"
    info "7. Click 'Deploy'"
    info ""
    info "Your app will be available at: https://$PROJECT_NAME.streamlit.app"
}

# Function to deploy to Heroku
deploy_heroku() {
    log "Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        error "Heroku CLI is not installed. Please install it first:"
        echo "https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Login to Heroku
    heroku login
    
    # Create Heroku app
    app_name="steel-manufacturing-$(date +%s)"
    log "Creating Heroku app: $app_name"
    heroku create "$app_name"
    
    # Push to Heroku
    log "Deploying to Heroku..."
    git push heroku main
    
    # Open app
    heroku open
    
    log "Successfully deployed to Heroku! ✅"
    info "App URL: https://$app_name.herokuapp.com"
}

# Function to run with Docker
deploy_docker() {
    log "Building and running with Docker..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Build Docker image
    log "Building Docker image..."
    docker build -t steel-manufacturing-system .
    
    # Run Docker container
    log "Starting Docker container..."
    docker run -d -p 8501:8501 --name steel-manufacturing steel-manufacturing-system
    
    log "Docker deployment completed! ✅"
    info "Application is running at: http://localhost:8501"
    info "To stop: docker stop steel-manufacturing"
    info "To remove: docker rm steel-manufacturing"
}

# Function to deploy to Railway
deploy_railway() {
    log "Preparing for Railway deployment..."
    
    info "Railway deployment steps:"
    info "1. Go to https://railway.app"
    info "2. Sign in with GitHub"
    info "3. Click 'New Project' → 'Deploy from GitHub repo'"
    info "4. Select: $GITHUB_USER/$PROJECT_NAME"
    info "5. Configure environment variables:"
    info "   - PORT=8501"
    info "   - ORACLE_HOST=your_host (optional)"
    info "6. Deploy!"
    
    warning "Make sure your code is pushed to GitHub first!"
}

# Function to run locally
run_local() {
    log "Running Steel Manufacturing System locally..."
    
    # Activate virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate || source venv/Scripts/activate
    fi
    
    # Install dependencies if needed
    pip install -r requirements.txt
    
    # Initialize database if needed
    if [ ! -f "manufacturing.db" ]; then
        python scripts/init_db.py
    fi
    
    # Run Streamlit
    log "Starting Streamlit server..."
    streamlit run app.py
}

# Function to clean project
clean_project() {
    log "Cleaning project artifacts..."
    
    # Remove Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove build artifacts
    rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage
    
    # Remove logs
    rm -rf logs/*.log 2>/dev/null || true
    
    log "Cleanup completed! ✅"
}

# Function to run tests
run_tests() {
    log "Running tests and quality checks..."
    
    # Activate virtual environment
    if [ -d "venv" ]; then
        source venv/bin/activate || source venv/Scripts/activate
    fi
    
    # Install test dependencies
    pip install flake8 black isort
    
    # Run code formatting check
    log "Checking code formatting with Black..."
    black --check . || true
    
    # Run import sorting check
    log "Checking import sorting with isort..."
    isort --check-only . || true
    
    # Run linting
    log "Running code analysis with flake8..."
    flake8 . --count --statistics || true
    
    # Test database initialization
    log "Testing database initialization..."
    python scripts/init_db.py
    
    log "Tests completed! ✅"
}

# Function to create backup
create_backup() {
    log "Creating project backup..."
    
    backup_dir="backups/$(date +'%Y%m%d_%H%M%S')"
    mkdir -p "$backup_dir"
    
    # Copy important files
    cp -r . "$backup_dir/" 2>/dev/null || true
    
    # Exclude unnecessary files from backup
    rm -rf "$backup_dir/venv" "$backup_dir/__pycache__" "$backup_dir/.git"
    
    # Create tar archive
    tar -czf "$backup_dir.tar.gz" -C "$backup_dir" .
    rm -rf "$backup_dir"
    
    log "Backup created: $backup_dir.tar.gz ✅"
}

# Main script logic
main() {
    case "${1:-help}" in
        setup)
            setup_project
            ;;
        github)
            shift
            deploy_github "$@"
            ;;
        streamlit)
            deploy_streamlit
            ;;
        heroku)
            deploy_heroku
            ;;
        docker)
            deploy_docker
            ;;
        railway)
            deploy_railway
            ;;
        local)
            run_local
            ;;
        clean)
            clean_project
            ;;
        test)
            run_tests
            ;;
        backup)
            create_backup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Banner
echo "🏭 ========================================"
echo "   Steel Manufacturing System Deployer"
echo "   Enterprise-Grade Manufacturing Solution"
echo "======================================== 🏭"
echo ""

# Run main function with all arguments
main "$@"