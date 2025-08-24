# Setup Guide for Vote Ballot System

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.8 or higher
- Node.js and npm (for Ganache)
- Git

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd election-fraud-checker
```

## Step 2: Set Up Python Environment

### Create a Virtual Environment
```bash
python -m venv venv
```

### Activate the Virtual Environment
On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Set Up Blockchain Environment

### Install Ganache
Ganache is a personal blockchain for Ethereum development. You can install it in two ways:

#### Option 1: Install Ganache CLI
```bash
npm install -g ganache
```

#### Option 2: Install Ganache GUI
Download from: https://trufflesuite.com/ganache/

### Start Ganache
If using Ganache CLI:
```bash
ganache -d
```

If using Ganache GUI:
1. Open the application
2. Click "Quickstart"

Note the RPC Server address (usually http://127.0.0.1:7545 or http://127.0.0.1:8545)

## Step 4: Configure Environment Variables

Create a `.env` file in the project root with the following content:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///election.db
BLOCKCHAIN_PROVIDER_URL=http://127.0.0.1:7545
```

## Step 5: Initialize the Database

Run the following commands to set up the database:

```bash
python -m flask db init
python -m flask db migrate -m "Initial migration"
python -m flask db upgrade
```

## Step 6: Deploy Smart Contract

Before running the application, you need to deploy the smart contract:

1. Start the Flask application in development mode
2. Access the deployment endpoint to deploy the contract
3. Update the `.env` file with the contract address

## Step 7: Run the Application

```bash
python run.py
```

The application will be available at http://127.0.0.1:5000

## Development Workflow

### Running Tests
```bash
python -m pytest
```

### Code Structure
- `app/` - Main application code
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and image files
- `tests/` - Unit and integration tests
- `contracts/` - Solidity smart contracts

### Making Changes
1. Create a new branch for your feature
2. Make your changes
3. Run tests to ensure nothing is broken
4. Commit and push your changes
5. Create a pull request

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `run.py` or kill the process using the port

2. **Database connection errors**
   - Check that the database file has correct permissions
   - Ensure the database URL in `.env` is correct

3. **Blockchain connection errors**
   - Verify Ganache is running
   - Check the RPC server URL in `.env`

4. **Missing dependencies**
   - Run `pip install -r requirements.txt` again
   - Ensure you're in the virtual environment

### Useful Commands

- Activate virtual environment: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
- Deactivate virtual environment: `deactivate`
- Check Python version: `python --version`
- Check pip packages: `pip list`
- Run Flask in debug mode: `flask --debug run`

## Next Steps

1. Customize the party list in the database
2. Add more security features as needed
3. Implement additional validation rules
4. Add more comprehensive logging
5. Set up continuous integration