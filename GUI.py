import tkinter as tk
import ttkbootstrap as ttk
from DB_Manager import *
from tkinter import messagebox

cursor, conn = connect_to_database('SQL Server', 'AHMEDEL-BARAMON', 'Clinic_Management_System')

DIMENSIONS = '1000x800'

#Logic Done
class LoginPage:
    def __init__(self):
        self.usernameVar = tk.StringVar()
        self.passwordVar = tk.StringVar()
        self.content = tk.Frame(root)

        self.loginLabel = tk.Label(self.content, text="Login", font=("Helvetica", 18), padx=30, pady=30)
        self.loginLabel.pack()

        self.nameLabel = tk.Label(self.content, text='Username', font=('calibre', 10, 'bold'))
        self.nameText = tk.Entry(self.content, textvariable=self.usernameVar, font=('calibre', 10, 'normal'))

        self.passwLabel = tk.Label(self.content, text='Password', font=('calibre', 10, 'bold'))
        self.passwText = tk.Entry(self.content, textvariable=self.passwordVar, font=('calibre', 10, 'normal'),
                                  show='*')

        self.nameLabel.pack()
        self.nameText.pack()
        self.passwLabel.pack()
        self.passwText.pack()

        self.user_type = tk.StringVar()

        style = ttk.Style()
        style.configure("Custom.TRadiobutton", font=("Calibri", 10))

        self.receptRadio = ttk.Radiobutton(self.content, text="Receptionist", variable=self.user_type,
                                           value="Receptionist", style="Custom.TRadiobutton")
        self.doctorRadio = ttk.Radiobutton(self.content, text="Doctor", variable=self.user_type,
                                           value="Doctor", style="Custom.TRadiobutton")
        self.patientRadio = ttk.Radiobutton(self.content, text="Patient", variable=self.user_type,
                                            value="Patient", style="Custom.TRadiobutton")

        self.receptRadio.pack(pady=2)
        self.doctorRadio.pack(pady=2)
        self.patientRadio.pack(pady=2)

        self.submitBtn = tk.Button(self.content, text="Submit", command=self.submit)
        self.submitBtn.pack(padx=0, pady=10)

    def show_page(self):
        self.content.pack()

    def submit(self):
        global receptionistId, doctorId, patientId
        username = self.usernameVar.get()
        password = self.passwordVar.get()
        if username == "":
            username = "NA"
        if password == "":
            password = "NA"
        # real_pass = cursor.execute( procedureGetPasswordOfTheUsername{username} )
        if self.user_type.get() == "Receptionist":
            rows = execute_procedure(cursor, f'ReceptionistLogin {username},{password}')
            if rows:
                receptionistId = rows[0][0]
                self.nameText.delete(0, 'end')
                self.passwText.delete(0, 'end')
                self.content.pack_forget()
                receptionistPage.show_page()
            else:
                messagebox.showinfo("Error", "Invalid Credentials!")
        elif self.user_type.get() == "Doctor":
            rows = execute_procedure(cursor, f'DoctorLogin {username},{password}')
            if rows:
                doctorId = rows[0][0]
                self.nameText.delete(0, 'end')
                self.passwText.delete(0, 'end')
                self.content.pack_forget()
                doctorPage.show_page()
            else:
                messagebox.showinfo("Error", "Invalid Credentials!")
        elif self.user_type.get() == "Patient":
            rows = execute_procedure(cursor, f'PatientLogin {username},{password}')
            if rows:
                patientId = rows[0][0]
                self.nameText.delete(0, 'end')
                self.passwText.delete(0, 'end')
                self.content.pack_forget()
                viewPatientAppointmentPage.show_page()
            else:
                messagebox.showinfo("Error", "Invalid Credentials!")
        else:
            messagebox.showinfo("Error","Invalid Credentials!")


# '------------------------- Receptionist Services -------------------------'
#Logic Done
class ReceptionistPage:
    def __init__(self):
        self.content = tk.Frame(root)
        self.nameLabel = ttk.Label(self.content, text='Receptionist page')
        self.nameLabel.pack()

        self.reserveAppointmentsBtn = ttk.Button(self.content, text="Reserve Appointment", command=self.reserve)
        self.addDoctorBtn = ttk.Button(self.content, text="Add a doctor", command=self.addDoctor)
        self.viewDoctorBtn = ttk.Button(self.content, text="view a doctor", command=self.viewDoctor)
        self.addPatientBtn = ttk.Button(self.content, text="Add a patient", command=self.addPatient)
        self.viewPatientBtn = ttk.Button(self.content, text="View a patient", command=self.viewPatient)
        self.updatePayrollBtn = ttk.Button(self.content, text="Update payroll", command=self.updatePayroll)
        self.backBtn = ttk.Button(self.content, text="Back", command=self.back)

        self.reserveAppointmentsBtn.pack(pady=10)
        self.addDoctorBtn.pack(pady=10)
        self.viewDoctorBtn.pack(pady=10)
        self.addPatientBtn.pack(pady=10)
        self.viewPatientBtn.pack(pady=10)
        self.updatePayrollBtn.pack(pady=10)
        self.backBtn.pack(pady=10)

    def show_page(self):
        self.content.pack()

    def reserve(self):
        self.content.pack_forget()
        reserveAppointmentPage.show_page()

    def addDoctor(self):
        self.content.pack_forget()
        addDoctorPage.show_page()

    def viewDoctor(self):
        self.content.pack_forget()
        viewDoctorPage.show_page()

    def addPatient(self):
        self.content.pack_forget()
        addPatientPage.show_page()

    def viewPatient(self):
        self.content.pack_forget()
        viewPatientPage.show_page()

    def updatePayroll(self):
        self.content.pack_forget()
        updatePayrollPage.show_page()

    def back(self):
        self.content.pack_forget()
        loginPage.show_page()

