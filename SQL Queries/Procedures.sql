-- Procedure for Patients table
CREATE PROCEDURE GetAllPatientsAttributes
AS
BEGIN
    SELECT *
    FROM Patients;
END;

-- Procedure for Medications table
CREATE PROCEDURE GetAllMedicationsAttributes
AS
BEGIN
    SELECT *
    FROM Medications;
END;

-- Procedure for Clinics table
CREATE PROCEDURE GetAllClinicsAttributes
AS
BEGIN
    SELECT *
    FROM Clinics;
END;

-- Procedure for Bills table
CREATE PROCEDURE GetAllBillsAttributes
AS
BEGIN
    SELECT *
    FROM Bills;
END;

SELECT Patients.Fname,Patients.Lname,Doctors.Fname,Doctors.Lname FROM
Patients,Appointments,Doctors WHERE Patients.ID = Appointments.ID AND Doctors.ID = Appointments.Doc_ID


SELECT count(*) FROM Patients,Appointments
WHERE
Patients.ID=Appointments.Patient_ID 
 

-- Procedure for Payrolls table
CREATE PROCEDURE GetAllPayrollsAttributes
AS
BEGIN
    SELECT *
    FROM Payrolls;
END;

-- Procedure for Prescriptions table
CREATE PROCEDURE GetAllPrescriptionsAttributes
AS
BEGIN
    SELECT *
    FROM Prescriptions;
END;

-- Procedure for Doctors table
CREATE PROCEDURE GetAllDoctorsAttributes
AS
BEGIN
    SELECT *
    FROM Doctors;
END;

-- Procedure for Receptionists table
CREATE PROCEDURE GetAllReceptionistsAttributes
AS
BEGIN
    SELECT *
    FROM Receptionists;
END;

-- Procedure for Insurance table
CREATE PROCEDURE GetAllInsuranceAttributes
AS
BEGIN
    SELECT *
    FROM Insurance;
END;

-- Procedure for Appointments table
CREATE PROCEDURE GetAllAppointmentsAttributes
AS
BEGIN
    SELECT *
    FROM Appointments;
END;

-- Procedure for Reservations table
CREATE PROCEDURE GetAllReservationsAttributes
AS
BEGIN
    SELECT *
    FROM Reservations;
END;


CREATE PROCEDURE create_appointment(
    @prescription AS INT = NULL,
    @doc AS INT,
    @patient AS INT,
    @date AS DATE,
    @receptionist AS INT,
    @paymenttype AS VARCHAR(255),
    @amount AS FLOAT,
    @paymentstatus AS VARCHAR(255) = 'Pending'
)
AS
BEGIN
    INSERT INTO Bills (PaymentType, amount, Paymentstatus)
    VALUES (@paymenttype, @amount, @paymentstatus);
	
    INSERT INTO Appointments (Prescription_ID, Bill_ID, Doc_ID, Patient_ID, Date)
    VALUES  (@prescription, (SELECT MAX(ID) FROM Bills), @doc, @patient, @date);
	
    INSERT INTO Reservations (Receptionist_ID, Appointment_ID)
    VALUES (@receptionist, (SELECT MAX(ID) FROM Appointments));
END;



CREATE PROCEDURE add_doctor(
    @fname VARCHAR(255),
    @lname VARCHAR(255),
    @sex VARCHAR(10),
    @bdate DATE,
    @age INT,
    @phone VARCHAR(20),
    @address VARCHAR(255),
    @email VARCHAR(255),
    @specification VARCHAR(255),
    @clinic_id INT = NULL,
    @payroll_id INT = NULL,
    @username VARCHAR(50),
    @password VARCHAR(50)
)
AS
BEGIN
    INSERT INTO Doctors (Fname,Lname,sex,BirthDate,age,phone,address,email,specification,Clinic_ID,Payroll_ID,username,password)
    VALUES (@fname,@lname,@sex,@bdate,@age,@phone,@address,@email,@specification,@clinic_id,@payroll_id,@username,@password);
END;


CREATE PROCEDURE GetDoctorByID(@DoctorID INT)
AS
BEGIN
    SELECT *
    FROM Doctors
    WHERE ID = @DoctorID;
END;

CREATE PROCEDURE add_patient
(
    @fname VARCHAR(255),
    @lname VARCHAR(255),
    @sex VARCHAR(10),
    @birthdate DATE,
    @age INT,
    @phone VARCHAR(20),
    @address VARCHAR(255),
    @email VARCHAR(255),
    @username VARCHAR(50),
    @password VARCHAR(50)
)
AS
BEGIN
    INSERT INTO Patients (Fname, Lname, sex, BirthDate, age, phone, address, email, username, password)
    VALUES (@fname, @lname, @sex, @birthdate, @age, @phone, @address, @email, @username, @password);
END;

CREATE PROCEDURE GetPatientByID (@PatientID INT)
AS
BEGIN
	SELECT * FROM Patients WHERE ID = @PatientID
END;

CREATE PROCEDURE ViewPrescriptionsPatients(@PatientID INT)
AS
BEGIN
    SELECT Prescriptions.ID,Prescriptions.diagnosis,Med_Name,MedFreq,MedDosage,MedDuration
    FROM Patients JOIN Appointments ON Patients.ID = Appointments.Patient_ID
	JOIN Prescriptions ON Prescriptions.ID= Appointments.Prescription_ID
	JOIN Medications ON Medications.prescription_ID=Prescriptions.ID
    WHERE Patients.ID = @PatientID
	ORDER BY Prescriptions.ID;
END;


