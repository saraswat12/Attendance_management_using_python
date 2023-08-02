from datetime import date, datetime, timedelta


user_database = []
student_database = {}

def register_user(username, password):
    if not any(user['username'] == username for user in user_database):
        user_database.append({'username': username, 'password': password})
        print("Registration successful. You can now log in.")
    else:
        print("Username already exists. Please choose a different username.")

def login_user(username, password):
    if any(user['username'] == username and user['password'] == password for user in user_database):
        print(f"Welcome, {username}!")
        return True
    else:
        print("Invalid username or password. Please try again.")
        return False


def add_student_info(name, roll_number, email, address):
    if roll_number not in student_database:
        student_database[roll_number] = {
            'Name': name,
            'Email': email,
            'Address': address
        }
        print(f"Student '{name}' information added successfully.")
    else:
        print(f"Student with Roll Number '{roll_number}'")
        
def view_student_info(roll_number):
    if roll_number in student_database:
        student_info = student_database[roll_number]
        print(f"Student Information for Roll Number '{roll_number}':")
        for key, value in student_info.items():
            print(f"{key}: {value}")
    else:
        print(f"Student with Roll Number '{roll_number}' not found in the database. Cannot view information.")



def update_student_info(roll_number, key, value):
    if roll_number in student_database:
        student_info = student_database[roll_number]
        if key in student_info:
            student_info[key] = value
            print(f"Student with Roll Number '{roll_number}' information updated successfully.")
        else:
            print(f"Invalid key '{key}'. Cannot update.")
    else:
        print(f"Student with Roll Number '{roll_number}' not found in the database.")

def delete_student_info(roll_number):
    if roll_number in student_database:
        del student_database[roll_number]
        print(f"Student with Roll Number '{roll_number}' information deleted successfully.")
    else:
        print(f"Student with Roll Number '{roll_number}' not found in the database. Cannot delete information.")


def validate_roll_number(roll_number):
    if not roll_number.isdigit():
        print("Invalid roll number. Roll number should contain digits only.")
        return False
    return True


def validate_email(email):
    # Simple email validation using a regular expression
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        print("Invalid email address.")
        return False
    return True


def mark_attendance(roll_number, date_str=None):
    today = date.today().strftime("%Y-%m-%d") if date_str is None else date_str
    if roll_number in student_database:
        if 'Attendance' not in student_database[roll_number]:
            student_database[roll_number]['Attendance'] = {}
        attendance_data = student_database[roll_number]['Attendance']

        if today in attendance_data:
            print(f"Attendance for Roll Number '{roll_number}' on {today} has already been marked as '{attendance_data[today]}'.")
        else:
            while True:
                attendance = input(f"Mark attendance for Roll Number '{roll_number}' on {today} (P for Present, A for Absent): ").upper()
                if attendance in ['P', 'A']:
                    attendance_data[today] = attendance
                    print(f"Attendance marked for Roll Number '{roll_number}' on {today} as '{attendance}'.")
                    break
                else:
                    print("Invalid input. Please enter 'P' for Present or 'A' for Absent.")
    else:
        print(f"Student with Roll Number '{roll_number}' not found in the database. Cannot mark attendance.")
                
def view_attendance_records(rollno):
    if rollno in student_database:
        student_data = student_database[rollno]
        if 'Attendance' in student_data:
            attendance_dates = student_data['Attendance']
            print(f"Attendance records for '{rollno}':")
            for date_str, attendance_status in attendance_dates.items():
                print(f"{date_str}: {attendance_status}")
        else:
            print(f"No attendance records found for '{rollno}'.")
    else:
        print(f"Student '{rollno}' not found in the database. Cannot view attendance records.")

def view_attendance_by_date(date_str):
    try:
        specific_date = datetime.strptime(date_str, "%Y-%m-%d")
        present_students = []

        for roll_number, student_data in student_database.items():
            if 'Attendance' in student_data:
                attendance_dates = student_data['Attendance']
                if date_str in attendance_dates and attendance_dates[date_str] == 'P':
                    present_students.append(roll_number)

        if present_students:
            print(f"Students present on {date_str}:")
            for value in present_students:
                print(f"Roll Number: {value}")
        else:
            print(f"No students were present on {date_str}.")
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD' format.")


# Step 1: Implement Function to Generate Reports

from datetime import datetime, timedelta