#Logic Done
class AddDoctorPage:
    def __init__(self):

        self.content = tk.Frame(root)
        self.form = tk.Frame(self.content)
        ttk.Label(self.form, text="Add Doctor", font="calibre 20").pack(pady=20)

        # Entries and Labels for the form fields
        self.entries = {}
        fields = ["First Name", "Last Name", "Birth Date", "E-Mail", "Phone", "Address", "Specialization", "Sex",
                  "Username", "Password"]

        for field in fields:
            frame = tk.Frame(self.form)
            label = ttk.Label(frame, text=f"{field}: ", font=("calibre", 10, "bold"))
            label.pack(side="left", padx=20)
            frame.pack(fill="both", expand=True, padx=20, pady=5)
            if field == "Sex":
                self.sex_var = tk.StringVar()
                ttk.Radiobutton(frame, text="Female", variable=self.sex_var, value="Female").pack(side="right", padx=10)
                ttk.Radiobutton(frame, text="Male", variable=self.sex_var, value="Male").pack(side="right")
                self.sex_var.set("Male")  # Set default value
                frame.pack(fill="both", expand=True, padx=20, pady=5)
                continue
            entry = ttk.Entry(frame)
            entry.pack(side="right")
            self.entries[field] = entry  # Save the entry


        self.btnsFrame = ttk.Frame(self.content)

        # Submit Button
        submit_btn = ttk.Button(self.btnsFrame, text="Submit", command=self.submit)
        submit_btn.pack(pady=10, side="left", padx = 30)

        # Back Button
        back_btn = ttk.Button(self.btnsFrame, text="Back", command=self.back)
        back_btn.pack(pady=10)

        self.form.pack()
        self.btnsFrame.pack()


    def show_page(self):
        self.content.pack()


    def submit(self):
        # Here, you would collect all the data from the entries, validate it, and then either insert it into the database or raise a validation error.
        doctor_data = {field: entry.get() for field, entry in self.entries.items()}
        doctor_data["Sex"] = self.sex_var.get()  # Get the value of the selected sex
        # TODO: Insert data into database

        print("Submitted Data:", doctor_data)  # This is for debugging, remove in production

        try:
            execute_insert_procedure(cursor, conn, f'add_doctor \'{doctor_data["First Name"]}\',\'{doctor_data["Last Name"]}\', \'{doctor_data["Sex"]}\',\'{doctor_data["Birth Date"]}\',{calculate_age(doctor_data["Birth Date"])},\'{doctor_data["Phone"]}\',\'{doctor_data["Address"]}\',\'{doctor_data["E-Mail"]}\',\'{doctor_data["Specialization"]}\',null,null,\'{doctor_data["Username"]}\',\'{doctor_data["Password"]}\'')

            messagebox.showinfo('Info', "Doctor added successfully!")
        except Exception:
            messagebox.showinfo('Error', "Please enter valid data!")


    def back(self):
        self.content.pack_forget()
        receptionistPage.show_page()

#Logic Done
class AddPatientPage:

    def __init__(self):

        self.content = tk.Frame(root)
        self.form = tk.Frame(self.content)
        ttk.Label(self.form, text="Add Patient", font="calibre 20").pack(pady=20)

        # Entries and Labels for the form fields
        self.entries = {}
        fields = ["First Name", "Last Name", "Birth Date", "E-Mail", "Phone", "Address", "Sex",
                  "Username", "Password"]

        for field in fields:
            frame = tk.Frame(self.form)
            label = ttk.Label(frame, text=f"{field}: ", font=("calibre", 10, "bold"))
            label.pack(side="left", padx=20)
            frame.pack(fill="both", expand=True, padx=20, pady=5)
            if field == "Sex":
                self.sex_var = tk.StringVar()
                ttk.Radiobutton(frame, text="Female", variable=self.sex_var, value="Female").pack(side="right", padx=10)
                ttk.Radiobutton(frame, text="Male", variable=self.sex_var, value="Male").pack(side="right")
                self.sex_var.set("Male")  # Set default value
                frame.pack(fill="both", expand=True, padx=20, pady=5)
                continue
            entry = ttk.Entry(frame)
            entry.pack(side="right")
            self.entries[field] = entry  # Save the entry

        self.btnsFrame = ttk.Frame(self.content)

        # Submit Button
        submit_btn = ttk.Button(self.btnsFrame, text="Submit", command=self.submit)
        submit_btn.pack(pady=10, side="left", padx=30)

        # Back Button
        back_btn = ttk.Button(self.btnsFrame, text="Back", command=self.back)
        back_btn.pack(pady=10)

        self.form.pack()
        self.btnsFrame.pack()

    def show_page(self):
        self.content.pack()

    def submit(self):

        patient_data = {field: entry.get() for field, entry in self.entries.items()}
        patient_data["Sex"] = self.sex_var.get()

        print("Submitted Data:", patient_data)

        try:
            execute_insert_procedure(cursor, conn, f'add_patient \'{patient_data["First Name"]}\',\'{patient_data["Last Name"]}\', \'{patient_data["Sex"]}\',\'{patient_data["Birth Date"]}\',{calculate_age(patient_data["Birth Date"])},\'{patient_data["Phone"]}\',\'{patient_data["Address"]}\',\'{patient_data["E-Mail"]}\',\'{patient_data["Username"]}\',\'{patient_data["Password"]}\'')

            messagebox.showinfo('Info', "Patient added successfully!")
        except Exception:
            messagebox.showinfo('Error', "Please enter valid data!")

    def back(self):
        self.content.pack_forget()
        receptionistPage.show_page()

