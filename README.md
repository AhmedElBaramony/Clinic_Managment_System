# Clinic Management System

## Overview
This Clinic Management System is a comprehensive application designed to manage the operations of a medical clinic. It includes features for managing patients, appointments, doctors, receptionists, prescriptions, and payrolls. The system is built using Python with a SQL Server database backend, ensuring robust data management and security.

## Features
- **User Authentication**: Secure login processes for Receptionists, Doctors, and Patients with tailored access rights.
- **Patient Management**: Comprehensive tools to add, update, and view patient details, along with managing their appointments and prescriptions.
- **Doctor Management**: Facilities to maintain doctor profiles, manage their schedules, and oversee their payroll information.
- **Appointment Scheduling**: Easy-to-use interface for receptionists to schedule, update, and view upcoming appointments.
- **Prescription Management**: Allows doctors to efficiently create and update prescriptions tied to patient visits.
- **Payroll Management**: Admin tools to handle payroll details for all clinic staff.

## Installation
Get started with our system in no time by following these steps:

1. **Clone The Repository:**
   ```bash
   git clone https://github.com/AhmedElBaramony/Clinic_Managment_System.git

2. **Install Dependencies:**
   ```bash
   pip install pypyodbc tkinter ttkbootstrap

3. **Database Setup:**
  - Initialize a SQL Server database using the SQL scripts provided.
  - Customize the *DB_Manager.py* file with your SQL Server details to connect to your database.

4. **Start Application:**
   Run *main.py* file to launch the application
   ```bash
   python main.py

## Configuration
Customize your database connection settings in DB_Manager.py to match your SQL Server configuration:

```python
def connect_to_database(driver, server, database):
    connection_string = f'''
        DRIVER={{{driver}}};
        SERVER={server};
        DATABASE={database};
        Trust_Connection=True;
    '''
    return odbc.connect(connection_string) 
