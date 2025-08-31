#!/bin/bash

# Farmazee Enterprise Platform Deployment Script
# This script provides multiple deployment options for different environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="farmazee"
DOCKER_COMPOSE_FILE="docker-compose.yml"
ENVIRONMENT=${ENVIRONMENT:-"development"}

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Check if required tools are installed
check_requirements() {
    log "Checking deployment requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        warning ".env file not found. Creating from template..."
        if [ -f env.example ]; then
            cp env.example .env
            warning "Please update .env file with your configuration values."
        else
            error "env.example file not found. Please create .env file manually."
        fi
    fi
    
    log "Requirements check completed."
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p media
    mkdir -p staticfiles
    mkdir -p backups
    mkdir -p ssl
    mkdir -p nginx/conf.d
    mkdir -p monitoring/grafana/provisioning
    mkdir -p init-scripts
    
    log "Directories created successfully."
}

# Build and start services
deploy_services() {
    local action=$1
    
    case $action in
        "start")
            log "Starting Farmazee services..."
            docker-compose -f $DOCKER_COMPOSE_FILE up -d
            ;;
        "stop")
            log "Stopping Farmazee services..."
            docker-compose -f $DOCKER_COMPOSE_FILE down
            ;;
        "restart")
            log "Restarting Farmazee services..."
            docker-compose -f $DOCKER_COMPOSE_FILE restart
            ;;
        "rebuild")
            log "Rebuilding and starting Farmazee services..."
            docker-compose -f $DOCKER_COMPOSE_FILE down
            docker-compose -f $DOCKER_COMPOSE_FILE build --no-cache
            docker-compose -f $DOCKER_COMPOSE_FILE up -d
            ;;
        "update")
            log "Updating Farmazee services..."
            docker-compose -f $DOCKER_COMPOSE_FILE pull
            docker-compose -f $DOCKER_COMPOSE_FILE up -d
            ;;
        *)
            error "Invalid action: $action. Use: start, stop, restart, rebuild, or update"
            ;;
    esac
}

# Database operations
database_operations() {
    local action=$1
    
    case $action in
        "migrate")
            log "Running database migrations..."
            docker-compose -f $DOCKER_COMPOSE_FILE exec web python manage.py migrate
            ;;
        "makemigrations")
            log "Creating database migrations..."
            docker-compose -f $DOCKER_COMPOSE_FILE exec web python manage.py makemigrations
            ;;
        "collectstatic")
            log "Collecting static files..."
            docker-compose -f $DOCKER_COMPOSE_FILE exec web python manage.py collectstatic --noinput
            ;;
        "createsuperuser")
            log "Creating superuser..."
            docker-compose -f $DOCKER_COMPOSE_FILE exec web python manage.py createsuperuser
            ;;
        "shell")
            log "Opening Django shell..."
            docker-compose -f $DOCKER_COMPOSE_FILE exec web python manage.py shell
            ;;
        "backup")
            log "Creating database backup..."
            docker-compose -f $DOCKER_COMPOSE_FILE exec postgres pg_dump -U farmazee_user farmazee_db > backups/backup_$(date +%Y%m%d_%H%M%S).sql
            ;;
        "restore")
            local backup_file=$2
            if [ -z "$backup_file" ]; then
                error "Please specify backup file to restore"
            fi
            log "Restoring database from backup: $backup_file"
            docker-compose -f $DOCKER_COMPOSE_FILE exec -T postgres psql -U farmazee_user farmazee_db < "backups/$backup_file"
            ;;
        *)
            error "Invalid database action: $action. Use: migrate, makemigrations, collectstatic, createsuperuser, shell, backup, or restore"
            ;;
    esac
}

# Monitoring and logs
monitoring() {
    local action=$1
    
    case $action in
        "logs")
            local service=${2:-""}
            if [ -z "$service" ]; then
                docker-compose -f $DOCKER_COMPOSE_FILE logs -f
            else
                docker-compose -f $DOCKER_COMPOSE_FILE logs -f "$service"
            fi
            ;;
        "status")
            log "Service status:"
            docker-compose -f $DOCKER_COMPOSE_FILE ps
            ;;
        "health")
            log "Health check:"
            docker-compose -f $DOCKER_COMPOSE_FILE exec web curl -f http://localhost:8000/health/ || error "Health check failed"
            ;;
        "metrics")
            log "Opening monitoring dashboards..."
            info "Grafana: http://localhost:3000 (admin/admin)"
            info "Prometheus: http://localhost:9090"
            info "Kibana: http://localhost:5601"
            info "Celery Flower: http://localhost:5555"
            ;;
        *)
            error "Invalid monitoring action: $action. Use: logs, status, health, or metrics"
            ;;
    esac
}