#Logic Done
class ReserveAppointmentPage:
    def __init__(self):
        # Content Frame
        self.content = tk.Frame(root)
        ttk.Label(self.content, text="Appointment Details: ", font="calibre 20").pack(pady=20)

        # Date Frame
        self.dateVar = tk.StringVar()
        self.dateFrame = tk.Frame(self.content)
        ttk.Label(self.dateFrame, text="Date: ").pack(side="left", padx=20)
        self.dateText = ttk.Entry(self.dateFrame, textvariable=self.dateVar)
        self.dateText.pack(side='left', padx=10)

        # Doctors Frame
        self.doctorSelected = -1
        self.doctorsLabel = ttk.Label(self.content, text="Choose a doctor")
        columns = ['ID', 'Name', 'Specialization']
        self.doctorsView = ttk.Treeview(self.content, columns=columns)
        for col in columns:
            self.doctorsView.heading(col, text=col, anchor='w')

        self.doctorsView.bind("<<TreeviewSelect>>", self.on_select)

        # Patient Id Frame
        self.patientIdVar = tk.IntVar()
        self.patientIdFrame = tk.Frame(self.content)
        ttk.Label(self.patientIdFrame, text="Patient Id: ").pack(side="left", padx=15)
        self.pIdText = ttk.Entry(self.patientIdFrame, textvariable=self.patientIdVar)
        self.pIdText.pack(side='left', padx=10)

        # Amount Frame
        self.amountVar = tk.StringVar()
        self.amountFrame = tk.Frame(self.content)
        ttk.Label(self.amountFrame, text="Amount: ").pack(side="left", padx=20)
        self.aText = ttk.Entry(self.amountFrame, textvariable=self.amountVar)
        self.aText.pack(side='left', padx=10)

        # Choose Payment method Frame
        self.paymentFrame = tk.Frame(self.content)
        types = ['Cash', 'Credit Card', 'Debit Card']
        self.typeVar = tk.StringVar(value=types[0])
        ttk.Label(self.paymentFrame, text="Payment Type: ").pack(side="left")
        self.paymentText = ttk.Combobox(self.paymentFrame, textvariable=self.typeVar)
        self.paymentText['values'] = types
        self.paymentText.pack(side='left', padx=10)

        # Buttons Frame
        self.btnFrame = tk.Frame(self.content)
        ttk.Button(self.btnFrame, text="Submit", command=self.submit).pack(side='top', padx=30)
        ttk.Button(self.btnFrame, text="Back", command=self.back).pack(side='right', padx=30)

        # Pack all items
        self.dateFrame.pack(expand=True, fill='both', pady=20)
        self.doctorsLabel.pack(pady=20)
        self.doctorsView.pack(fill="both", expand=False)
        self.patientIdFrame.pack(expand=True, fill='both', pady=20)
        self.amountFrame.pack(expand=True, fill='both', pady=20)
        self.paymentFrame.pack(expand=True, fill='both', pady=20)
        self.btnFrame.pack(expand=True, fill='both', pady=20)

    def show_page(self):
        self.content.pack()
        rows = execute_procedure(cursor, 'GetAllDoctorsAttributes')
        if rows:
            for item in self.doctorsView.get_children():
                self.doctorsView.delete(item)

            for row in rows:
                self.doctorsView.insert("", "end", values=(row[0], row[1] + ' ' + row[2], row[9]))

    def on_select(self, event):
        selected = self.doctorsView.selection()[0]
        self.doctorSelected = self.doctorsView.item(selected)['values'][0]

    def submit(self):
        try:
            execute_insert_procedure(cursor, conn, f'create_appointment null, {self.doctorSelected}, {self.patientIdVar.get()},'
                                               f' \'{self.dateVar.get()}\', {receptionistId}, \'{self.typeVar.get()}\', '
                                               f'{self.amountVar.get()}, \'pending\'')
            print(f'create_appointment null, {self.doctorSelected}, {self.patientIdVar.get()},'
                                               f' \'{self.dateVar.get()}\', {receptionistId}, \'{self.typeVar.get()}\', '
                                               f'{self.amountVar.get()}, \'pending\'')
            messagebox.showinfo('Info', "Appointment added successfully!")
        except Exception:
            messagebox.showinfo('Error', "Please enter valid data!")

    def back(self):
        self.content.pack_forget()
        receptionistPage.show_page()

#Logic Done
class UpdatePayrollPage:
    def _init_(self):
        self.docId = -1
        self.content = tk.Frame(root)
        ttk.Label(self.content, text="View Payroll", font="Calibre 40").pack()

        self.doctorIdVar = tk.IntVar()
        self.doctorIdFrame = tk.Frame(self.content)
        ttk.Label(self.doctorIdFrame, text="Doctor Id: ", font="Calibre 20").pack(side='left')
        self.doctorIdText = ttk.Entry(self.doctorIdFrame, textvariable=self.doctorIdVar)
        self.doctorIdText.pack(side='left', padx='30')
        self.submitBtn = ttk.Button(self.doctorIdFrame, text="Submit", command=self.submit)
        self.submitBtn.pack(side='right')

        self.workingHrsVar = tk.StringVar()
        self.workingHrsFrame = tk.Frame(self.content)
        ttk.Label(self.workingHrsFrame, text="Working hours: ", font="Calibre 20").pack(side='left')
        self.workingHrsText = ttk.Entry(self.workingHrsFrame, textvariable=self.workingHrsVar)
        self.workingHrsText.pack(side='right')

        self.salaryVar = tk.StringVar()
        self.salaryFrame = tk.Frame(self.content)
        ttk.Label(self.salaryFrame, text="Salary: ", font="Calibre 20").pack(side='left')
        self.salaryText = ttk.Entry(self.salaryFrame, textvariable=self.salaryVar)
        self.salaryText.pack(side='right')

        self.btnsFrame = tk.Frame(self.content)
        self.insertBtn = ttk.Button(self.btnsFrame, text="Insert", command=self.insert)
        self.backBtn = ttk.Button(self.btnsFrame, text="Back", command=self.back)
        self.backBtn.pack(side='left', padx=40)

        self.doctorIdFrame.pack(fill='both', expand=True, pady=50)
        self.btnsFrame.pack(pady=30)

    def show_page(self):
        self.content.pack(pady=50)

    def submit(self):
        try:
            self.docId = self.doctorIdVar.get()
            rows = execute_procedure(cursor, f'GetDoctorByID {self.docId}')
            if rows:
                self.btnsFrame.pack_forget()
                self.backBtn.pack_forget()
                self.workingHrsFrame.pack(fill='both', expand=True)
                self.salaryFrame.pack(fill='both', expand=True, pady=50)
                self.insertBtn.pack(side='left', padx=40)
                self.backBtn.pack(side='left', padx=40)
                self.btnsFrame.pack(pady=30)
            else:
                self.insertBtn.pack_forget()
                self.workingHrsFrame.pack_forget()
                self.salaryFrame.pack_forget()
                messagebox.showinfo("Error", "Please Enter a Valid ID!")
        except Exception:
            self.insertBtn.pack_forget()
            self.workingHrsFrame.pack_forget()
            self.salaryFrame.pack_forget()
            messagebox.showinfo("Error", "Please Enter a Valid ID!")

    def insert(self):
        salary = self.salaryVar.get()
        workingHrs = self.workingHrsVar.get()
        payrollId = execute_procedure(cursor, f'GetDoctorByID {self.docId}')[0][11]
        if payrollId:
            try:
                execute_insert_procedure(cursor, conn, f'add_payroll {self.docId}, {workingHrs}, {salary}')
                messagebox.showinfo("Info", "Payroll Updated successfully!")
            except Exception:
                messagebox.showinfo("Error", "Please Enter Valid data!")
        else:
            try:
                execute_insert_procedure(cursor, conn, f'add_new_payroll {self.docId}, {workingHrs}, {salary}')
                messagebox.showinfo("Info", "Payroll added successfully!")
            except Exception:
                messagebox.showinfo("Error", "Please Enter Valid data!")

    def back(self):
        self.content.pack_forget()
        receptionistPage.show_page()


