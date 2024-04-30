CREATE DATABASE Clinic_Management_System

USE Clinic_Management_System
GO

CREATE TABLE Patients (
    ID INT IDENTITY(1,1),
    Fname VARCHAR(255),
    Lname VARCHAR(255),
    sex VARCHAR(10),
    BirthDate DATE,
    age INT,
    phone VARCHAR(20),
    address VARCHAR(255),
    email VARCHAR(255),
	username VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL
	
	CONSTRAINT Patient_pk PRIMARY KEY(ID)
);

CREATE TABLE Insurance (
    Cname VARCHAR(255),
    CoverageDetails VARCHAR(255),
    CoverageType VARCHAR(255),
    Patient_ID INT,

	CONSTRAINT Insurance_pk PRIMARY KEY(Cname,Patient_ID),
    CONSTRAINT Insurance_Patient_fk FOREIGN KEY (Patient_ID) REFERENCES Patients(ID)
);

CREATE TABLE Prescriptions (
    ID INT IDENTITY(1,1),
    diagnosis VARCHAR(255),

	CONSTRAINT Prescription_pk PRIMARY KEY(ID)
);

CREATE TABLE Medications (
    ID INT IDENTITY(1,1),
    MedDuration INT,
    MedFreq INT,
    Med_Name VARCHAR(255),
    MedDosage FLOAT,
	prescription_ID INT,

	CONSTRAINT Medication_pk PRIMARY KEY(ID),
	CONSTRAINT medication_prescription_fk FOREIGN KEY(prescription_ID) REFERENCES Prescriptions(ID)
);


CREATE TABLE Clinics (
    ID INT IDENTITY(1,1),
    room INT,
    specialization VARCHAR(255),
    Working_Hours INT,
    InsuranceAccepted VARCHAR(255),

	CONSTRAINT Clinics_pk PRIMARY KEY(ID)
);

CREATE TABLE Bills (
    PaymentType VARCHAR(255),
    ID INT IDENTITY(1,1),
    amount FLOAT,
    Paymentstatus VARCHAR(255),

	CONSTRAINT Bills_pk PRIMARY KEY(ID)
);

CREATE TABLE Payrolls (
    ID INT IDENTITY(1,1),
    WorkingHours INT ,
    Salary FLOAT NULL,

	CONSTRAINT Payrolls_pk PRIMARY KEY(ID)
);

CREATE TABLE Receptionists (
    ID INT IDENTITY(1,1),
    Fname VARCHAR(255),
    Lname VARCHAR(255),
    sex VARCHAR(10),
    BirthDate DATE,
    age INT,
    phone VARCHAR(20),
    address VARCHAR(255),
    email VARCHAR(255),
    Payroll_ID INT,
	username VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL


	CONSTRAINT Receptionist_pk PRIMARY KEY(ID),
    CONSTRAINT Receptionist_Payroll_fk FOREIGN KEY (Payroll_ID) REFERENCES Payrolls(ID)
);

CREATE TABLE Doctors (
    ID INT IDENTITY(1,1),
    Fname VARCHAR(255),
    Lname VARCHAR(255),
    sex VARCHAR(10),
    BirthDate DATE,
    age INT,
    phone VARCHAR(20),
    address VARCHAR(255),
    email VARCHAR(255),
    specification VARCHAR(255),
    Clinic_ID INT,
    Payroll_ID INT,
	username VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL

	CONSTRAINT Doctors_pk PRIMARY KEY(ID),
    CONSTRAINT Doctor_Clinic_fk FOREIGN KEY (Clinic_ID) REFERENCES Clinics(ID),
    CONSTRAINT Doctor_Payroll_fk FOREIGN KEY (Payroll_ID) REFERENCES Payrolls(ID)
);

CREATE TABLE Appointments (
    ID INT IDENTITY(1,1),
    Prescription_ID INT NULL,
    Bill_ID INT,
    Doc_ID INT,
    Patient_ID INT,
    Date DATE,

	CONSTRAINT Appointments_pk PRIMARY KEY(ID),
    CONSTRAINT Appointments_Prescription_fk FOREIGN KEY (Prescription_ID) REFERENCES Prescriptions(ID),
    CONSTRAINT Appointments_Bills_fk FOREIGN KEY (Bill_ID) REFERENCES Bills(ID),
    CONSTRAINT Appointments_Doctors_fk FOREIGN KEY (Doc_ID) REFERENCES Doctors(ID),
    CONSTRAINT Appointments_Patients_fk FOREIGN KEY (Patient_ID) REFERENCES Patients(ID)
);


CREATE TABLE Reservations (
    Receptionist_ID INT,
    Appointment_ID INT,

	CONSTRAINT Reservation_pk PRIMARY KEY(Receptionist_ID,Appointment_ID),
    CONSTRAINT Reservation_Receptionist_fk FOREIGN KEY (Receptionist_ID) REFERENCES Receptionists(ID),
    CONSTRAINT Reservation_Appointment_fk FOREIGN KEY (Appointment_ID) REFERENCES Appointments(ID)
);