# Backup and restore
backup_restore() {
    local action=$1
    
    case $action in
        "backup")
            log "Creating full system backup..."
            local backup_dir="backups/backup_$(date +%Y%m%d_%H%M%S)"
            mkdir -p "$backup_dir"
            
            # Database backup
            docker-compose -f $DOCKER_COMPOSE_FILE exec postgres pg_dump -U farmazee_user farmazee_db > "$backup_dir/database.sql"
            
            # Media files backup
            if [ -d "media" ]; then
                tar -czf "$backup_dir/media.tar.gz" media/
            fi
            
            # Configuration backup
            cp .env "$backup_dir/"
            cp docker-compose.yml "$backup_dir/"
            
            log "Backup created in: $backup_dir"
            ;;
        "restore")
            local backup_dir=$2
            if [ -z "$backup_dir" ]; then
                error "Please specify backup directory to restore"
            fi
            if [ ! -d "backups/$backup_dir" ]; then
                error "Backup directory not found: backups/$backup_dir"
            fi
            
            log "Restoring from backup: $backup_dir"
            
            # Stop services
            docker-compose -f $DOCKER_COMPOSE_FILE down
            
            # Restore database
            if [ -f "backups/$backup_dir/database.sql" ]; then
                docker-compose -f $DOCKER_COMPOSE_FILE up -d postgres
                sleep 10
                docker-compose -f $DOCKER_COMPOSE_FILE exec -T postgres psql -U farmazee_user farmazee_db < "backups/$backup_dir/database.sql"
            fi
            
            # Restore media files
            if [ -f "backups/$backup_dir/media.tar.gz" ]; then
                rm -rf media/
                tar -xzf "backups/$backup_dir/media.tar.gz"
            fi
            
            # Restart services
            docker-compose -f $DOCKER_COMPOSE_FILE up -d
            
            log "Restore completed successfully"
            ;;
        *)
            error "Invalid backup action: $action. Use: backup or restore"
            ;;
    esac
}

# Development setup
dev_setup() {
    log "Setting up development environment..."
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Create .env file for development
    if [ ! -f .env ]; then
        cp env.example .env
        # Update .env for development
        sed -i 's/DEBUG=False/DEBUG=True/' .env
        sed -i 's/ENVIRONMENT=production/ENVIRONMENT=development/' .env
        sed -i 's/DB_ENGINE=django.db.backends.postgresql/DB_ENGINE=django.db.backends.sqlite3/' .env
        sed -i 's/DB_NAME=farmazee_db/DB_NAME=db.sqlite3/' .env
        sed -i 's/REDIS_URL=redis:\/\/127.0.0.1:6379/REDIS_URL=redis:\/\/localhost:6379/' .env
    fi
    
    # Run migrations
    python manage.py migrate
    
    # Create superuser
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@farmazee.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    log "Development environment setup completed."
    log "You can now run: python manage.py runserver"
    log "Admin credentials: admin / admin123"
}

# Production setup
prod_setup() {
    log "Setting up production environment..."
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        error "Production setup must be run as root"
    fi
    
    # Install system dependencies
    apt-get update
    apt-get install -y docker.io docker-compose nginx certbot python3-certbot-nginx
    
    # Start Docker service
    systemctl start docker
    systemctl enable docker
    
    # Create production .env
    if [ ! -f .env ]; then
        cp env.example .env
        warning "Please update .env file with production values"
        warning "Set DEBUG=False and ENVIRONMENT=production"
    fi
    
    # Create systemd service
    cat > /etc/systemd/system/farmazee.service << EOF
[Unit]
Description=Farmazee Enterprise Platform
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$(pwd)
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF
    
    # Enable and start service
    systemctl daemon-reload
    systemctl enable farmazee
    systemctl start farmazee
    
    log "Production environment setup completed."
    log "Service enabled and started. Use: systemctl status farmazee"
}

# SSL certificate management
ssl_management() {
    local action=$1
    local domain=$2
    
    case $action in
        "setup")
            if [ -z "$domain" ]; then
                error "Please specify domain for SSL setup"
            fi
            
            log "Setting up SSL certificate for domain: $domain"
            
            # Stop nginx temporarily
            docker-compose -f $DOCKER_COMPOSE_FILE stop nginx
            
            # Get SSL certificate
            certbot certonly --standalone -d "$domain" --email admin@farmazee.com --agree-tos --non-interactive
            
            # Copy certificates
            cp /etc/letsencrypt/live/"$domain"/fullchain.pem ssl/
            cp /etc/letsencrypt/live/"$domain"/privkey.pem ssl/
            
            # Restart nginx
            docker-compose -f $DOCKER_COMPOSE_FILE start nginx
            
            log "SSL certificate setup completed for $domain"
            ;;
        "renew")
            log "Renewing SSL certificates..."
            certbot renew
            log "SSL certificates renewed"
            ;;
        *)
            error "Invalid SSL action: $action. Use: setup or renew"
            ;;
    esac
}

# Main script
main() {
    local command=$1
    local subcommand=$2
    local args=${@:3}
    
    case $command in
        "deploy")
            check_requirements
            create_directories
            deploy_services "$subcommand"
            ;;
        "db")
            database_operations "$subcommand" $args
            ;;
        "monitor")
            monitoring "$subcommand" $args
            ;;
        "backup")
            backup_restore "$subcommand" $args
            ;;
        "dev")
            dev_setup
            ;;
        "prod")
            prod_setup
            ;;
        "ssl")
            ssl_management "$subcommand" $args
            ;;
        "help"|"--help"|"-h"|"")
            echo "Farmazee Enterprise Platform Deployment Script"
            echo ""
            echo "Usage: $0 <command> [subcommand] [args...]"
            echo ""
            echo "Commands:"
            echo "  deploy <action>     Deploy services (start|stop|restart|rebuild|update)"
            echo "  db <action>         Database operations (migrate|makemigrations|collectstatic|createsuperuser|shell|backup|restore)"
            echo "  monitor <action>    Monitoring and logs (logs|status|health|metrics)"
            echo "  backup <action>     Backup and restore (backup|restore)"
            echo "  dev                 Setup development environment"
            echo "  prod                Setup production environment"
            echo "  ssl <action>        SSL certificate management (setup|renew)"
            echo "  help                Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 deploy start"
            echo "  $0 db migrate"
            echo "  $0 monitor logs web"
            echo "  $0 backup backup"
            echo "  $0 ssl setup example.com"
            ;;
        *)
            error "Unknown command: $command. Use '$0 help' for usage information."
            ;;
    esac
}

# Run main function with all arguments
main "$@"

