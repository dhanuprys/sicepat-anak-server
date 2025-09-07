# Stunting Checking App API

Aplikasi API untuk deteksi stunting pada anak menggunakan FastAPI, SQLAlchemy, dan MySQL.

## 🚀 Fitur

- **Authentication**: JWT-based authentication system
- **User Management**: CRUD operations untuk user profile
- **Children Management**: CRUD operations untuk data anak
- **Stunting Detection**: API untuk diagnosa stunting (logic akan diimplementasikan nanti)
- **Database Migration**: Alembic untuk database versioning
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **Database**: MySQL
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: bcrypt
- **Validation**: Pydantic

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+
- pip

## 🔧 Installation

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd stunting
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp env.example .env
   # Edit .env file dengan konfigurasi database dan JWT secret
   ```

5. **Setup database**
   ```bash
   # Buat database MySQL
   mysql -u root -p
   CREATE DATABASE stunting_db;
   exit
   
   # Jalankan migration
   alembic upgrade head
   ```

## 🚀 Running the Application

1. **Start the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `avatar_type`: Integer untuk tipe avatar
- `name`: Nama lengkap user
- `username`: Username unik
- `address`: Alamat (nullable)
- `dob`: Tanggal lahir
- `gender`: Jenis kelamin
- `password`: Password ter-hash
- `registration_date`: Tanggal registrasi

### Childrens Table
- `id`: Primary key
- `user_id`: Foreign key ke users table
- `name`: Nama anak
- `gender`: Jenis kelamin (L/P)
- `dob`: Tanggal lahir
- `created_at`: Waktu pembuatan
- `updated_at`: Waktu update

### Diagnose Histories Table
- `id`: Primary key
- `children_id`: Foreign key ke childrens table
- `age_on_month`: Usia dalam bulan
- `height`: Tinggi badan dalam cm
- `diagnosed_at`: Waktu diagnosa

## 🔐 API Endpoints

### Unauthenticated
- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Registrasi user baru

### Authenticated (Require JWT Token)
- `PUT /api/profile` - Update profile
- `PUT /api/profile/change-password` - Ganti password
- `POST /api/children` - Buat data anak baru
- `GET /api/children` - List semua anak user
- `GET /api/children/{id}` - Detail anak
- `PUT /api/children/{id}` - Update data anak
- `DELETE /api/children/{id}` - Hapus data anak
- `POST /api/children/{id}/diagnose` - Buat diagnosa baru
- `GET /api/children/{id}/diagnose` - List diagnosa anak
- `GET /api/children/{id}/diagnose/{diagnose_id}` - Detail diagnosa

## 🔄 Database Migration

### Create new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

### Check current migration status
```bash
alembic current
```

## 🧪 Testing

Untuk testing, Anda bisa menggunakan:
- **Swagger UI**: http://localhost:8000/docs
- **Postman**: Import OpenAPI spec dari `/docs`
- **cURL**: Manual API calls

## 📝 Environment Variables

Buat file `.env` dengan konfigurasi berikut:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/stunting_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-make-it-long-and-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

## 🔒 Security Features

- **Password Hashing**: Menggunakan bcrypt
- **JWT Authentication**: Secure token-based auth
- **Input Validation**: Pydantic validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS Configuration**: Configurable CORS settings

## 🚧 TODO

- [ ] Implement stunting detection logic
- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Add logging configuration
- [ ] Add rate limiting
- [ ] Add API versioning
- [ ] Add bulk operations
- [ ] Add search and filtering
- [ ] Add pagination for list endpoints

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License.
