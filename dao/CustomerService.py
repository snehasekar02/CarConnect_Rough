from dao.ICustomerService import ICustomerService
from entity.Customer import Customer
from dao.DatabaseContext import DatabaseContext
from exception.CustomerNotFoundException import CustomerNotFoundException


def get_connection():
    return DatabaseContext.getConnection(r'D:\Hexaware\CarConnect\util\db.properties')


'''
def close_connection(cursor, connection):
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
'''


class CustomerService(ICustomerService):

    def get_customer_by_id(self, customer_id):

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Customer WHERE customer_id = ?", (customer_id,))
            customer_data = cursor.fetchone()

            if not customer_data:
                raise CustomerNotFoundException("Admin with ID {} not found".format(customer_id))

            customer = Customer(*customer_data)
            return customer

        except Exception as e:
            print("Error:", e)
            return None

    def get_customer_by_username(self, username):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Customer WHERE Username= ?", (username,))
            customer_data = cursor.fetchone()

            if not customer_data:
                raise CustomerNotFoundException("Admin with username {} not found".format(username))

            customer = Customer(*customer_data)
            return customer

        except Exception as e:
            print("Error:", e)
            return None

    def register_customer(self, customer):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "INSERT INTO Customer (customer_id, first_name, last_name, email, phone_number, address, username,"
                "password,registration_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (customer.get_customer_id(), customer.get_first_name(), customer.get_last_name(), customer.get_email(),
                 customer.get_address(), customer.get_phone_number(), customer.get_username(),
                 customer.get_password(), customer.get_registration_date()))

            connection.commit()

            return True

        except Exception as e:
            print("Error:", e)
            return False

    def update_customer(self, customer):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "UPDATE  Customer SET firstName=?, lastName=?, email=?, phoneNumber=?,username=?,password=?,role=?,joinDate=? WHERE customer_id,=?",
                (customer.firstName, customer.lastName, customer.email, customer.phoneNumber, customer.username,
                 customer.password,
                 customer.role, customer.joinDate, customer.customer_id,))
            connection.commit()

            return True

        except Exception as e:
            print("Error:", e)
            return False

    def delete_customer(self, customer_id):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("DELETE FROM Customer WHERE customer_id=?", (customer_id,))
            connection.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False
