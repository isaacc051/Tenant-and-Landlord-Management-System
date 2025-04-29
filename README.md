# Tenant and Landlord Management System

A Django-based web application for managing properties, leases, maintenance requests, and communications between tenants and landlords.

## Features

- User authentication and authorization (Tenants and Landlords)
- Property listing and management
- Lease agreement management
- Maintenance request tracking
- Payment processing
- Communication system
- Notification system

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd Tenant-and-Landlord-Management-System
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

- `accounts/`: User authentication and profiles
- `properties/`: Property listing and management
- `leases/`: Lease agreement management
- `maintenance/`: Maintenance request tracking
- `payments/`: Payment processing
- `communications/`: Messaging system
- `notifications/`: Notification system

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the MIT License.