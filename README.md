# Property Management System

A comprehensive Django-based web application for managing rental properties, tenants, leases, maintenance requests, and payments.

## Features

- **User Management**: Separate portals for landlords and tenants
- **Property Management**: List, view, and manage properties
- **Lease Agreements**: Create and manage lease contracts
- **Maintenance Requests**: Submit and track property maintenance needs
- **Payment Processing**: Handle rent payments and track payment history
- **Communications**: Messaging system between landlords and tenants

## Quick Start (Windows)

The easiest way to run this project is using our setup script:

1. **Clone the repository**
   ```
   git clone https://github.com/your-username/property-management-system.git
   cd property-management-system
   ```

2. **Run the setup script**
   - Simply double-click on `scripts/fix_and_run.bat` from File Explorer
   - OR run it from the command line:
     ```
     scripts\fix_and_run.bat
     ```

This script will:
- Check if Python is installed
- Create a virtual environment if needed
- Install all required dependencies
- Set up the database
- Start the development server

## Manual Installation (Alternative)

If you prefer to set up manually or are using a non-Windows system:

1. **Set up a virtual environment** (recommended)
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```
   python manage.py migrate
   ```

4. **Create a superuser** (optional)
   ```
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```
   python manage.py runserver
   ```

## Access the Application

- Open your browser and go to `http://127.0.0.1:8000/`
- Admin interface is available at `http://127.0.0.1:8000/admin/`

## Configuration

The project uses SQLite by default for development. For production:

1. Configure proper email settings in `settings.py`
2. Set up payment processing with proper Stripe API keys
3. Use a production-ready database (PostgreSQL recommended)
4. Set `DEBUG = False` and configure proper `ALLOWED_HOSTS`

## User Types

- **Landlords**: Can add properties, manage leases, and respond to maintenance requests
- **Tenants**: Can view their leases, submit maintenance requests, and make payments

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.