#Logic Done
class ViewDoctorPage:
    def __init__(self):
        self.content = tk.Frame(root)
        ttk.Label(self.content, text="View Doctor", font="Calibre 20").pack(pady=20)

        # Doctor ID Frame
        self.doctorIdVar = tk.IntVar()
        self.doctorIdFrame = tk.Frame(self.content)
        ttk.Label(self.doctorIdFrame, text="Doctor Id: ", font="Calibre 15").pack(side='left')
        self.doctorIdText = ttk.Entry(self.doctorIdFrame, textvariable=self.doctorIdVar)
        self.doctorIdText.pack(side='left', padx=40)
        self.submitBtn = ttk.Button(self.doctorIdFrame, text="Submit", command=self.submit)
        self.submitBtn.pack(side='left', padx=50)

        # Details Frame
        self.fNameVar = tk.StringVar()
        self.lNameVar = tk.StringVar()
        self.dateVar = tk.StringVar()
        self.emailVar = tk.StringVar()
        self.usernameVar = tk.StringVar()
        self.phoneVar = tk.StringVar()
        self.addressVar = tk.StringVar()
        self.specializationVar = tk.StringVar()
        self.sexVar = tk.StringVar()
        self.passwordVar = tk.StringVar()

        # Details Variables
        self.detailsFrame = tk.Frame(self.content)

        self.frame1 = tk.Frame(self.detailsFrame)
        self.frame1.pack(side='left', padx=30, pady=20, fill='both', expand=True)

        self.frame2 = tk.Frame(self.detailsFrame)
        self.frame2.pack(side='left', padx=60, pady=20, fill='both', expand=True)

        # Fname Frame
        self.fNameFrame = tk.Frame(self.frame1)
        ttk.Label(self.fNameFrame, text="First name: ", font="Calibre 15").pack(side='left')
        self.fNameText = ttk.Label(self.fNameFrame, font="Calibre 15", textvariable=self.fNameVar)
        self.fNameText.pack(side='right')
        self.fNameFrame.pack(fill='both', expand=True)

        # Lname Frame
        self.lNameFrame = tk.Frame(self.frame1)
        ttk.Label(self.lNameFrame, text="Last name: ", font="Calibre 15").pack(side='left')
        self.lNameText = ttk.Label(self.lNameFrame, font="Calibre 15", textvariable=self.lNameVar)
        self.lNameText.pack(side='right')
        self.lNameFrame.pack(fill='both', expand=True)

        # Date Frame
        self.dateFrame = tk.Frame(self.frame1)
        ttk.Label(self.dateFrame, text="Birth date:", font="Calibre 15").pack(side='left')
        self.dateText = ttk.Label(self.dateFrame, font="Calibre 15", textvariable=self.dateVar)
        self.dateText.pack(side='right')
        self.dateFrame.pack(fill='both', expand=True)

        # Email Frame
        self.emailFrame = tk.Frame(self.frame1)
        ttk.Label(self.emailFrame, text="Email: ", font="Calibre 15").pack(side='left')
        self.emailText = ttk.Label(self.emailFrame, font="Calibre 15", textvariable=self.emailVar)
        self.emailText.pack(side='right')
        self.emailFrame.pack(fill='both', expand=True)

        # username Frame
        self.usernameFrame = tk.Frame(self.frame1)
        ttk.Label(self.usernameFrame, text="username: ", font="Calibre 15").pack(side='left')
        self.usernameText = ttk.Label(self.usernameFrame, font="Calibre 15", textvariable=self.usernameVar)
        self.usernameText.pack(side='right')
        self.usernameFrame.pack(fill='both', expand=True)

        # phone Frame
        self.phoneFrame = tk.Frame(self.frame2)
        ttk.Label(self.phoneFrame, text="Phone: ", font="Calibre 15").pack(side='left')
        self.phoneText = ttk.Label(self.phoneFrame, font="Calibre 15", textvariable=self.phoneVar)
        self.phoneText.pack(side='right')
        self.phoneFrame.pack(fill='both', expand=True)

        # address Frame
        self.addressFrame = tk.Frame(self.frame2)
        ttk.Label(self.addressFrame, text="Address: ", font="Calibre 15").pack(side='left')
        self.addressText = ttk.Label(self.addressFrame, font="Calibre 15", textvariable=self.addressVar)
        self.addressText.pack(side='right')
        self.addressFrame.pack(fill='both', expand=True)

        # specialization Frame
        self.specializationFrame = tk.Frame(self.frame2)
        ttk.Label(self.specializationFrame, text="Specialization: ", font="Calibre 15").pack(side='left')
        self.specializationText = ttk.Label(self.specializationFrame, font="Calibre 15",
                                            textvariable=self.specializationVar)
        self.specializationText.pack(side='right')
        self.specializationFrame.pack(fill='both', expand=True)

        # sex Frame
        self.sexFrame = tk.Frame(self.frame2)
        ttk.Label(self.sexFrame, text="Sex: ", font="Calibre 15").pack(side='left')
        self.sexText = ttk.Label(self.sexFrame, font="Calibre 15", textvariable=self.sexVar)
        self.sexText.pack(side='right')
        self.sexFrame.pack(fill='both', expand=True)

        # password Frame
        self.passwordFrame = tk.Frame(self.frame2)
        ttk.Label(self.passwordFrame, text="Password: ", font="Calibre 15").pack(side='left')
        self.passwordText = ttk.Label(self.passwordFrame, font="Calibre 15", textvariable=self.passwordVar)
        self.passwordText.pack(side='right')
        self.passwordFrame.pack(fill='both', expand=True)

        # Appointments Tree-view
        self.appointmentSelected = -1
        self.appointmentsFrame = tk.Frame(self.content)

        columns = ('Appointment ID', 'Date', 'Patient', 'Diagnosis', 'Amount')
        self.appointmentsTreeView = ttk.Treeview(self.appointmentsFrame, columns=columns)
        for i, col in enumerate(columns):
            self.appointmentsTreeView.heading(col, text=col, anchor='w')
        for col in columns:
            self.appointmentsTreeView.column(col, width=100)
        self.appointmentsTreeView.pack(fill='both', expand=True)

        self.appointmentsTreeView.bind("<<TreeviewSelect>>", self.on_select)

        # Buttons Frame
        self.btnsFrame = tk.Frame(self.content)
        self.viewPrescriptionBtn = ttk.Button(self.btnsFrame, text="View Prescription", command=self.view_presc)
        self.backBtn = ttk.Button(self.btnsFrame, text="Back", command=self.back)
        self.backBtn.pack(side='right')

        # Pack everything
        self.doctorIdFrame.pack(pady=50, padx=200, fill='both', expand=True)
        self.btnsFrame.pack(fill='both', expand=True, padx=100, pady=10)

        self.fNameVar.set('label')
        self.lNameVar.set('label')
        self.dateVar.set('label')
        self.emailVar.set('label')
        self.usernameVar.set('label')
        self.phoneVar.set('label')
        self.addressVar.set('label')
        self.specializationVar.set('label')
        self.sexVar.set('label')
        self.passwordVar.set('label')

    def show_page(self):
        self.content.pack()

    def submit(self):
        try:
            docId = self.doctorIdVar.get()
            docDetails = execute_procedure(cursor, f'GetDoctorByID {docId}')
            appointments = execute_procedure(cursor, f'Doctor_view {docId}')
            if docDetails:  # Call the procedure
                self.btnsFrame.pack_forget()
                self.detailsFrame.pack(fill='both', expand=True)
                self.appointmentsFrame.pack(fill='both', expand=True, pady=30)
                self.viewPrescriptionBtn.pack(side='right', padx=300)
                self.btnsFrame.pack(fill='both', expand=True, padx=100, pady=10)
                print(docId)

                self.fNameVar.set(docDetails[0][1])
                self.lNameVar.set(docDetails[0][2])
                self.sexVar.set(docDetails[0][3])
                self.dateVar.set(docDetails[0][4])
                self.phoneVar.set(docDetails[0][6])
                self.addressVar.set(docDetails[0][7])
                self.emailVar.set(docDetails[0][8])
                self.specializationVar.set(docDetails[0][9])
                self.usernameVar.set(docDetails[0][12])
                self.passwordVar.set(docDetails[0][13])

                for item in self.appointmentsTreeView.get_children():
                    self.appointmentsTreeView.delete(item)

                for appointment in appointments:
                    self.appointmentsTreeView.insert("", "end", values=(appointment[0], appointment[1],
                                                                        appointment[2] + ' ' + appointment[3],
                                                                        appointment[4], appointment[5]))
            else:
                self.detailsFrame.pack_forget()
                self.appointmentsFrame.pack_forget()
                self.viewPrescriptionBtn.pack_forget()
                messagebox.showinfo("Error", "Please Enter a Valid ID!")
        except Exception:
            self.detailsFrame.pack_forget()
            self.appointmentsFrame.pack_forget()
            self.viewPrescriptionBtn.pack_forget()
            messagebox.showinfo("Error", "Please Enter a Valid ID!")

    def on_select(self, event):
        selected = self.appointmentsTreeView.selection()[0]
        self.appointmentSelected = self.appointmentsTreeView.item(selected)['values'][0]
        print(self.appointmentSelected)

    def view_presc(self):
        # Open a window of prescription
        pass

    def back(self):
        self.content.pack_forget()
        receptionistPage.show_page()