CREATE PROCEDURE add_payroll
(
	@doc_id INT,
    @working_hours INT,
    @salary FLOAT
)
AS
BEGIN
    UPDATE Payrolls 
	SET
	WorkingHours = @working_hours, 
	Salary = @salary
	WHERE Payrolls.ID = (Select Doctors.Payroll_ID 
						 From Doctors
						 WHERE Doctors.ID = @doc_id);
END;


CREATE PROCEDURE add_new_payroll(
	@doc_id INT,
    @working_hours INT,
    @salary FLOAT
)
AS
BEGIN
	INSERT INTO Payrolls (WorkingHours, Salary)
    VALUES (@working_hours, @salary);

	UPDATE Doctors
	SET
	Payroll_ID = (SELECT MAX(ID) FROM Payrolls)
	WHERE Doctors.ID = @doc_id
END;


CREATE PROCEDURE Doctor_view(@doctor_id AS INT=1) 
AS
BEGIN
	SELECT Appointments.ID,Appointments.Date,
	Patients.Fname,Patients.Lname,
	Prescriptions.diagnosis,
	Bills.amount,Bills.Paymentstatus
	FROM Appointments
	join Doctors on Doc_ID=Doctors.ID
	left join Prescriptions on Appointments.Prescription_ID=Prescriptions.ID
	join Bills on Bill_ID = Bills.ID
	join Patients on Patient_ID = Patients.ID
	WHERE
	Doc_ID = @doctor_id
END;

-- these two procedure must be made after each other 

CREATE PROCEDURE prescription_add (@diagnosis AS VARCHAR(255),@apoint_id AS INT)
AS
BEGIN
	INSERT INTO Prescriptions (diagnosis)
	VALUES (@diagnosis);

	UPDATE Appointments
	SET Prescription_ID = (SELECT MAX(ID)FROM Prescriptions)
	WHERE Appointments.ID = @apoint_id;

END;

CREATE PROCEDURE GetPrescriptionByAppointID (@apoint_id AS INT)
AS
BEGIN
	SELECT Prescriptions.ID, Prescriptions.Diagnosis
	FROM Appointments JOIN Prescriptions ON Appointments.Prescription_ID = Prescriptions.ID
	WHERE Appointments.ID = @apoint_id;
END;


CREATE PROCEDURE GetMedicationByPrescriptionID (@presc_id AS INT)
AS
BEGIN
	SELECT Medications.ID, Medications.Med_Name, Medications.MedDosage, Medications.MedDuration, Medications.MedFreq
	FROM Medications JOIN Prescriptions ON Medications.prescription_ID = Prescriptions.ID
	WHERE Prescriptions.ID = @presc_id;
END;

CREATE PROCEDURE medication_add (@medduration AS INT,@medfreq AS INT,@medname AS VARCHAR(255),@meddosage AS FLOAT,@prescript_id AS INT =NULL)
AS
BEGIN 
    IF @prescript_id IS NULL
        SET @prescript_id = (SELECT MAX(ID) FROM Prescriptions);

	INSERT INTO Medications  (MedDuration,MedFreq,Med_Name,MedDosage,prescription_ID)
	VALUES (@medduration,@medfreq,@medname,@meddosage,@prescript_id)
END;

CREATE PROCEDURE ViewPrescriptionsDoctors(@DoctorsID INT)
AS
BEGIN
    SELECT Prescriptions.ID,Prescriptions.diagnosis,Med_Name,MedFreq,MedDosage,MedDuration
    FROM Doctors JOIN Appointments ON Doctors.ID = Appointments.Doc_ID
	JOIN Prescriptions ON Prescriptions.ID= Appointments.Prescription_ID
	JOIN Medications ON Medications.prescription_ID=Prescriptions.ID
    WHERE Doctors.ID = @DoctorsID 
	ORDER BY Prescriptions.ID;
END;

Create PROCEDURE view_payroll (@doc_id AS INT)
AS 
BEGIN
	SELECT Payroll_ID,WorkingHours,Salary FROM Payrolls 
	JOIN Doctors ON Payroll_ID=Payrolls.ID 
	where @doc_id=Doctors.ID
END;

CREATE PROCEDURE Patient_view(@patient_id AS INT=1) 
AS
BEGIN
	SELECT Appointments.ID,Appointments.Date,
	Doctors.Fname,Doctors.Lname,
	Prescriptions.diagnosis,
	Bills.amount,Bills.Paymentstatus
	FROM Appointments
	join Doctors on Appointments.Doc_ID=Doctors.ID
	left join Prescriptions on Appointments.Prescription_ID=Prescriptions.ID
	join Bills on Appointments.Bill_ID = Bills.ID
	WHERE 
	Appointments.Patient_ID = @patient_id
END;

CREATE PROCEDURE DoctorLogin
    (@Username VARCHAR(50),
    @Password VARCHAR(50))
AS
BEGIN
    SET NOCOUNT ON;

    SELECT ID AS DoctorID
    FROM Doctors
    WHERE username = @Username AND password = @Password;
END;

CREATE PROCEDURE PatientLogin
    (@Username VARCHAR(50),
    @Password VARCHAR(50))
AS
BEGIN
    SET NOCOUNT ON;

    SELECT ID AS PatientID
    FROM Patients
    WHERE username = @Username AND password = @Password;
END;

CREATE PROCEDURE ReceptionistLogin
    (@Username VARCHAR(50),
    @Password VARCHAR(50))
AS
BEGIN
    SET NOCOUNT ON;

    SELECT ID AS ReceptionistID
    FROM Receptionists
    WHERE username = @Username AND password = @Password;


	SELECT AVG(Salary) 
	FROM Receptionists join Payrolls
	on Receptionists.Payroll_ID = Payrolls.ID;

	SELECT Doc_ID ,count(*)

	As NumberofAppointment 

	From Appointments

	Groub bDoc_ID




