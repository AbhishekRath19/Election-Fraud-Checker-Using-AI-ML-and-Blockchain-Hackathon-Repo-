# Python Requirements for Vote Ballot System

## Required Packages

### Core Web Framework
- **Flask==2.3.2**: Micro web framework for Python
- **Flask-SQLAlchemy==3.0.3**: SQLAlchemy integration for Flask
- **python-dotenv==1.0.0**: Environment variable management

### Blockchain Integration
- **web3==6.0.0**: Python library for interacting with Ethereum
- **eth-account==0.8.0**: Ethereum account management utilities

### Image Processing
- **Pillow==9.5.0**: Python Imaging Library for image compression

### Encryption
- **pycryptodome==3.18.0**: Self-contained Python package of low-level cryptographic primitives

### Database
- **SQLAlchemy==2.0.15**: Python SQL toolkit and Object Relational Mapper

### Development and Testing
- **pytest==7.3.1**: Testing framework
- **pytest-cov==4.0.0**: Coverage reporting for pytest

## Installation Instructions

Create a virtual environment and install the requirements:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Package Details

### Flask
Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

### Web3.py
Web3.py is a Python library for interacting with Ethereum. It provides a convenient way to interact with smart contracts, send transactions, and query blockchain data.

### Pillow
Pillow is the Python Imaging Library that adds support for opening, manipulating, and saving many different image file formats. It will be used for compressing government ID images.

### PyCryptodome
PyCryptodome is a self-contained Python package of low-level cryptographic primitives. It will be used for encrypting vote data before storing it in the database.

### SQLAlchemy
SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL. It will be used for database operations through Flask-SQLAlchemy.

## Version Pinning

All package versions are pinned to ensure consistent installations across different environments. These versions have been tested for compatibility with each other and with the Python 3.8+ requirement.

## Optional Dependencies

For production deployment, consider adding:
- **gunicorn**: WSGI HTTP Server for UNIX
- **psycopg2**: PostgreSQL database adapter (if using PostgreSQL instead of SQLite)
- **redis**: In-memory data structure store for caching

## Development Dependencies

For development, also consider:
- **flake8**: Code linting
- **black**: Code formatting
- **pre-commit**: Pre-commit hooks for code quality