class ViewPatientPage:
    def __init__(self):
        self.content = tk.Frame(root)
        ttk.Label(self.content, text="View Patient", font="Calibre 20").pack(pady=20)

        # Doctor ID Frame
        self.doctorIdVar = tk.IntVar()
        self.doctorIdFrame = tk.Frame(self.content)
        ttk.Label(self.doctorIdFrame, text="Patient Id: ", font="Calibre 15").pack(side='left')
        self.doctorIdText = ttk.Entry(self.doctorIdFrame, textvariable=self.doctorIdVar)
        self.doctorIdText.pack(side='left', padx=40)
        self.submitBtn = ttk.Button(self.doctorIdFrame, text="Submit", command=self.submit)
        self.submitBtn.pack(side='left', padx=50)

        # Details Frame
        self.fNameVar = tk.StringVar()
        self.lNameVar = tk.StringVar()
        self.dateVar = tk.StringVar()
        self.emailVar = tk.StringVar()
        self.usernameVar = tk.StringVar()
        self.phoneVar = tk.StringVar()
        self.addressVar = tk.StringVar()
        self.sexVar = tk.StringVar()
        self.passwordVar = tk.StringVar()

        # Details Variables
        self.detailsFrame = tk.Frame(self.content)

        self.frame1 = tk.Frame(self.detailsFrame)
        self.frame1.pack(side='left', padx=30, pady=20, fill='both', expand=True)

        self.frame2 = tk.Frame(self.detailsFrame)
        self.frame2.pack(side='left', padx=60, pady=20, fill='both', expand=True)

        # Fname Frame
        self.fNameFrame = tk.Frame(self.frame1)
        ttk.Label(self.fNameFrame, text="First name: ", font="Calibre 15").pack(side='left')
        self.fNameText = ttk.Label(self.fNameFrame, font="Calibre 15", textvariable=self.fNameVar)
        self.fNameText.pack(side='right')
        self.fNameFrame.pack(fill='both', expand=True)

        # Lname Frame
        self.lNameFrame = tk.Frame(self.frame1)
        ttk.Label(self.lNameFrame, text="Last name: ", font="Calibre 15").pack(side='left')
        self.lNameText = ttk.Label(self.lNameFrame, font="Calibre 15", textvariable=self.lNameVar)
        self.lNameText.pack(side='right')
        self.lNameFrame.pack(fill='both', expand=True)

        # Date Frame
        self.dateFrame = tk.Frame(self.frame1)
        ttk.Label(self.dateFrame, text="Birth date:", font="Calibre 15").pack(side='left')
        self.dateText = ttk.Label(self.dateFrame, font="Calibre 15", textvariable=self.dateVar)
        self.dateText.pack(side='right')
        self.dateFrame.pack(fill='both', expand=True)

        # Email Frame
        self.emailFrame = tk.Frame(self.frame1)
        ttk.Label(self.emailFrame, text="Email: ", font="Calibre 15").pack(side='left')
        self.emailText = ttk.Label(self.emailFrame, font="Calibre 15", textvariable=self.emailVar)
        self.emailText.pack(side='right')
        self.emailFrame.pack(fill='both', expand=True)

        # username Frame
        self.usernameFrame = tk.Frame(self.frame1)
        ttk.Label(self.usernameFrame, text="username: ", font="Calibre 15").pack(side='left')
        self.usernameText = ttk.Label(self.usernameFrame, font="Calibre 15", textvariable=self.usernameVar)
        self.usernameText.pack(side='right')
        self.usernameFrame.pack(fill='both', expand=True)

        # phone Frame
        self.phoneFrame = tk.Frame(self.frame2)
        ttk.Label(self.phoneFrame, text="Phone: ", font="Calibre 15").pack(side='left')
        self.phoneText = ttk.Label(self.phoneFrame, font="Calibre 15", textvariable=self.phoneVar)
        self.phoneText.pack(side='right')
        self.phoneFrame.pack(fill='both', expand=True)

        # address Frame
        self.addressFrame = tk.Frame(self.frame2)
        ttk.Label(self.addressFrame, text="Address: ", font="Calibre 15").pack(side='left')
        self.addressText = ttk.Label(self.addressFrame, font="Calibre 15", textvariable=self.addressVar)
        self.addressText.pack(side='right')
        self.addressFrame.pack(fill='both', expand=True)

        # sex Frame
        self.sexFrame = tk.Frame(self.frame2)
        ttk.Label(self.sexFrame, text="Sex: ", font="Calibre 15").pack(side='left')
        self.sexText = ttk.Label(self.sexFrame, font="Calibre 15", textvariable=self.sexVar)
        self.sexText.pack(side='right')
        self.sexFrame.pack(fill='both', expand=True)

        # password Frame
        self.passwordFrame = tk.Frame(self.frame2)
        ttk.Label(self.passwordFrame, text="Password: ", font="Calibre 15").pack(side='left')
        self.passwordText = ttk.Label(self.passwordFrame, font="Calibre 15", textvariable=self.passwordVar)
        self.passwordText.pack(side='right')
        self.passwordFrame.pack(fill='both', expand=True)

        # Appointments Tree-view
        self.appointmentsFrame = tk.Frame(self.content)

        self.appointmentSelected = -1
        columns = ('Appointment ID', 'Date', 'Doctor', 'Diagnosis', 'Amount')
        self.appointmentsTreeView = ttk.Treeview(self.appointmentsFrame, columns=columns)
        for i, col in enumerate(columns):
            self.appointmentsTreeView.heading(col, text=col, anchor='w')
        for col in columns:
            self.appointmentsTreeView.column(col, width=100)
        self.appointmentsTreeView.pack(fill='both', expand=True)

        # Buttons Frame
        self.btnsFrame = tk.Frame(self.content)
        self.viewPrescriptionBtn = ttk.Button(self.btnsFrame, text="View Prescription", command=self.view_presc)
        self.backBtn = ttk.Button(self.btnsFrame, text="Back", command=self.back)
        self.backBtn.pack(side='right')

        # Pack everything
        self.doctorIdFrame.pack(pady=50, padx=200, fill='both', expand=True)
        self.btnsFrame.pack(fill='both', expand=True, padx=100, pady=10)

        self.fNameVar.set('label')
        self.lNameVar.set('label')
        self.dateVar.set('label')
        self.emailVar.set('label')
        self.usernameVar.set('label')
        self.phoneVar.set('label')
        self.addressVar.set('label')
        self.sexVar.set('label')
        self.passwordVar.set('label')

    def show_page(self):
        self.content.pack()

    def submit(self):
        try:
            patId = self.doctorIdVar.get()
            patDetails = execute_procedure(cursor, f'GetPatientByID {patId}')
            appointments = execute_procedure(cursor, f'Patient_view {patId}')
            if patDetails:  # Call the procedure
                self.btnsFrame.pack_forget()
                self.detailsFrame.pack(fill='both', expand=True)
                self.appointmentsFrame.pack(fill='both', expand=True, pady=30)
                self.viewPrescriptionBtn.pack(side='right', padx=300)
                self.btnsFrame.pack(fill='both', expand=True, padx=100, pady=10)
                print(patId)

                self.fNameVar.set(patDetails[0][1])
                self.lNameVar.set(patDetails[0][2])
                self.sexVar.set(patDetails[0][3])
                self.dateVar.set(patDetails[0][4])
                self.phoneVar.set(patDetails[0][6])
                self.addressVar.set(patDetails[0][7])
                self.emailVar.set(patDetails[0][8])
                self.usernameVar.set(patDetails[0][9])
                self.passwordVar.set(patDetails[0][10])

                for item in self.appointmentsTreeView.get_children():
                    self.appointmentsTreeView.delete(item)

                for appointment in appointments:
                    self.appointmentsTreeView.insert("", "end", values=(appointment[0], appointment[1],
                                                                        appointment[2] + ' ' + appointment[3],
                                                                        appointment[4], appointment[5]))
            else:
                self.detailsFrame.pack_forget()
                self.appointmentsFrame.pack_forget()
                self.viewPrescriptionBtn.pack_forget()
                messagebox.showinfo("Error", "Please Enter a Valid ID!")
        except Exception:
            self.detailsFrame.pack_forget()
            self.appointmentsFrame.pack_forget()
            self.viewPrescriptionBtn.pack_forget()
            messagebox.showinfo("Error", "Please Enter a Valid ID!")

    def on_select(self, event):
        selected = self.appointmentsTreeView.selection()[0]
        self.appointmentSelected = self.appointmentsTreeView.item(selected)['values'][0]
        print(self.appointmentSelected)

    def view_presc(self):
        # Open a window of prescription
        pass

    def back(self):
        self.content.pack_forget()
        receptionistPage.show_page()



