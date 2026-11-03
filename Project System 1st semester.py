import re
from datetime import datetime, date, time

# ============================================================
# COC STUDENTS UNIFORM APPOINTMENT SCHEDULER
# ============================================================

STAFF_PASSWORD = "STAFF1948"
MIN_APPOINTMENT_DATE = date(2026, 10, 1)
MAX_APPOINTMENT_DATE = date(2027, 4, 30)
MAX_APPOINTMENTS_PER_DATE = 100
ALLOWED_CAMPUS = "PUERTO CAMPUS"

appointments = []
total_added = 0
total_cancelled = 0
total_completed = 0
next_code_number = 1


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def choose_option(title, options):
    while True:
        print("\n" + "-" * 55)
        print(title)
        print("-" * 55)

        for number, option in enumerate(options, 1):
            print(f"{number}. {option}")

        choice = input("Enter your choice: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(options):
                return options[choice - 1]

        print("\nInvalid choice. Please select from the available options.")


def get_student_name():
    while True:
        print("\nEnter Student Name")
        print("Format: LAST NAME, FIRST NAME, MI.")
        print("Example: DELA CRUZ, JUAN, D.")

        name = input("Student Name: ").strip()

        pattern = (
            r"^[A-Za-zÑñ]+(?:[ '-][A-Za-zÑñ]+)*, "
            r"[A-Za-zÑñ]+(?:[ '-][A-Za-zÑñ]+)*, [A-Za-zÑñ]\.$"
        )

        if re.fullmatch(pattern, name):
            return name.upper()

        print("\nInvalid name format.")
        print("Please follow this format: LAST NAME, FIRST NAME, MI.")


def get_student_id():
    while True:
        print("\nEnter Student ID")
        print("Format: XX-XXXX-XXXXXX")
        print("Example: 02-2627-009656")

        student_id = input("Student ID: ").strip()

        if re.fullmatch(r"\d{2}-\d{4}-\d{6}", student_id):
            return student_id

        print("\nInvalid Student ID.")
        print("Your ID must have 2 digits - 4 digits - 6 digits.")


def get_phone_number():
    while True:
        print("\nEnter Phone Number")
        print("Example: 09678855865")

        phone = input("Phone Number: ").strip()

        if re.fullmatch(r"09\d{9}", phone):
            return phone

        print("\nInvalid phone number.")
        print("Phone number must contain exactly 11 digits and start with 09.")


def count_active_appointments_on_date(date_string, exclude_code=None):
    count = 0

    for appointment in appointments:
        if (
            appointment["status"] == "ACTIVE"
            and appointment["date"] == date_string
        ):
            if (
                exclude_code is not None
                and appointment["code"] == exclude_code
            ):
                continue

            count += 1

    return count


def get_appointment_date(exclude_code=None):
    while True:
        print("\nEnter Appointment Date")
        print("Format: MM/DD/YYYY")

        date_input = input("Appointment Date: ").strip()

        try:
            appointment_date = datetime.strptime(
                date_input,
                "%m/%d/%Y"
            ).date()

        except ValueError:
            print("\nInvalid date format.")
            print("Please use MM/DD/YYYY.")
            continue

        if (
            appointment_date < MIN_APPOINTMENT_DATE
            or appointment_date > MAX_APPOINTMENT_DATE
        ):
            print("\nInvalid appointment date.")
            print(
                "Appointment dates are only available "
                "from 10/01/2026 to 04/30/2027."
            )
            continue

        formatted_date = appointment_date.strftime("%m/%d/%Y")

        current_count = count_active_appointments_on_date(
            formatted_date,
            exclude_code
        )

        if current_count >= MAX_APPOINTMENTS_PER_DATE:
            print("\nThis date has already reached 100 active students.")
            print(
                "Please set another date to avoid over users interaction."
            )
            continue

        return formatted_date


def get_appointment_time():
    while True:
        print("\nEnter Appointment Time")
        print("Morning: 7:00 AM - 11:30 AM")
        print("Afternoon: 1:30 PM - 5:00 PM")

        time_input = input("Appointment Time: ").strip().upper()

        try:
            appointment_time = datetime.strptime(
                time_input,
                "%I:%M %p"
            ).time()

        except ValueError:
            print("\nInvalid time format.")
            print("Please use HH:MM AM/PM.")
            continue

        morning_start = time(7, 0)
        morning_end = time(11, 30)

        afternoon_start = time(13, 30)
        afternoon_end = time(17, 0)

        valid_time = (
            morning_start <= appointment_time <= morning_end
            or
            afternoon_start <= appointment_time <= afternoon_end
        )

        if valid_time:
            return appointment_time.strftime("%I:%M %p")

        print("\nInvalid appointment time.")
        print("Available time is:")
        print("7:00 AM - 11:30 AM")
        print("1:30 PM - 5:00 PM")


def generate_code():
    global next_code_number

    code = f"AP-{next_code_number:04d}"
    next_code_number += 1

    return code


def find_appointment(code):
    for appointment in appointments:
        if appointment["code"].upper() == code.upper():
            return appointment

    return None


def has_active_appointment(student_id):
    for appointment in appointments:
        if (
            appointment["student_id"] == student_id
            and appointment["status"] == "ACTIVE"
        ):
            return True

    return False


def appointment_datetime(appointment):
    appointment_date = datetime.strptime(
        appointment["date"],
        "%m/%d/%Y"
    ).date()

    appointment_time = datetime.strptime(
        appointment["time"],
        "%I:%M %p"
    ).time()

    return datetime.combine(
        appointment_date,
        appointment_time
    )


def sort_appointments():
    active_appointments = [
        appointment
        for appointment in appointments
        if appointment["status"] == "ACTIVE"
    ]

    active_appointments.sort(
        key=appointment_datetime
    )

    return active_appointments


def get_queue_number(appointment):
    active_appointments = sort_appointments()

    for index, item in enumerate(active_appointments, 1):
        if item["code"] == appointment["code"]:
            return index

    return None


# ============================================================
# CREATE APPOINTMENT
# ============================================================

def create_appointment():
    global total_added

    print("\n" + "=" * 60)
    print("CREATE NEW APPOINTMENT")
    print("=" * 60)

    campus = choose_option(
        "Select Campus",
        [
            "PUERTO CAMPUS",
            "NOT PUERTO CAMPUS"
        ]
    )

    if campus != ALLOWED_CAMPUS:
        print(
            "\nOnly Puerto Campus students are allowed "
            "to use this system."
        )
        print("Appointment creation has been stopped.")
        return

    student_id = get_student_id()

    if has_active_appointment(student_id):
        print("\nYou already have an active appointment.")
        print(
            "Please finish or cancel your current "
            "appointment first."
        )
        return

    name = get_student_name()

    gender = choose_option(
        "Select Gender",
        [
            "M",
            "F"
        ]
    )

    phone = get_phone_number()

    course = choose_option(
        "Select Course",
        [
            "BSBA",
            "BSIT",
            "BSED",
            "BEED",
            "BSHM",
            "Other"
        ]
    )

    year_level = choose_option(
        "Select Year Level",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )

    uniform_type = choose_option(
        "Select Uniform Type",
        [
            "A",
            "B",
            "PE",
            "A & B",
            "A & PE",
            "B & PE",
            "A, B & PE"
        ]
    )

    uniform_size = choose_option(
        "Select Uniform Size",
        [
            "XS",
            "S",
            "M",
            "L",
            "XL",
            "XXL"
        ]
    )

    service = choose_option(
        "Select Service",
        [
            "Uniform Fitting",
            "Uniform Claiming",
            "Uniform Concern"
        ]
    )

    appointment_date = get_appointment_date()
    appointment_time = get_appointment_time()

    # Final capacity check before saving the appointment
    if (
        count_active_appointments_on_date(appointment_date)
        >= MAX_APPOINTMENTS_PER_DATE
    ):
        print("\nThis date has already reached 100 active students.")
        print(
            "Please set another date to avoid over users interaction."
        )
        return

    code = generate_code()

    appointment = {
        "code": code,
        "campus": campus,
        "name": name,
        "student_id": student_id,
        "gender": gender,
        "phone": phone,
        "course": course,
        "year_level": year_level,
        "uniform_type": uniform_type,
        "uniform_size": uniform_size,
        "service": service,
        "date": appointment_date,
        "time": appointment_time,
        "status": "ACTIVE"
    }

    appointments.append(appointment)
    total_added += 1

    queue_number = get_queue_number(appointment)

    date_count = count_active_appointments_on_date(
        appointment_date
    )

    print("\n" + "=" * 60)
    print("APPOINTMENT SUCCESSFULLY CREATED")
    print("=" * 60)

    print(f"Appointment Code : {code}")
    print(f"Campus           : {campus}")
    print(f"Queue Number     : {queue_number}")
    print(f"Service          : {service}")
    print(f"Date             : {appointment_date}")
    print(f"Time             : {appointment_time}")
    print(f"Students on Date : {date_count}/100")

    print("\nIMPORTANT REMINDER:")
    print("Please bring your OFFICIAL REGISTRATION FORM.")
    print(
        "It will be used to identify and verify "
        "that you are a Puerto Campus student."
    )
    print(
        "Keep your Appointment Code and show it "
        "to the staff when you arrive."
    )


# ============================================================
# STUDENT PUBLIC QUEUE
# ============================================================

def view_student_queue():
    print("\n" + "=" * 70)
    print("STUDENT PUBLIC QUEUE")
    print("=" * 70)

    active_appointments = sort_appointments()

    if not active_appointments:
        print("\nThere are currently no active appointments.")
        return

    print(
        f"{'QUEUE':<8}"
        f"{'CODE':<12}"
        f"{'SERVICE':<22}"
        f"{'DATE':<15}"
        f"{'TIME':<12}"
    )

    print("-" * 69)

    for index, appointment in enumerate(
        active_appointments,
        1
    ):
        print(
            f"{index:<8}"
            f"{appointment['code']:<12}"
            f"{appointment['service']:<22}"
            f"{appointment['date']:<15}"
            f"{appointment['time']:<12}"
        )

    print("\nPrivacy Notice:")
    print(
        "Student names and personal information "
        "are hidden from the public queue."
    )


# ============================================================
# CHECK APPOINTMENT
# ============================================================

def check_appointment():
    print("\n" + "=" * 60)
    print("CHECK MY APPOINTMENT")
    print("=" * 60)

    code = input(
        "\nEnter your Appointment Code: "
    ).strip().upper()

    appointment = find_appointment(code)

    if appointment is None:
        print("\nAppointment not found.")
        return

    print("\n" + "-" * 60)

    print(
        f"Appointment Code : {appointment['code']}"
    )
    print(
        f"Campus           : {appointment['campus']}"
    )
    print(
        f"Status           : {appointment['status']}"
    )
    print(
        f"Service          : {appointment['service']}"
    )
    print(
        f"Date             : {appointment['date']}"
    )
    print(
        f"Time             : {appointment['time']}"
    )

    if appointment["status"] == "ACTIVE":
        queue_number = get_queue_number(appointment)

        if queue_number is not None:
            print(
                f"Current Queue    : {queue_number}"
            )

    elif appointment["status"] == "DONE":
        print(
            "\nThis appointment has already been completed."
        )

    elif appointment["status"] == "CANCELLED":
        print(
            "\nThis appointment was cancelled."
        )

    print("-" * 60)


# ============================================================
# UPDATE APPOINTMENT
# ============================================================

def update_appointment():
    print("\n" + "=" * 60)
    print("UPDATE APPOINTMENT")
    print("=" * 60)

    code = input(
        "\nEnter Appointment Code: "
    ).strip().upper()

    appointment = find_appointment(code)

    if appointment is None:
        print("\nAppointment not found.")
        return

    if appointment["status"] != "ACTIVE":
        print("\nThis appointment cannot be updated.")
        print(
            f"Current status: {appointment['status']}"
        )
        return

    print("\nUpdate Appointment Date and Time")

    old_date = appointment["date"]

    new_date = get_appointment_date(
        exclude_code=appointment["code"]
    )

    new_time = get_appointment_time()

    appointment["date"] = new_date
    appointment["time"] = new_time

    print("\nAppointment successfully updated.")
    print(f"Previous Date : {old_date}")
    print(f"New Date      : {new_date}")
    print(f"New Time      : {new_time}")


# ============================================================
# CANCEL APPOINTMENT
# ============================================================

def cancel_appointment():
    global total_cancelled

    print("\n" + "=" * 60)
    print("CANCEL APPOINTMENT")
    print("=" * 60)

    code = input(
        "\nEnter Appointment Code: "
    ).strip().upper()

    appointment = find_appointment(code)

    if appointment is None:
        print("\nAppointment not found.")
        return

    if appointment["status"] != "ACTIVE":
        print("\nThis appointment cannot be cancelled.")
        print(
            f"Current status: {appointment['status']}"
        )
        return

    confirmation = input(
        "\nAre you sure you want to cancel "
        "this appointment? (Y/N): "
    ).strip().upper()

    if confirmation == "Y":
        appointment["status"] = "CANCELLED"
        total_cancelled += 1

        print("\nAppointment successfully cancelled.")
        print(
            "You may create a new appointment if needed."
        )

    else:
        print("\nCancellation cancelled.")


# ============================================================
# STAFF LOGIN
# ============================================================

def staff_login():
    print("\n" + "=" * 60)
    print("STAFF LOGIN")
    print("=" * 60)

    password = input(
        "Enter Staff Password: "
    ).strip()

    if password == STAFF_PASSWORD:
        print("\nWelcome, Staff!")
        print(
            "You may now manage and verify "
            "student appointments."
        )
        return True

    print("\nIncorrect password.")
    return False


# ============================================================
# STAFF ACTIVE QUEUE
# ============================================================

def view_staff_queue():
    print("\n" + "=" * 75)
    print("STAFF ACTIVE QUEUE")
    print("=" * 75)

    active_appointments = sort_appointments()

    if not active_appointments:
        print("\nThere are no active appointments.")
        return

    print(
        f"{'QUEUE':<8}"
        f"{'CODE':<12}"
        f"{'SERVICE':<22}"
        f"{'DATE':<15}"
        f"{'TIME':<12}"
    )

    print("-" * 70)

    for index, appointment in enumerate(
        active_appointments,
        1
    ):
        print(
            f"{index:<8}"
            f"{appointment['code']:<12}"
            f"{appointment['service']:<22}"
            f"{appointment['date']:<15}"
            f"{appointment['time']:<12}"
        )

    print(
        "\nStaff can verify an appointment "
        "using its Appointment Code."
    )


# ============================================================
# VERIFY APPOINTMENT
# ============================================================

def verify_appointment():
    print("\n" + "=" * 70)
    print("VERIFY APPOINTMENT")
    print("=" * 70)

    code = input(
        "\nEnter Appointment Code: "
    ).strip().upper()

    appointment = find_appointment(code)

    if appointment is None:
        print("\nAppointment not found.")
        return

    print("\n" + "=" * 70)
    print("APPOINTMENT DETAILS")
    print("=" * 70)

    print(
        f"Appointment Code : {appointment['code']}"
    )
    print(
        f"Status           : {appointment['status']}"
    )
    print(
        f"Campus           : {appointment['campus']}"
    )
    print(
        f"Student Name     : {appointment['name']}"
    )
    print(
        f"Student ID       : {appointment['student_id']}"
    )
    print(
        f"Phone Number     : {appointment['phone']}"
    )
    print(
        f"Gender           : {appointment['gender']}"
    )
    print(
        f"Course           : {appointment['course']}"
    )
    print(
        f"Year Level       : {appointment['year_level']}"
    )
    print(
        f"Uniform Type     : {appointment['uniform_type']}"
    )
    print(
        f"Uniform Size     : {appointment['uniform_size']}"
    )
    print(
        f"Service          : {appointment['service']}"
    )
    print(
        f"Date             : {appointment['date']}"
    )
    print(
        f"Time             : {appointment['time']}"
    )

    if appointment["status"] == "ACTIVE":
        queue_number = get_queue_number(
            appointment
        )

        if queue_number is not None:
            print(
                f"Queue Number     : {queue_number}"
            )

    print("=" * 70)

    print(
        "Reminder: Ask the student to present "
        "the OFFICIAL REGISTRATION FORM."
    )


# ============================================================
# MARK APPOINTMENT AS DONE
# ============================================================

def mark_as_done():
    global total_completed

    print("\n" + "=" * 70)
    print("MARK APPOINTMENT AS DONE")
    print("=" * 70)

    code = input(
        "\nEnter Appointment Code: "
    ).strip().upper()

    appointment = find_appointment(code)

    if appointment is None:
        print("\nAppointment not found.")
        return

    if appointment["status"] == "DONE":
        print(
            "\nThis appointment is already marked as DONE."
        )
        return

    if appointment["status"] == "CANCELLED":
        print("\nThis appointment was cancelled.")
        print(
            "A cancelled appointment cannot be marked as DONE."
        )
        return

    print("\nAppointment found.")

    print(
        f"Student Name : {appointment['name']}"
    )
    print(
        f"Student ID   : {appointment['student_id']}"
    )
    print(
        f"Campus       : {appointment['campus']}"
    )
    print(
        f"Service      : {appointment['service']}"
    )
    print(
        f"Date         : {appointment['date']}"
    )
    print(
        f"Time         : {appointment['time']}"
    )

    confirmation = input(
        "\nHas the student finished the transaction? (Y/N): "
    ).strip().upper()

    if confirmation == "Y":
        appointment["status"] = "DONE"
        total_completed += 1

        print("\n" + "=" * 70)
        print("APPOINTMENT MARKED AS DONE")
        print("=" * 70)

        print(
            f"Appointment Code : {appointment['code']}"
        )
        print("Status           : DONE")

        print(
            "\nThe appointment has been removed "
            "from the active queue."
        )

        print(
            "The next student can now be served."
        )

    else:
        print("\nAppointment remains ACTIVE.")


# ============================================================
# VIEW STATISTICS
# ============================================================

def view_statistics():
    active_count = len([
        appointment
        for appointment in appointments
        if appointment["status"] == "ACTIVE"
    ])

    cancelled_count = len([
        appointment
        for appointment in appointments
        if appointment["status"] == "CANCELLED"
    ])

    completed_count = len([
        appointment
        for appointment in appointments
        if appointment["status"] == "DONE"
    ])

    print("\n" + "=" * 65)
    print("APPOINTMENT STATISTICS")
    print("=" * 65)

    print(
        f"Total Appointments Added : {total_added}"
    )
    print(
        f"Active Appointments      : {active_count}"
    )
    print(
        f"Completed Appointments   : {completed_count}"
    )
    print(
        f"Cancelled Appointments   : {cancelled_count}"
    )

    print("=" * 65)


# ============================================================
# STUDENT MENU
# ============================================================

def student_menu():
    print("\n" + "=" * 65)
    print("WELCOME COCIANS STUDENT!")
    print(
        "This is the COC Students Uniform "
        "Appointment Scheduler."
    )
    print(
        "Please let us know a little about you "
        "by completing the student information "
        "needed for your appointment."
    )
    print("=" * 65)

    while True:
        print("\n" + "=" * 60)
        print("STUDENT MENU")
        print("=" * 60)

        print("1. Create Appointment")
        print("2. View Public Queue")
        print("3. Check My Appointment")
        print("4. Update Appointment")
        print("5. Cancel Appointment")
        print("6. Back to Main Menu")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            create_appointment()

        elif choice == "2":
            view_student_queue()

        elif choice == "3":
            check_appointment()

        elif choice == "4":
            update_appointment()

        elif choice == "5":
            cancel_appointment()

        elif choice == "6":
            break

        else:
            print(
                "\nInvalid choice. Please try again."
            )


# ============================================================
# STAFF MENU
# ============================================================

def staff_menu():
    if not staff_login():
        return

    while True:
        print("\n" + "=" * 65)
        print("STAFF PANEL")
        print("=" * 65)

        print("1. View Active Queue")
        print("2. Verify Appointment")
        print("3. Mark Appointment as DONE")
        print("4. View Statistics")
        print("5. Logout")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            view_staff_queue()

        elif choice == "2":
            verify_appointment()

        elif choice == "3":
            mark_as_done()

        elif choice == "4":
            view_statistics()

        elif choice == "5":
            print("\nStaff logged out.")
            break

        else:
            print(
                "\nInvalid choice. Please try again."
            )


# ============================================================
# MAIN MENU
# ============================================================

def main():
    while True:
        print("\n" + "=" * 70)
        print(
            "COC STUDENTS UNIFORM APPOINTMENT SCHEDULER"
        )
        print("=" * 70)

        print("1. Student")
        print("2. Staff")
        print("3. Exit")

        print(
            "\nNOTE: ONLY PUERTO CAMPUS STUDENTS "
            "ARE ALLOWED TO USE THIS SYSTEM."
        )

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            student_menu()

        elif choice == "2":
            staff_menu()

        elif choice == "3":
            print(
                "\nThank you for using the "
                "COC Students Uniform Appointment Scheduler."
            )
            print("Program ended.")
            break

        else:
            print(
                "\nInvalid choice. Please try again."
            )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()