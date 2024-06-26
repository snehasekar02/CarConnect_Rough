from dao.AuthenticationService import AuthenticationService
from dao.AdminService import AdminService
from dao.CustomerService import CustomerService
from dao.ReservationService import ReservationService
from dao.VehicleService import VehicleService
from dao.reportGenerator import ReportGenerator
from entity.Admin import Admin
from entity.Customer import Customer
from entity.Reservation import Reservation
from entity.Vehicle import Vehicle
from datetime import date

authentication_service = AuthenticationService()
reservationService = ReservationService()
customerService = CustomerService()
vehicleService = VehicleService()
adminService = AdminService()
reportGenerator = ReportGenerator()


def handle_customer_actions():
    while True:
        print("Customer Actions Menu:")
        print("1. Create Reservation")
        print("2. Update Reservation")
        print("3. Cancel Reservation")
        print("4. Update Customer Information")
        print("5. Get Available Vehicles")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("These are all the available vehicles..")
            v = vehicleService.get_available_vehicles()
            if v is not None:
                print(v)
                last_reservation_id = 10000
                reservationID = last_reservation_id + 1
                customerID = input("Enter customer ID: ")
                vehicleID = input("Enter vehicle ID: ")
                startDate = input("Enter start date (YYYY-MM-DD): ")
                endDate = input("Enter end date (YYYY-MM-DD): ")
                status = 'Booked'
                reservation = Reservation(reservationID, customerID, vehicleID, startDate, endDate, 0, status)
                rate = vehicleService.get_vehicle_by_id(vehicleID).get_dailyRate()
                reservation.calculateTotalCost(rate)
                reservationService.create_reservation(reservation)
                print("Reservation created successfully!!")


        elif choice == '2':
            username = input("Enter Customer Username: ")
            cust = customerService.get_customer_by_username(username)
            customerID = cust.get_customer_id()
            vehicleID = input("Enter vehicle ID: ")
            startDate = input("Enter start date (YYYY-MM-DD): ")
            endDate = input("Enter end date (YYYY-MM-DD): ")
            status = 'Booked'
            res = reservationService.get_reservations_by_customer_id(customerID)
            if res is not None:
                r = Reservation(res.get_reservationID(), customerID, vehicleID, startDate, endDate, 0, status)
                rate = vehicleService.get_vehicle_by_id(vehicleID).get_dailyRate()
                r.calculateTotalCost(rate)
                print("Updated Reservation Details:")
                r.print_info()
                reservationService.update_reservation(r)
                print("Reservation updated successfully!!")
            else:
                print("No reservations found for the customer.")

        elif choice == '3':
            Rid = int(input("Enter ReservationID to be cancelled: "))
            reservationService.cancel_reservation(Rid)
            print("Reservation cancelled successfully!!")

        elif choice == '4':
            print("Updating customer information")
            customer_id = int(input("Enter your customer id : "))
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            email = input("Enter your email: ")
            phone_number = input("Enter your phone number: ")
            address = input("Enter your address: ")
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            registration_date = date.today()
            updated_customer = Customer(customer_id, first_name, last_name, email, phone_number, address,
                                        username, password, registration_date)
            customerService.update_customer(updated_customer)
            print("Customer Details updated successfully!!")

        elif choice == '5':
            print("Available Vehicles: ")
            print(vehicleService.get_available_vehicles())
        elif choice == '6':
            print("Exiting Customer Actions...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def customer_workflow():
    customer_service = CustomerService()
    while True:
        print("Are you a new customer or an existing customer?")
        print("1. New Customer")
        print("2. Existing Customer")
        print("3. Logout")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            last_cust_id = 100
            print("Customer Registration:")
            customer_id = last_cust_id + 1
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            email = input("Enter your email: ")
            phone_number = input("Enter your phone number: ")
            address = input("Enter your address: ")
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            registration_date = date.today()
            new_customer = Customer(customer_id, first_name, last_name, email, phone_number, address,
                                    username, password, registration_date)
            if customer_service.register_customer(new_customer):
                print("Registration successful! ")
            else:
                print("Registration failed. Please try again.")
        elif choice == 2:
            print("Customer Login:")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authentication_service.authenticate_customer(username, password):
                print("Login successful!")
                print(f"Hello {username}!!")
                handle_customer_actions()
            else:
                print("Login failed. Incorrect username or password.")
        elif choice == 3:
            print("Logged out!!")
            break
        else:
            print("Invalid choice")


def handle_admin_actions():
    while True:
        print("Admin Actions Menu:")
        print("1. Get Admin by ID")
        print("2. Update Admin")
        print("3. Remove Admin")
        print("4. Add Vehicle")
        print("5. Update Vehicle")
        print("6. Remove Vehicle")
        print("7. Generate Report")
        print("8. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            admin_id = input("Enter admin ID: ")
            print(adminService.get_admin_by_id(admin_id))
        elif choice == '2':
            adminID = input("Enter Admin ID: ")
            firstName = input("Enter new First Name: ")
            lastName = input("Enter new Last Name: ")
            email = input("Enter new Email: ")
            phoneNumber = input("Enter new Phone Number: ")
            username = input("Enter new Username: ")
            password = input("Enter new Password: ")
            role = input("Enter new Role: ")
            joinDate = input("Enter new Join Date: ")

            admin = Admin(adminID, firstName, lastName, email, phoneNumber, username, password, role, joinDate)
            adminService.update_admin(admin)
            print("Admin updated successfully!!")
        elif choice == '3':
            admin_id = input("Enter admin ID: ")
            adminService.delete_admin(admin_id)
            print("Admin deleted successfully!!")
        elif choice == '4':
            last_vehicle_id = 1000
            vehicleID = last_vehicle_id + 1
            model = input("Enter Model: ")
            make = input("Enter Make: ")
            year = input("Enter Year: ")
            color = input("Enter Color: ")
            registrationNumber = input("Enter Registration Number: ")
            availability = int(input("Enter Availability (True=1/False=0): "))
            dailyRate = float(input("Enter Daily Rate: "))
            vehicle = Vehicle(vehicleID, model, make, year, color, registrationNumber, availability, dailyRate)
            vehicleService.add_vehicle(vehicle)
            print("Vehicle Added sucessfully!!")
        elif choice == '5':
            vehicle_id = input("Enter vehicle ID to be updated: ")
            model = input("Enter Model: ")
            make = input("Enter Make: ")
            year = input("Enter Year: ")
            color = input("Enter Color: ")
            registrationNumber = input("Enter Registration Number: ")
            availability = int(input("Enter Availability (True=1/False=0): "))
            dailyRate = 1
            vehicle = Vehicle(vehicle_id, model, make, year, color, registrationNumber, availability, dailyRate)
            vehicleService.update_vehicle(vehicle)
            print("Vehicle updated successfully!!")
        elif choice == '6':
            vehicle_id = input("Enter vehicle ID: ")
            vehicleService.remove_vehicle(vehicle_id)
            print("Vehicle deleted successfully!!")
        elif choice == '7':
            print("Report Generation\n1.By Vehicle\n2.By Customer\n3.By Reservation\n4.By Admin\n")
            ch = int(input("Enter choice to generate report: "))
            if ch == 1:
                vehicleID = int(input("Enter Vehicle ID: "))
                reportGenerator.generate_vehicle_report(vehicleID)
            elif ch == 2:
                Customer_ID = int(input("Enter Customer ID: "))
                reportGenerator.generate_customer_report(Customer_ID)
            elif ch == 3:
                Reservation_ID = int(input("Enter Reservation ID: "))
                reportGenerator.generate_reservation_report(Reservation_ID)
            elif ch == 4:
                Admin_ID = int(input("Enter Admin ID: "))
                reportGenerator.generate_admin_report(Admin_ID)

        elif choice == '8':
            print("Exiting Admin Actions...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def admin_workflow():
    while True:
        print("Welcome to CarConnect - Car Rental Platform")
        print("1. Admin Registration")
        print("2. Admin Login")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            a = AdminService()
            last_admin_id = 0
            admin_id = last_admin_id + 1
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role: ")
            join_date = input("Enter join date: ")
            admin = Admin(admin_id, first_name, last_name, email, phone_number, username, password, role, join_date)

            if a.register_admin(admin=admin):
                print("Registration successful!")
            else:
                print("Registration failed. Please try again.")
        elif choice == '2':
            print("Admin Login:")
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authentication_service.authenticate_admin(username, password):
                print("Login successful!")
                print(f"Hello {username}!!")
                handle_admin_actions()
            else:
                print("Login failed. Incorrect username or password.")
        elif choice == '3':
            print("Logged out!!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def main():
    while True:
        print("Welcome to the Reservation System")
        print("Are you a customer or an admin?")
        print("1. Customer")
        print("2. Admin")
        print("3. Quit")
        user_type = int(input("Enter your choice: "))
        if user_type == 1:
            customer_workflow()
        elif user_type == 2:
            admin_workflow()
        elif user_type == 3:
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