class ViewPrescriptionPage:
    def __init__(self):
        self.content = tk.Frame(root)
        self.form = tk.Frame(self.content)
        ttk.Label(self.form, text="View Prescription", font=("calibre", 20)).pack(pady=20)

        # Diagnosis Display
        self.diagnosisFrame = tk.Frame(self.form)
        ttk.Label(self.diagnosisFrame, text="Diagnosis: ", font=("calibre", 10, "bold")).pack(side="left", padx=20)
        self.diagnosisVar = tk.StringVar()
        ttk.Label(self.diagnosisFrame, textvariable=self.diagnosisVar, font=("calibre", 10)).pack(side="right", padx=20)
        self.diagnosisFrame.pack(fill="x", expand=True, padx=20, pady=5)


        # Medications Treeview
        self.medicationFrame = tk.Frame(self.form)
        ttk.Label(self.medicationFrame, text="Medications", font=("calibre", 18)).pack(pady=10)

        # Define the columns
        self.columns = ("Name", "Dosage", "Frequency", "Duration")
        self.medicationTreeview = ttk.Treeview(self.medicationFrame, columns=self.columns, show="headings")
        for col in self.columns:
            self.medicationTreeview.heading(col, text=col)
            self.medicationTreeview.column(col, width=100)

        # Add a scrollbar
        self.treeviewScrollbar = ttk.Scrollbar(self.medicationFrame, orient="vertical",
                                               command=self.medicationTreeview.yview)
        self.medicationTreeview.configure(yscrollcommand=self.treeviewScrollbar.set)
        self.treeviewScrollbar.pack(side="right", fill="y")
        self.medicationTreeview.pack(side="left", fill="both", expand=True)

        self.medicationFrame.pack(fill="both", expand=True, padx=20, pady=20)

        self.backBtn = ttk.Button(self.content, text="Back", command=self.back)
        self.backBtn.pack(pady=10)

        self.form.pack(pady=10)

    def back(self):
        self.content.pack_forget()
        viewDoctorAppointmentPage.show_page()


    def show_page(self):
        self.content.pack()

        for item in self.medicationTreeview.get_children():
            self.medicationTreeview.delete(item)

        try:
            prescription = execute_procedure(cursor, f'GetPrescriptionByAppointID {appointId}')[0]
            presId = prescription[0]
            diagnosis = prescription[1]
            medications = execute_procedure(cursor, f'GetMedicationByPrescriptionID {presId}')

            # Set diagnosis
            self.diagnosisVar.set(diagnosis)

            # Add medications to listbox
            for med in medications:
                self.medicationTreeview.insert("", "end",
                                               values=(med[1], med[2], med[4], med[3]))

        except Exception:
            messagebox.showinfo('Error', "Unexpected Error!")