-- Inserting patients
INSERT INTO Patients (Fname, Lname, sex, BirthDate, age, phone, address, email, username, password)
VALUES 
('John', 'Doe', 'Male', '1990-01-01', 31, '1234567890', '123 Main St', 'john.doe@example.com', 'johndoe', 'johndoe'),
('Alice', 'Smith', 'Female', '1995-05-15', 29, '9876543210', '456 Pine St', 'alice.smith@example.com', 'alicesmith', 'alicesmith'),
('Emily', 'Jones', 'Female', '1987-03-12', 35, '5552223333', '789 Cedar St', 'emily.jones@example.com', 'emilyjones', 'emilyjones'),
('David', 'Wilson', 'Male', '1975-09-28', 47, '9998887777', '123 Oak St', 'david.wilson@example.com', 'davidwilson', 'davidwilson'),
('Sophia', 'Martinez', 'Female', '1992-11-05', 32, '7776665555', '456 Walnut St', 'sophia.martinez@example.com', 'sophiamartinez', 'sophiamartinez'),
('James', 'Taylor', 'Male', '1980-07-18', 41, '3334445555', '789 Birch St', 'james.taylor@example.com', 'jamestaylor', 'jamestaylor'),
('Olivia', 'Brown', 'Female', '1998-02-20', 26, '1112223333', '321 Maple St', 'olivia.brown@example.com', 'oliviabrown', 'oliviabrown'),
('Daniel', 'Anderson', 'Male', '1983-06-30', 40, '4445556666', '987 Elm St', 'daniel.anderson@example.com', 'danielanderson', 'danielanderson');



-- Inserting clinics
INSERT INTO Clinics(room, specialization, Working_Hours, InsuranceAccepted)
VALUES 
(101, 'General Medicine', 40, 'Blue Cross Blue Shield'),
(201, 'Pediatrics', 45, 'Aetna'),
(301, 'Dermatology', 50, 'Cigna'),
(401, 'Orthopedics', 45, 'UnitedHealthcare'),
(501, 'Cardiology', 40, 'Medicare'),
(601, 'Ophthalmology', 35, 'Aetna'),
(701, 'Gastroenterology', 55, 'Humana'),
(801, 'Obstetrics and Gynecology', 50, 'Blue Cross Blue Shield');

-- Inserting bills
INSERT INTO Bills (PaymentType, amount, Paymentstatus)
VALUES 
('Credit Card',50, 'Paid'),
('Cash',75, 'Pending'),
( 'Cash',60, 'Pending'),
( 'Credit Card',100, 'Paid'),
( 'Insurance', 20, 'Pending'),
( 'Cash',90, 'Paid'),
( 'Credit Card',80, 'Pending'),
( 'Insurance',50, 'Paid');

-- Inserting payrolls
INSERT INTO Payrolls (WorkingHours, Salary)
VALUES 
(40, 4000),
(35, 3500),
(30, 3000),
(45, 4500),
(35, 3500),
(40, 4000),
(50, 5000),
(55, 5500);

-- Inserting prescriptions
INSERT INTO Prescriptions (diagnosis)
VALUES 
('Headache'),
('Fever'),
('Strep Throat'),
('Hypertension'),
('GERD'),
('Hypercholesterolemia'),
('Asthma'),
('Type 2 Diabetes');

-- Inserting medications
INSERT INTO Medications (MedDuration, MedFreq, Med_Name, MedDosage,prescription_ID)
VALUES 
(7, 2, 'Ibuprofen', 200,2),
(10, 1, 'Paracetamol', 500,5),
(5, 3, 'Amoxicillin', 500,6),
(15, 1, 'Lisinopril', 10,3),
(7, 2, 'Omeprazole', 20,1),
(10, 1, 'Atorvastatin', 40,4),
(7, 3, 'Albuterol', 2,7),
(30, 1, 'Metformin', 1000,8),
(7, 2, 'Ibuprofen', 200,1),
(10, 1, 'Paracetamol', 500,2),
(5, 3, 'Amoxicillin', 500,3),
(15, 1, 'Lisinopril', 10,4),
(7, 2, 'Omeprazole', 20,5),
(10, 1, 'Atorvastatin', 40,6),
(7, 3, 'Albuterol', 2,7),
(30, 1, 'Metformin', 1000,8);

