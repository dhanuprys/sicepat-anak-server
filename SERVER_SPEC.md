# STUNTING CHECKING APP

# Entity Relational Diagram

## users:
 - id
 - avatar_type: int
 - name
 - username
 - address (nullable)
 - dob
 - gender
 - password
 - registration_date
 - ...other field that related to user account

## childrens:
 - id
 - user_id: refers to "users" with on delete cascade
 - name
 - gender (L/P)
 - dob
 - created_at
 - updated_at

## diagnose_histories:
 - id
 - children_id: refers to "childrens" with on delete cascade
 - age_on_month
 - height
 - diagnosed_at

# API Information

Every API should prefixed with /api pathname

## Unauthenticated API

### Login
POST /auth/login

### Register
POST /auth/register

## Authenticated API

### Update profile
PUT /profile
Params:
    - avatar_type: numerical
    - username
    - name
    - address
    - dob
    - gender

### Change password
PUT /profile/change-password
Params:
    - new_password

### Children REST API
/children

### Children stunting detection
POST /children/{children_id}/diagnose
Params:
    - age_on_month
    - gender
    - height

### Diagnose detail
GET /children/{children_id}/diagnose/{diagnose_id}

### Diagnose list of children
GET /children/{children_id}/diagnose