# '------------------------- Doctor Services -------------------------'

#Logic Done
class DoctorPage:
    def __init__(self):
        self.content = tk.Frame(root)

    def show_page(self):
        self.content.pack(expand=True, fill='both')
        self.nameLabel = ttk.Label(self.content, text="Doctor page")
        self.nameLabel.pack()

        self.viewAppointmentsBtn = ttk.Button(self.content, text="view Appointments", command=self.viewAppointments)
        self.viewPayrollBtn = ttk.Button(self.content, text="view Payroll", command=self.viewPayroll)
        self.backBtn = ttk.Button(self.content, text="Back", command=self.back)

        self.viewAppointmentsBtn.pack(pady=10)
        self.viewPayrollBtn.pack(pady=10)
        self.backBtn.pack(pady=10)


    def viewAppointments(self):
        self.content.pack_forget()
        viewDoctorAppointmentPage.show_page()

    def viewPayroll(self):
        self.content.pack_forget()
        viewPayrollPage.show_page()

    def back(self):
        self.content.pack_forget()
        loginPage.show_page()


class DoctorViewAppointment:
    def __init__(self):

        # Page Title

        self.content = tk.Frame(root)
        ttk.Label(self.content, text="View Appointments", font="Calibre 20").pack(pady=20)

        # Appointment Tree

        self.appointmentsFrame = tk.Frame(self.content)
        columns = ('Appointment ID', 'Date', 'Doctor', 'Patient', 'Amount')
        self.appointmentsTreeView = ttk.Treeview(self.appointmentsFrame, columns=columns)
        for i, col in enumerate(columns):
            self.appointmentsTreeView.heading(col, text=col, anchor='w')
        for col in columns:
            self.appointmentsTreeView.column(col, width=100)
        self.appointmentsTreeView.pack(fill='both', expand=True ,pady=30)

        self.appointmentsTreeView.bind("<<TreeviewSelect>>", self.on_select)

        # Buttons Frame

        self.btnsFrame = tk.Frame(self.content)

        self.viewPrescriptionBtn = ttk.Button(self.btnsFrame, text="View Prescription", command=self.view_presc)
        self.editPrescriptionBtn = ttk.Button(self.btnsFrame, text="Edit Prescription", command=self.edit_presc)
        self.backBtn = ttk.Button(self.btnsFrame, text="Back", command=self.back)

        self.viewPrescriptionBtn.pack(side='left', padx=30)
        self.editPrescriptionBtn.pack(side='left', padx=30)
        self.backBtn.pack(side='left', padx=30)

        # Pack Frames
        self.appointmentsFrame.pack()
        self.btnsFrame.pack()

    def on_select(self, event):
        global appointId
        selected = self.appointmentsTreeView.selection()[0]
        appointId = self.appointmentsTreeView.item(selected)['values'][0]

    def show_page(self):
        self.content.pack()
        try:
            appointments = execute_procedure(cursor, f'Doctor_view {doctorId}')
            self.appointmentsFrame.pack(fill='both', expand=True, pady=30)

            for item in self.appointmentsTreeView.get_children():
                self.appointmentsTreeView.delete(item)

            for appointment in appointments:
                self.appointmentsTreeView.insert("", "end", values=(appointment[0], appointment[1],
                                                                    appointment[2] + ' ' + appointment[3],
                                                                    appointment[4], appointment[5]))

        except Exception:
            self.appointmentsFrame.pack_forget()
            messagebox.showinfo("Error", "Unexpected Error!")

    def back(self):
        self.content.pack_forget()
        doctorPage.show_page()

    def view_presc(self):
        self.content.pack_forget()
        viewPrescriptionPage.show_page()

    def edit_presc(self):
        self.content.pack_forget()
        editPrescriptionPage.show_page()


class EditPrescriptionPage:
    def __init__(self):
        self.content = tk.Frame(root)
        self.form = tk.Frame(self.content)
        ttk.Label(self.form, text="Edit Prescription", font=("calibre", 20)).pack(pady=20)

        # Diagnosis Entry
        self.diagnosisFrame = tk.Frame(self.form)
        ttk.Label(self.diagnosisFrame, text="Diagnosis: ", font=("calibre", 10, "bold")).pack(side="left", padx=20)
        self.diagnosisEntry = ttk.Entry(self.diagnosisFrame)
        self.diagnosisEntry.pack(side="right", padx=20)
        self.diagnosisFrame.pack(fill="x", expand=True, padx=20, pady=5)

        # Medication List
        self.medications = []

        # Medication Details
        self.medicationFrame = tk.Frame(self.form)
        ttk.Label(self.medicationFrame, text="Medication", font=("calibre", 18)).pack(pady=10)
        self.medicationEntries = {}
        fields = ["Name", "Dosage", "Frequency", "Duration"]
        for field in fields:
            frame = tk.Frame(self.medicationFrame)
            ttk.Label(frame, text=f"{field}: ", font=("calibre", 10, "bold")).pack(side="left", padx=20)
            entry = ttk.Entry(frame)
            entry.pack(side="right", padx=20)
            self.medicationEntries[field] = entry
            frame.pack(fill="x", expand=True, padx=20, pady=5)

        # Add Medication Button
        self.addMedicationBtn = ttk.Button(self.medicationFrame, text="Add Medication", command=self.add_medication)
        self.addMedicationBtn.pack(pady=10)

        self.medicationFrame.pack(pady=20)

        # Medications Listbox
        self.medicationListLabel = ttk.Label(self.form, text="Medications List", font=("calibre", 10, "bold"))
        self.medicationListLabel.pack(pady=10)
        self.medicationListBox = tk.Listbox(self.form, width=50)
        self.medicationListBox.pack(pady=10)

        # Submit Button
        self.submitBtn = ttk.Button(self.content, text="Submit Prescription", command=self.submit_prescription)
        self.submitBtn.pack(pady=10)

        self.form.pack(pady=10)

    def show_page(self):
        self.content.pack()

    def add_medication(self):
        # Retrieve the medication details from the entries
        medication = {field: self.medicationEntries[field].get() for field in self.medicationEntries}
        # Add the medication to the medications list
        self.medications.append(medication)
        # Clear the entries
        for entry in self.medicationEntries.values():
            entry.delete(0, tk.END)
        # Update the Listbox
        self.medicationListBox.insert(tk.END, medication["Name"])

    def submit_prescription(self):
        diagnosis = self.diagnosisEntry.get()
        # Here you would handle the prescription submission, for example, sending it to a database
        print(f"Diagnosis: {diagnosis}")
        for medication in self.medications:
            print(f"Medication: {medication}")

        try:
            execute_insert_procedure(cursor,conn,f'prescription_add \'{diagnosis}\',{appointId}')
            presId = execute_procedure(cursor, f'GetPrescriptionByAppointID {appointId}')[0][0]

            for i in range(len(self.medications)):
                execute_insert_procedure(cursor,conn, f'medication_add {self.medications[i]['Duration']},{self.medications[i]['Frequency']}, '
                                          f'\'{self.medications[i]['Name']}\',{self.medications[i]['Dosage']},{presId}')
        except Exception:
            messagebox.showinfo('Error', "Please enter valid data!")

        # Clear the form
        self.diagnosisEntry.delete(0, tk.END)
        self.medications.clear()
        self.medicationListBox.delete(0, tk.END)