-- Inserting doctors with username and password
INSERT INTO Doctors (Fname, Lname, sex, BirthDate, age, phone, address, email, specification, Clinic_ID, Payroll_ID, username, password)
VALUES 
('Jane', 'Doe', 'Female', '1985-01-01', 36, '0987654321', '456 Elm St', 'jane.doe@example.com', 'General Practitioner', 1, 1, 'janedoe', 'password'),
('Michael', 'Johnson', 'Male', '1978-08-20', 46, '1234567890', '789 Maple St', 'michael.johnson@example.com', 'Pediatrician', 2, 2, 'michaeljohnson', 'password'),
('William', 'Moore', 'Male', '1972-04-15', 52, '5556667777', '123 Pine St', 'william.moore@example.com', 'Dermatologist', 3, 3, 'williammoore', 'password'),
('Elizabeth', 'Clark', 'Female', '1989-08-10', 32, '7778889999', '456 Oak St', 'elizabeth.clark@example.com', 'Orthopedic Surgeon', 4, 4, 'elizabethclark', 'password'),
('Alexander', 'Lewis', 'Male', '1970-12-25', 51, '1112223333', '789 Cedar St', 'alexander.lewis@example.com', 'Cardiologist', 5, 5, 'alexanderlewis', 'password'),
('Victoria', 'Walker', 'Female', '1982-06-02', 39, '4445556666', '321 Walnut St', 'victoria.walker@example.com', 'Ophthalmologist', 6, 6, 'victoriawalker', 'password'),
('Charles', 'Young', 'Male', '1975-03-20', 49, '8889990000', '987 Birch St', 'charles.young@example.com', 'Gastroenterologist', 7, 7, 'charlesyoung', 'password'),
('Emma', 'Hill', 'Female', '1986-11-12', 38, '2223334444', '654 Maple St', 'emma.hill@example.com', 'Obstetrician/Gynecologist', 8, 8, 'emmahill', 'password');


-- Inserting receptionists with username and password
INSERT INTO Receptionists (Fname, Lname, sex, BirthDate, age, phone, address, email, Payroll_ID, username, password)
VALUES 
('Bob', 'Smith', 'Male', '1995-01-01', 26, '5551234567', '789 Oak St', 'bob.smith@example.com', 1, 'bobsmith','admin'),
('Emily', 'Brown', 'Female', '1990-03-10', 34, '5559876543', '321 Oak St', 'emily.brown@example.com', 2, 'emilybrown','admin'),
('Nathan', 'Adams', 'Male', '1993-02-28', 31, '5554443333', '987 Pine St', 'nathan.adams@example.com', 4, 'nathanadams','admin'),
('Sophie', 'Baker', 'Female', '1996-05-18', 28, '3332221111', '654 Oak St', 'sophie.baker@example.com', 5, 'sophiebaker','admin'),
('Samuel', 'Miller', 'Male', '1984-09-05', 40, '8887776666', '321 Cedar St', 'samuel.miller@example.com', 6, 'samuelmiller','admin'),
('Ava', 'Harris', 'Female', '1991-07-22', 33, '6665554444', '789 Walnut St', 'ava.harris@example.com', 7, 'avaharris','admin'),
('Christopher', 'Wright', 'Male', '1997-11-30', 27, '2221110000', '456 Birch St', 'christopher.wright@example.com', 8, 'christopherwright','admin'),
('Madison', 'King', 'Female', '1990-04-14', 34, '9998887777', '123 Maple St', 'madison.king@example.com', 8, 'madisonking','admin');


-- Inserting insurance information
INSERT INTO Insurance (Cname, CoverageDetails, CoverageType, Patient_ID)
VALUES 
('Blue Cross Blue Shield', '80% coverage', 'PPO', 1),
('Aetna', '70% coverage', 'HMO', 2),
('Cigna', '60% coverage', 'PPO', 3),
('UnitedHealthcare', '90% coverage', 'HMO', 4),
('Medicare', '75% coverage', 'PPO', 5),
('Aetna', '80% coverage', 'HMO', 6),
('Humana', '85% coverage', 'PPO', 7),
('Blue Cross Blue Shield', '70% coverage', 'HMO', 8);

-- Inserting appointments
INSERT INTO Appointments (Prescription_ID, Bill_ID, Doc_ID, Patient_ID, Date)
VALUES 
(1, 1, 1, 1, '2022-01-01'),
(2, 2, 2, 2, '2022-01-05'),
(3, 3, 3, 3, '2022-01-10'),
(4, 4, 4, 4, '2022-01-15'),
(5, 5, 5, 5, '2022-01-20'),
(6, 6, 6, 6, '2022-01-25'),
(7, 7, 7, 7, '2022-01-30'),
(8, 8, 8, 8, '2022-02-05'),
(7, 2, 1, 5, '2022-01-12'), 
(3, 7, 8, 1, '2022-01-16'),
(5, 1, 6, 2, '2022-01-22'),
(6, 2, 4, 5, '2022-01-27'),
(7, 6, 4, 2, '2022-02-01'),
(8, 7, 1, 5, '2022-02-07');

-- Inserting reservations
INSERT INTO Reservations (Receptionist_ID, Appointment_ID)
VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(3, 9),
(4, 10),
(5, 11),
(6, 12),
(7, 13),
(8, 14);