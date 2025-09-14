# 🔧 Configuration Guide - Stunting Checking App

## 📋 Overview

Aplikasi Stunting Checking App menggunakan sistem konfigurasi yang fleksibel untuk development dan production environments. Semua konfigurasi dapat disesuaikan melalui environment variables.

## 🌍 Environment Variables

### Database Configuration
```bash
DATABASE_URL=mysql+pymysql://username:password@host:port/database_name
```

### JWT Configuration
```bash
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Application Configuration
```bash
BASE_URL=http://localhost:8000
ENVIRONMENT=development
```

## 🚀 Setup Instructions

### Development Environment

1. **Copy environment file:**
   ```bash
   cp env.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   # Database Configuration
   DATABASE_URL=mysql+pymysql://root:password@db:3306/stunting_db
   
   # JWT Configuration
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Application Configuration
   BASE_URL=http://localhost:8000
   ENVIRONMENT=development
   ```

3. **Start with Docker Compose:**
   ```bash
   docker compose up -d
   ```

### Production Environment

1. **Set environment variables:**
   ```bash
   # Database Configuration
   DATABASE_URL=mysql+pymysql://username:password@your-db-host:3306/stunting_db
   
   # JWT Configuration
   SECRET_KEY=your-super-secure-secret-key-for-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Application Configuration
   BASE_URL=https://stunting-api.dedan.my.id
   ENVIRONMENT=production
   ```

2. **Update docker-compose.yml:**
   ```yaml
   environment:
     - DATABASE_URL=mysql+pymysql://username:password@your-db-host:3306/stunting_db
     - SECRET_KEY=your-super-secure-secret-key-for-production
     - BASE_URL=https://stunting-api.dedan.my.id
     - ENVIRONMENT=production
   ```

## 📁 Configuration Files

### `app/config.py`
File konfigurasi utama yang mengatur semua settings aplikasi:

```python
class Settings:
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@db:3306/stunting_db")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Base URL settings
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        # Production origins added automatically
    ]
```

### `env.example`
Template file untuk environment variables dengan contoh konfigurasi.

## 🔗 Base URL Configuration

### Development
```bash
BASE_URL=http://localhost:8000
```

### Production
```bash
BASE_URL=https://stunting-api.dedan.my.id
```

### Impact on PDF Reports
Base URL digunakan untuk generate download URL pada PDF reports:

```python
# PDF Service automatically uses BASE_URL from config
def get_report_url(self, filepath: str) -> str:
    filename = os.path.basename(filepath)
    return f"{self.base_url}/reports/{filename}"
```

**Example URLs:**
- Development: `http://localhost:8000/reports/diagnose_report_1_20250914_123456_abc12345.pdf`
- Production: `https://stunting-api.dedan.my.id/reports/diagnose_report_1_20250914_123456_abc12345.pdf`

## 🔒 Security Configuration

### JWT Secret Key
**⚠️ IMPORTANT:** Pastikan menggunakan secret key yang kuat di production:

```bash
# Development (weak - OK for local testing)
SECRET_KEY=your-secret-key-here

# Production (strong - required)
SECRET_KEY=your-super-secure-secret-key-with-at-least-32-characters
```

### CORS Configuration
CORS origins otomatis dikonfigurasi berdasarkan environment:

- **Development:** Localhost origins
- **Production:** Production domains + localhost untuk testing

## 🐳 Docker Configuration

### Development
```yaml
environment:
  - BASE_URL=http://localhost:8000
  - ENVIRONMENT=development
```

### Production
```yaml
environment:
  - BASE_URL=https://stunting-api.dedan.my.id
  - ENVIRONMENT=production
```

## 📊 Configuration Usage

### In Code
```python
from app.config import settings

# Use configuration
print(f"Base URL: {settings.BASE_URL}")
print(f"Environment: {settings.ENVIRONMENT}")
print(f"Database URL: {settings.DATABASE_URL}")
```

### In Services
```python
class PDFReportService:
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.reports_dir = settings.REPORTS_DIR
```

## 🔄 Environment Switching

### Quick Switch to Production
1. Update `BASE_URL` environment variable
2. Restart application
3. PDF download URLs automatically use new base URL

### Quick Switch to Development
1. Update `BASE_URL` to `http://localhost:8000`
2. Restart application
3. All URLs automatically switch back to localhost

## 🧪 Testing Configuration

### Test Current Configuration
```bash
# Test config loading
docker compose exec -ti app python -c "from app.config import settings; print(f'BASE_URL: {settings.BASE_URL}')"

# Test PDF service with current config
docker compose exec -ti app python -c "from app.services.pdf_service import PDFReportService; service = PDFReportService(); print(f'Base URL: {service.base_url}')"
```

## 📝 Notes

- **Environment Variables:** Semua konfigurasi dapat di-override melalui environment variables
- **Default Values:** Aplikasi memiliki default values yang aman untuk development
- **Production Security:** Pastikan menggunakan secret key yang kuat di production
- **Base URL:** PDF download URLs otomatis menggunakan BASE_URL yang dikonfigurasi
- **CORS:** Origins otomatis dikonfigurasi berdasarkan environment

## 🆘 Troubleshooting

### Common Issues

1. **PDF URLs not working:**
   - Check `BASE_URL` environment variable
   - Ensure reports directory is mounted correctly

2. **CORS errors:**
   - Check `CORS_ORIGINS` configuration
   - Add your frontend domain to allowed origins

3. **Database connection issues:**
   - Verify `DATABASE_URL` format
   - Check database credentials and host

4. **JWT token issues:**
   - Ensure `SECRET_KEY` is set
   - Check token expiration settings