#Logic Done
class ViewPayrollPage:
    def __init__(self):
        self.content = tk.Frame(root)
        ttk.Label(self.content, text="View Payroll", font="Calibre 40").pack()

        self.workingHrsVar = tk.StringVar()
        self.workingHrsFrame = tk.Frame(self.content)
        ttk.Label(self.workingHrsFrame, text="Working hours: ", font="Calibre 20").pack(side='left')
        self.workingHrsText = ttk.Label(self.workingHrsFrame, textvariable=self.workingHrsVar, font="Calibre 20")
        self.workingHrsText.pack(side='right')

        self.salaryVar = tk.StringVar()
        self.salaryFrame = tk.Frame(self.content)
        ttk.Label(self.salaryFrame, text="Salary: ", font="Calibre 20").pack(side='left')
        self.salaryText = ttk.Label(self.salaryFrame, textvariable=self.salaryVar, font="Calibre 20")
        self.salaryText.pack(side='right')

        self.backBtn = ttk.Button(self.content, text="Back", command=self.back)

        self.workingHrsFrame.pack(fill='both', expand=True, pady=50)
        self.salaryFrame.pack(fill='both', expand=True)
        self.backBtn.pack(pady=90)

        self.workingHrsVar.set("This is working hrs")
        self.salaryVar.set("This is Salary")

    def show_page(self):
        self.content.pack(pady=50)
        try:
            rows = execute_procedure(cursor, f'view_payroll {doctorId}')
            self.workingHrsVar.set(rows[0][1])
            self.salaryVar.set(rows[0][2])
        except Exception:
            messagebox.showinfo('Error', 'No Payroll for that doctor!')

    def back(self):
        self.content.pack_forget()
        doctorPage.show_page()


# '------------------------- Patient Services -------------------------'
class PatientViewAppointment:

    def __init__(self):

        # Page Title

        self.content = tk.Frame(root)
        ttk.Label(self.content, text="View Appointments", font="Calibre 20").pack(pady=20)

        # Appointment Tree

        self.appointmentsFrame = tk.Frame(self.content)
        columns = ('Appointment ID', 'Date', 'Doctor', 'Patient', 'Amount')
        self.appointmentsTreeView = ttk.Treeview(self.appointmentsFrame, columns=columns)
        for i, col in enumerate(columns):
            self.appointmentsTreeView.heading(col, text=col, anchor='w')
        for col in columns:
            self.appointmentsTreeView.column(col, width=100)
        self.appointmentsTreeView.pack(fill='both', expand=True ,pady=30)

        # Buttons Frame

        self.btnsFrame = tk.Frame(self.content)

        self.viewPrescriptionBtn = ttk.Button(self.btnsFrame, text="View Prescription", command=self.view_presc)
        self.backBtn = ttk.Button(self.btnsFrame, text="Back", command=self.back)

        self.viewPrescriptionBtn.pack(side='left', padx=30)
        self.backBtn.pack(side='left', padx=30)




        # Pack Frames
        self.appointmentsFrame.pack()
        self.btnsFrame.pack()

    def show_page(self):
        self.content.pack()
        try:
            appointments = execute_procedure(cursor, f'Patient_view {patientId}')

            for item in self.appointmentsTreeView.get_children():
                self.appointmentsTreeView.delete(item)

            for appointment in appointments:
                self.appointmentsTreeView.insert("", "end", values=(appointment[0], appointment[1],
                                                                    appointment[2] + ' ' + appointment[3],
                                                                    appointment[4], appointment[5]))
        except Exception:
            self.appointmentsFrame.pack_forget()
            self.viewPrescriptionBtn.pack_forget()
            messagebox.showinfo("Error", "Please Enter a Valid ID!")

    def back(self):
        self.content.pack_forget()
        loginPage.show_page()

    def view_presc(self):
        # Open a window of prescription
        pass


# '------------------------- GUI Window-------------------------'

root = ttk.Window(themename='darkly')
root.title("Clinical Management System")
root.geometry(DIMENSIONS)

# '------------------------- Page Instances -------------------------'
loginPage = LoginPage()

# Receptionist Landing Page
receptionistPage = ReceptionistPage()
reserveAppointmentPage = ReserveAppointmentPage()
addDoctorPage = AddDoctorPage()
addPatientPage = AddPatientPage()
updatePayrollPage = UpdatePayrollPage()
viewPatientPage = ViewPatientPage()
viewDoctorPage = ViewDoctorPage()

# Doctor Landing Page
doctorPage = DoctorPage()
viewPayrollPage = ViewPayrollPage()
viewDoctorAppointmentPage = DoctorViewAppointment()
editPrescriptionPage = EditPrescriptionPage()
viewPrescriptionPage = ViewPrescriptionPage()

# Patient Landing Page
viewPatientAppointmentPage = PatientViewAppointment()

# Essential Variables
doctorId = -1
patientId = -1
receptionistId = -1
appointId = -1
