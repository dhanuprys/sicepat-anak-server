# 📚 API Documentation - Stunting Checking App

## 🏗️ **Overview**

**Stunting Checking App** adalah aplikasi API untuk deteksi stunting pada anak menggunakan FastAPI, SQLAlchemy, dan MySQL. Aplikasi ini menyediakan sistem autentikasi JWT, manajemen user dan anak, serta fitur diagnosa stunting menggunakan machine learning.

- **Base URL**: `http://localhost:8000`
- **API Prefix**: `/api`
- **Documentation**: `/docs` (Swagger UI), `/redoc` (ReDoc)
- **Version**: 1.0.0

---

## 🔐 **Authentication**

### **JWT Token Format**
```
token: <access_token>
```

### **Token Response Format**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "avatar_type": 1,
    "name": "string",
    "username": "string",
    "address": "string",
    "dob": "YYYY-MM-DD",
    "gender": "string",
    "is_admin": false,
    "registration_date": "YYYY-MM-DDTHH:MM:SS"
  }
}
```

---

## 📋 **API Endpoints**

### **1. Authentication (Unauthenticated)**

#### **POST** `/api/auth/login`
**Description**: Login user untuk mendapatkan access token

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "avatar_type": 1,
    "name": "string",
    "username": "string",
    "address": "string",
    "dob": "YYYY-MM-DD",
    "gender": "string",
    "is_admin": false,
    "registration_date": "YYYY-MM-DDTHH:MM:SS"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Username atau password salah
- `422 Unprocessable Entity`: Data tidak valid

---

#### **POST** `/api/auth/register`
**Description**: Registrasi user baru

**Request Body**:
```json
{
  "avatar_type": 1,
  "name": "string",
  "username": "string",
  "address": "string (optional)",
  "dob": "YYYY-MM-DD",
  "gender": "string",
  "password": "string (min 6 characters)"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "avatar_type": 1,
  "name": "string",
  "username": "string",
  "address": "string",
  "dob": "YYYY-MM-DD",
  "gender": "string",
  "is_admin": false,
  "registration_date": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `400 Bad Request`: Username sudah terdaftar
- `422 Unprocessable Entity`: Data tidak valid

---

### **2. Profile Management (Authenticated)**

#### **GET** `/api/profile`
**Description**: Get current user profile information

**Headers**: `token: <access_token>`

**Response** (200 OK):
```json
{
  "id": 1,
  "avatar_type": 1,
  "name": "string",
  "username": "string",
  "address": "string",
  "dob": "YYYY-MM-DD",
  "gender": "string",
  "is_admin": false,
  "registration_date": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid

---

#### **PUT** `/api/profile`
**Description**: Update profile user

**Headers**: `token: <access_token>`

**Request Body**:
```json
{
  "avatar_type": 1,
  "name": "string",
  "username": "string",
  "address": "string",
  "dob": "YYYY-MM-DD",
  "gender": "string"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "avatar_type": 1,
  "name": "string",
  "username": "string",
  "address": "string",
  "dob": "YYYY-MM-DD",
  "gender": "string",
  "is_admin": false,
  "registration_date": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: User tidak ditemukan
- `422 Unprocessable Entity`: Data tidak valid

---

#### **PUT** `/api/profile/change-password`
**Description**: Ganti password user

**Headers**: `token: <access_token>`

**Request Body**:
```json
{
  "new_password": "string (min 6 characters)"
}
```

**Response** (200 OK):
```json
{
  "message": "Password updated successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: User tidak ditemukan
- `422 Unprocessable Entity`: Password tidak valid

---

### **3. Children Management (Authenticated)**

#### **POST** `/api/children`
**Description**: Buat data anak baru

**Headers**: `token: <access_token>`

**Request Body**:
```json
{
  "name": "string",
  "gender": "L|P",
  "dob": "YYYY-MM-DD"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "string",
  "gender": "L",
  "dob": "YYYY-MM-DD",
  "user_id": 1,
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `422 Unprocessable Entity`: Data tidak valid

---

#### **GET** `/api/children`
**Description**: Dapatkan semua data anak user

**Headers**: `token: <access_token>`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "string",
    "gender": "L",
    "dob": "YYYY-MM-DD",
    "user_id": 1,
    "created_at": "YYYY-MM-DDTHH:MM:SS",
    "updated_at": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid

---

#### **GET** `/api/children/{children_id}`
**Description**: Dapatkan detail anak berdasarkan ID

**Headers**: `token: <access_token>`

**Path Parameters**:
- `children_id`: ID anak (integer)

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "string",
  "gender": "L",
  "dob": "YYYY-MM-DD",
  "user_id": 1,
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: Anak tidak ditemukan

---

#### **PUT** `/api/children/{children_id}`
**Description**: Update data anak

**Headers**: `token: <access_token>`

**Path Parameters**:
- `children_id`: ID anak (integer)

**Request Body**:
```json
{
  "name": "string",
  "gender": "L|P",
  "dob": "YYYY-MM-DD"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "string",
  "gender": "L",
  "dob": "YYYY-MM-DD",
  "user_id": 1,
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: Anak tidak ditemukan
- `422 Unprocessable Entity`: Data tidak valid

---

#### **DELETE** `/api/children/{children_id}`
**Description**: Hapus data anak

**Headers**: `token: <access_token>`

**Path Parameters**:
- `children_id`: ID anak (integer)

**Response** (200 OK):
```json
{
  "message": "Children deleted successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: Anak tidak ditemukan

---

### **4. Stunting Diagnosis (Authenticated)**

#### **POST** `/api/children/{children_id}/diagnose`
**Description**: Buat diagnosa stunting baru untuk anak

**Headers**: `token: <access_token>`

**Path Parameters**:
- `children_id`: ID anak (integer)

**Request Body**:
```json
{
  "age_on_month": 24,
  "gender": "L",
  "height": 85
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "age_on_month": 24,
  "gender": "L",
  "height": 85,
  "result": "Normal",
  "children_id": 1,
  "diagnosed_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: Anak tidak ditemukan
- `422 Unprocessable Entity`: Data tidak valid
- `500 Internal Server Error`: ML prediction gagal
- `503 Service Unavailable`: ML predictor tidak siap

---

#### **GET** `/api/children/{children_id}/diagnose`
**Description**: Dapatkan semua riwayat diagnosa anak

**Headers**: `token: <access_token>`

**Path Parameters**:
- `children_id`: ID anak (integer)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "age_on_month": 24,
    "gender": "L",
    "height": 85,
    "result": "Normal",
    "children_id": 1,
    "diagnosed_at": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: Anak tidak ditemukan
- `500 Internal Server Error`: Server error

---

#### **GET** `/api/children/{children_id}/diagnose/{diagnose_id}`
**Description**: Dapatkan detail diagnosa berdasarkan ID

**Headers**: `token: <access_token>`

**Path Parameters**:
- `children_id`: ID anak (integer)
- `diagnose_id`: ID diagnosa (integer)

**Response** (200 OK):
```json
{
  "id": 1,
  "age_on_month": 24,
  "gender": "L",
  "height": 85,
  "result": "Normal",
  "children_id": 1,
  "diagnosed_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: Anak atau diagnosa tidak ditemukan

---

#### **GET** `/api/children/{children_id}/diagnose/{diagnose_id}/report`
**Description**: Generate PDF report untuk diagnosa spesifik

**Headers**: `token: <access_token>`

**Path Parameters**:
- `children_id`: ID anak (integer)
- `diagnose_id`: ID diagnosa (integer)

**Response** (200 OK):
```json
{
  "message": "PDF report generated successfully",
  "download_url": "http://localhost:8000/reports/diagnose_report_1_20250913_123456_abc12345.pdf",
  "filename": "diagnose_report_1_20250913_123456_abc12345.pdf",
  "diagnose_id": 1,
  "children_id": 1
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `404 Not Found`: Anak atau diagnosa tidak ditemukan
- `500 Internal Server Error`: Gagal generate PDF report

**PDF Report Format**:
```
SURAT KETERANGAN HASIL DIAGNOSA
Nomor: 000001

Menerangkan bahwa:
1. Nama Pasien : [Nama Anak]
2. Jenis Kelamin : [Laki-laki/Perempuan]
3. Alamat : [Alamat User]

Telah diperiksa pada tanggal [Tanggal Diagnosa] dengan hasil pemeriksaan sebagai berikut:

Data Pemeriksaan :
1. Umur : [X] bulan
2. Berat Badan : Tidak diukur
3. Tinggi Badan : [X] cm

Diagnosa Medis :
[Normal/Stunted/Severely Stunted/Tinggi]
```

---

### **5. Admin Management (Admin Only)**

#### **GET** `/api/users/`
**Description**: Get all users (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "avatar_type": 1,
    "name": "string",
    "username": "string",
    "address": "string",
    "dob": "YYYY-MM-DD",
    "gender": "string",
    "is_admin": false,
    "registration_date": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required

---

#### **GET** `/api/users/{user_id}`
**Description**: Get user by ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `user_id`: ID user (integer)

**Response** (200 OK):
```json
{
  "id": 1,
  "avatar_type": 1,
  "name": "string",
  "username": "string",
  "address": "string",
  "dob": "YYYY-MM-DD",
  "gender": "string",
  "is_admin": false,
  "registration_date": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: User tidak ditemukan

---

#### **PUT** `/api/users/{user_id}`
**Description**: Update user by ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `user_id`: ID user (integer)

**Request Body**:
```json
{
  "avatar_type": 1,
  "name": "string",
  "username": "string",
  "address": "string",
  "dob": "YYYY-MM-DD",
  "gender": "string"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "avatar_type": 1,
  "name": "string",
  "username": "string",
  "address": "string",
  "dob": "YYYY-MM-DD",
  "gender": "string",
  "is_admin": false,
  "registration_date": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: User tidak ditemukan
- `422 Unprocessable Entity`: Data tidak valid

---

#### **DELETE** `/api/users/{user_id}`
**Description**: Delete user by ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `user_id`: ID user (integer)

**Response** (200 OK):
```json
{
  "message": "User deleted successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: User tidak ditemukan

---

### **6. Admin Children Management (Admin Only)**

#### **GET** `/api/users/children/`
**Description**: Get all children from all users (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "string",
    "gender": "L",
    "dob": "YYYY-MM-DD",
    "user_id": 1,
    "created_at": "YYYY-MM-DDTHH:MM:SS",
    "updated_at": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required

---

#### **GET** `/api/users/children/{children_id}`
**Description**: Get children by ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `children_id`: ID anak (integer)

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "string",
  "gender": "L",
  "dob": "YYYY-MM-DD",
  "user_id": 1,
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: Anak tidak ditemukan

---

#### **GET** `/api/users/children/user/{user_id}`
**Description**: Get all children by user ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `user_id`: ID user (integer)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "string",
    "gender": "L",
    "dob": "YYYY-MM-DD",
    "user_id": 1,
    "created_at": "YYYY-MM-DDTHH:MM:SS",
    "updated_at": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required

---

#### **POST** `/api/users/children/`
**Description**: Create children for any user (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Request Body**:
```json
{
  "name": "string",
  "gender": "L|P",
  "dob": "YYYY-MM-DD",
  "user_id": 1
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "string",
  "gender": "L",
  "dob": "YYYY-MM-DD",
  "user_id": 1,
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `422 Unprocessable Entity`: Data tidak valid

---

#### **PUT** `/api/users/children/{children_id}`
**Description**: Update children by ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `children_id`: ID anak (integer)

**Request Body**:
```json
{
  "name": "string",
  "gender": "L|P",
  "dob": "YYYY-MM-DD"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "string",
  "gender": "L",
  "dob": "YYYY-MM-DD",
  "user_id": 1,
  "created_at": "YYYY-MM-DDTHH:MM:SS",
  "updated_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: Anak tidak ditemukan
- `422 Unprocessable Entity`: Data tidak valid

---

#### **DELETE** `/api/users/children/{children_id}`
**Description**: Delete children by ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `children_id`: ID anak (integer)

**Response** (200 OK):
```json
{
  "message": "Children deleted successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: Anak tidak ditemukan

---

### **7. Admin Diagnose Management (Admin Only)**

#### **GET** `/api/users/diagnose/`
**Description**: Get all diagnose histories from all users (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "age_on_month": 24,
    "gender": "L",
    "height": 85,
    "result": "Normal",
    "children_id": 1,
    "diagnosed_at": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required

---

#### **GET** `/api/users/diagnose/{diagnose_id}`
**Description**: Get diagnose by ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `diagnose_id`: ID diagnosa (integer)

**Response** (200 OK):
```json
{
  "id": 1,
  "age_on_month": 24,
  "gender": "L",
  "height": 85,
  "result": "Normal",
  "children_id": 1,
  "diagnosed_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: Diagnosa tidak ditemukan

---

#### **GET** `/api/users/diagnose/children/{children_id}`
**Description**: Get all diagnose histories by children ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `children_id`: ID anak (integer)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "age_on_month": 24,
    "gender": "L",
    "height": 85,
    "result": "Normal",
    "children_id": 1,
    "diagnosed_at": "YYYY-MM-DDTHH:MM:SS"
  }
]
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required

---

#### **POST** `/api/users/diagnose/children/{children_id}`
**Description**: Create diagnose history for any children (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `children_id`: ID anak (integer)

**Request Body**:
```json
{
  "age_on_month": 24,
  "gender": "L",
  "height": 85
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "age_on_month": 24,
  "gender": "L",
  "height": 85,
  "result": "Normal",
  "children_id": 1,
  "diagnosed_at": "YYYY-MM-DDTHH:MM:SS"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: Anak tidak ditemukan
- `422 Unprocessable Entity`: Data tidak valid
- `500 Internal Server Error`: ML prediction gagal
- `503 Service Unavailable`: ML predictor tidak siap

---

#### **DELETE** `/api/users/diagnose/{diagnose_id}`
**Description**: Delete diagnose history by ID (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `diagnose_id`: ID diagnosa (integer)

**Response** (200 OK):
```json
{
  "message": "Diagnose history deleted successfully"
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: Diagnosa tidak ditemukan

---

#### **GET** `/api/users/diagnose/children/{children_id}/diagnose/{diagnose_id}/report`
**Description**: Generate PDF report for specific diagnose (Admin only)

**Headers**: `token: <access_token>`

**Authorization**: Requires admin privileges (`is_admin: true`)

**Path Parameters**:
- `children_id`: ID anak (integer)
- `diagnose_id`: ID diagnosa (integer)

**Response** (200 OK):
```json
{
  "message": "PDF report generated successfully",
  "download_url": "http://localhost:8000/reports/diagnose_report_1_20250913_123456_abc12345.pdf",
  "filename": "diagnose_report_1_20250913_123456_abc12345.pdf",
  "diagnose_id": 1,
  "children_id": 1
}
```

**Error Responses**:
- `401 Unauthorized`: Token tidak valid
- `403 Forbidden`: Admin privileges required
- `404 Not Found`: Anak atau diagnosa tidak ditemukan
- `500 Internal Server Error`: Gagal generate PDF report

---

### **8. ML Predictor Status (Public)**

#### **GET** `/api/children/predictor/status`
**Description**: Cek status ML predictor

**Response** (200 OK):
```json
{
  "status": "ready",
  "model_info": {
    "model_name": "string",
    "version": "string",
    "accuracy": "float"
  },
  "cache_status": {
    "total_cached": 0,
    "cache_hits": 0
  }
}
```

**Response** (200 OK) - Not Ready:
```json
{
  "status": "not_ready",
  "message": "Stunting predictor is not initialized or trained"
}
```

---

### **9. System Endpoints (Public)**

#### **GET** `/`
**Description**: Root endpoint

**Response** (200 OK):
```json
{
  "message": "Welcome to Stunting Checking App API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

#### **GET** `/health`
**Description**: Health check endpoint

**Response** (200 OK):
```json
{
  "status": "healthy"
}
```

---

## 📊 **Data Models & Validation**

### **User Model**
```typescript
{
  id: number
  avatar_type: number
  name: string
  username: string (unique)
  address: string | null
  dob: date (YYYY-MM-DD)
  gender: string
  password: string (min 6 chars)
  is_admin: boolean (nullable, default: false)
  registration_date: datetime
}
```

### **Children Model**
```typescript
{
  id: number
  user_id: number (foreign key to users.id)
  name: string
  gender: "L" | "P"
  dob: date (YYYY-MM-DD)
  created_at: datetime
  updated_at: datetime
}
```

### **Diagnose History Model**
```typescript
{
  id: number
  children_id: number (foreign key to childrens.id)
  age_on_month: number (0-60 months)
  gender: "L" | "P"
  height: number (30-200 cm)
  result: "Normal" | "Severely Stunted" | "Stunted" | "Tinggi"
  diagnosed_at: datetime
}
```

---

## ✅ **Validation Rules**

### **Age Validation**
- **Range**: 0-60 bulan
- **Type**: Integer

### **Height Validation**
- **Range**: 30-200 cm
- **Type**: Integer

### **Gender Validation**
- **Values**: "L" (Laki-laki) atau "P" (Perempuan)
- **Type**: String

### **Password Validation**
- **Minimum Length**: 6 karakter
- **Type**: String

### **Result Validation**
- **Values**: "Normal", "Severely Stunted", "Stunted", "Tinggi"
- **Type**: String

---

## 🔒 **Security Features**

### **Authentication**
- JWT-based authentication
- Token expiration: 30 menit (configurable)
- Secure password hashing dengan bcrypt

### **Authorization**
- User hanya dapat mengakses data miliknya sendiri
- Cascade delete untuk data anak dan diagnosa

### **Input Validation**
- Pydantic validation untuk semua input
- SQL injection protection dengan SQLAlchemy ORM
- CORS configuration

---

## 🚨 **Error Handling**

### **HTTP Status Codes**
- `200 OK`: Request berhasil
- `201 Created`: Resource berhasil dibuat
- `400 Bad Request`: Data request tidak valid
- `401 Unauthorized`: Token tidak valid atau tidak ada
- `404 Not Found`: Resource tidak ditemukan
- `422 Unprocessable Entity`: Data validation error
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: ML predictor tidak siap

### **Error Response Format**
```json
{
  "detail": "Error message description"
}
```
---

## 🧪 **Testing & Development**

### **Swagger UI**
- **URL**: `http://localhost:8000/docs`
- **Features**: Interactive API testing, request/response examples

### **ReDoc**
- **URL**: `http://localhost:8000/redoc`
- **Features**: Clean API documentation, searchable

### **Health Check**
- **URL**: `http://localhost:8000/health`
- **Purpose**: Verify API availability

---

## 📝 **Notes**

### **ML Predictor Integration**
- Aplikasi menggunakan machine learning model untuk prediksi stunting
- Model memproses input: usia (bulan), gender, tinggi (cm)
- Output: kategori stunting (Normal, Stunted, Severely Stunted, Tinggi)

### **Database Relationships**
- User → Children (One-to-Many)
- Children → DiagnoseHistory (One-to-Many)
- Cascade delete untuk maintain data integrity

### **Performance Considerations**
- Database indexing pada username dan foreign keys
- ML model caching untuk prediksi yang sama
- Connection pooling untuk database

---

## 🔄 **API Versioning**

- **Current Version**: v1.0.0
- **Base Path**: `/api`
- **Future Versions**: `/api/v2`, `/api/v3`, etc.

---

## 📞 **Support**

Untuk pertanyaan atau masalah teknis, silakan buat issue di repository atau hubungi tim development.

---

*Dokumentasi ini dibuat berdasarkan analisis kode aplikasi Stunting Checking App v1.0.0*

