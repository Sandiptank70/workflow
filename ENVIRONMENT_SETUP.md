# Environment Configuration Guide

## Backend .env File

The backend requires a `.env` file in the `/backend` directory with the following variables:

### ✅ Already Configured

Your backend already has a `.env` file with these settings:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=securepassword
DB_NAME=workflow_db
DB_PORT=3306
ENCRYPTION_KEY=mzE3MjU4NzIxZjQ2YjM4ZGExZTU3MmE1YjE5NjA5NzY4ODc5ZGU0ZDJiNzM4YzQ4YWRhYzI1YzE3OTc1YzNkZQ==
```

### 📋 Configuration Explained

#### Database Settings
- **DB_HOST**: Database server location
  - Local: `localhost`
  - Docker: `db` (service name in docker-compose)
  
- **DB_USER**: Database username (default: `root`)

- **DB_PASSWORD**: Database password
  - ⚠️ **IMPORTANT**: Change this in production!
  - Default: `securepassword`

- **DB_NAME**: Database name (default: `workflow_db`)

- **DB_PORT**: Database port (default: `3306`)

#### Security Settings
- **ENCRYPTION_KEY**: Fernet encryption key for securing credentials
  - ✅ Already generated and ready to use
  - 🔐 Keep this secret and secure
  - ⚠️ Never commit to version control
  - 🔄 If compromised, generate new key (see below)

### 🔄 Generate New Encryption Key (if needed)

If you need to generate a new encryption key:

```bash
cd backend
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the output and replace the `ENCRYPTION_KEY` value in `.env`

⚠️ **WARNING**: Changing the encryption key will invalidate all existing encrypted credentials in the database!

### 🐳 Docker Environment

When using Docker Compose, the environment variables are automatically set in `docker-compose.yml`:

```yaml
environment:
  - DB_HOST=db
  - DB_USER=root
  - DB_PASSWORD=securepassword
  - DB_NAME=workflow_db
  - DB_PORT=3306
  - ENCRYPTION_KEY=mzE3MjU4NzIxZjQ2YjM4ZGExZTU3MmE1YjE5NjA5NzY4ODc5ZGU0ZDJiNzM4YzQ4YWRhYzI1YzE3OTc1YzNkZQ==
```

**Note**: `DB_HOST=db` for Docker (not `localhost`)

### 🔧 Customizing for Your Environment

#### For Local Development (MySQL/MariaDB)

If your MariaDB has different settings:

```env
# If running on a different host
DB_HOST=192.168.1.100

# If using a different user
DB_USER=workflow_user

# If using a different password
DB_PASSWORD=your_secure_password_here

# If using a different database name
DB_NAME=my_workflow_db

# If using a different port
DB_PORT=3307
```

#### For Production

1. **Change the database password**:
   ```env
   DB_PASSWORD=YourVerySecurePassword123!@#
   ```

2. **Use environment-specific encryption key**:
   - Generate production key separately
   - Store securely (e.g., AWS Secrets Manager, Azure Key Vault)

3. **Consider using environment variables** instead of .env file:
   ```bash
   export DB_HOST=production-db.example.com
   export DB_PASSWORD=$(cat /secure/path/db-password)
   export ENCRYPTION_KEY=$(cat /secure/path/encryption-key)
   ```

### 📁 File Locations

```
backend/
├── .env                 # Your configuration (ALREADY EXISTS ✅)
└── .env.example        # Template for reference
```

### ✅ Verification

Test if your .env is working:

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Test database connection
python -c "
from app.database import engine
try:
    with engine.connect() as conn:
        print('✅ Database connection successful!')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"

# Test encryption
python -c "
from app.utils.encryption import encryption_service
encrypted = encryption_service.encrypt('test')
decrypted = encryption_service.decrypt(encrypted)
print('✅ Encryption working!' if decrypted == 'test' else '❌ Encryption failed!')
"
```

### 🐛 Troubleshooting

#### Error: "ENCRYPTION_KEY environment variable not set"
**Solution**: Make sure `.env` file exists in `/backend` directory with `ENCRYPTION_KEY` set

#### Error: "Invalid ENCRYPTION_KEY"
**Solution**: Generate a new key using the command above

#### Error: "Can't connect to MySQL server"
**Solutions**:
1. Check if MariaDB is running: `systemctl status mariadb`
2. Verify DB_HOST is correct (localhost for local, db for Docker)
3. Test connection: `mysql -u root -p -h localhost`
4. Check if database exists: `SHOW DATABASES;`

#### Error: "Access denied for user 'root'"
**Solutions**:
1. Verify DB_PASSWORD is correct
2. Check user permissions: `GRANT ALL PRIVILEGES ON workflow_db.* TO 'root'@'localhost';`

### 🔐 Security Best Practices

1. ✅ **Never commit `.env` to Git**
   - Already in `.gitignore`
   - Use `.env.example` as template

2. ✅ **Use strong passwords**
   - Minimum 16 characters
   - Mix of letters, numbers, symbols

3. ✅ **Rotate encryption keys periodically**
   - Generate new key
   - Re-encrypt all credentials
   - Update `.env`

4. ✅ **Use different keys per environment**
   - Development key
   - Staging key
   - Production key

5. ✅ **Store production secrets securely**
   - Use secret management systems
   - AWS Secrets Manager
   - Azure Key Vault
   - HashiCorp Vault

### 📝 Summary

Your `.env` file is **already configured and ready to use** for local development! 

- ✅ Database settings configured
- ✅ Encryption key generated
- ✅ Default password set

**For production**: Remember to change `DB_PASSWORD` to something more secure!

### 🚀 Next Steps

1. Start MariaDB: `systemctl start mariadb`
2. Create database: `mysql -u root -p -e "CREATE DATABASE workflow_db;"`
3. Start backend: `cd backend && uvicorn app.main:app --reload`
4. Verify: http://localhost:8000/health

That's it! Your environment is ready! 🎉