def generate_attendance_report(roll_number, time_period):
    if roll_number in student_database:
        student_data = student_database[roll_number]
        if 'Attendance' in student_data:
            attendance_dates = student_data['Attendance']
            if time_period == "monthly":
                today = datetime.today()
                first_day_of_month = today.replace(day=1)
                report_start_date = first_day_of_month - timedelta(days=30)

            elif time_period == "weekly":
                today = datetime.today()
                report_start_date = today - timedelta(days=today.weekday())
            
            elif time_period == "daily":
                report_start_date = datetime.today()
            else:
                print("Invalid time period. Please choose 'monthly', 'weekly', or 'daily'.")
                return

            report = {}
            for date_str in attendance_dates:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj >= report_start_date:
                    date_formatted = date_obj.strftime("%Y-%m-%d")
                    report[date_formatted] = "Present"

            print(f"Attendance report for roll number '{roll_number}' for the last {time_period}:")

            if report:
                for date_str, status in report.items():
                    print(f"{date_str}: {status}")
                print(f"Total days attended in the last {time_period}: {len(report)}")
                total_days = len(report)
                total_days_in_period = (datetime.today() - report_start_date).days + 1
                percentage_attendance = (total_days / total_days_in_period) * 100
                print(f"Percentage attendance in the last {time_period}: {percentage_attendance:.2f}%")
            else:
                print(f"No attendance records found for roll number '{roll_number}' in the last {time_period}.")

        else:
            print(f"No attendance records found for roll number '{roll_number}'.")
    else:
        print(f"Student roll number '{roll_number}' not found in the database. Cannot generate attendance report.")


def main():

    logged_in = False
    should_continue = True

    while should_continue:
        print("\nAttendance Management System")
        if not logged_in:
            print("1. Register")
            print("2. Login")
            print("3. Exit")
        else:
            print("1. Add Student")
            print("2. Remove Student")
            print("3. Mark Attendance")
            print("4. View Attendance")
            print("5. Manage Student Information")
            print("6. View Attendance Records Filter by Date")
            print("7. Generate Attendance Report")
            print("8. Logout")
            print("9. Exit")


        choice = int(input("Enter your choice: "))

        if not logged_in:
            if choice == 1:
                username = input("Enter username: ")
                password = input("Enter password: ")
                register_user(username, password)

            elif choice == 2:
                username = input("Enter username: ")
                password = input("Enter password: ")
                logged_in = login_user(username, password)

            elif choice == 3:
                print("\nYOU EXIT FROM THE SYSTEM")
                should_continue = False

            else:
                print("Invalid choice. Please try again.")

        else:
            if choice == 1:
                 name = input("Enter student name: ")
                 while True:
                     roll_number = input("Enter student roll number: ")
                     if validate_roll_number(roll_number):
                         break;

                 while True:
                     email = input("Enter student email: ")
                     if validate_email(email):
                         break;
                 
                 
                 address = input("Enter address: ")
                 add_student_info(name, roll_number, email, address)
                    

            elif choice == 2:
                roll_number = input("Enter student roll number: ")
                delete_student_info(roll_number)

            elif choice == 3:
                roll_number = input("Enter student roll number: ")
                date_str = input("Enter date (YYYY-MM-DD) to mark attendance (press Enter for today's date): ")
                if not date_str:
                    mark_attendance(roll_number)
                else:
                    mark_attendance(roll_number, date_str)
            

            elif choice == 4:
                roll_number = input("Enter student roll number: ")
                view_attendance_records(roll_number)                

            elif choice == 5:
                print("\nManage student Information")
                roll_number = input("Enter student roll number: ")
                       
                print("1. View Student Information")
                print("2. Update Student Information")
                print("3. Delete Student Information")

                info_choice = int(input("Enter your choice: "))

                if info_choice == 1:
                    view_student_info(roll_number)

                elif info_choice == 2:
                    key = input("Enter key (e.g., 'Address', 'Email'): ")
                    value = input("Enter new value: ")
                    #if key == 'Address' and not validate_roll_number(value):
                        #continue
                    if key == 'Email' and not validate_email(value):
                        continue
                    update_student_info(roll_number, key, value)
                    
                elif info_choice == 3:
                    delete_student_info(roll_number)

                else:
                    print("Invalid choice. Please try again.")

            elif choice == 6:               
                date_str = input("Enter date (YYYY-MM-DD) to filter records: ")
                view_attendance_by_date(date_str)

            elif choice == 7:
                roll_number = input("Enter student roll number: ")
                time_period = input("Enter time period ('monthly', 'weekly', or 'daily'): ")
                generate_attendance_report(roll_number, time_period)
                 
        
            elif choice == 8:
                logged_in = False
                print("\nLOGGED OUT")
                
            elif choice == 9:
                print("\nYOU EXIT FROM THE SYSTEM")
                should_continue = False

            else:
                print("Invalid choice. Please try again.")
                                
                   
                
if __name__ == "__main__":
    main()           
                
                

        

         
        















































        

        
   
