class CustomerService:
    """
    [Summary]
    Service responsible for registering customers and managing their credits and payments.

    [Attributes]
    :param app: The Flask application instance.
    :type app: Flask

    [Methods]
    :raises UniqueUsernameError: If the provided username already exists during registration.

    """

    def __init__(self, app):
        """
        [Summary]
        Constructor method for CustomerService.

        :param app: The Flask application instance.
        :type app: Flask
        """
        self.app = app

    def register_customer(self, full_name, username, password, age, address, gender, marital_status):
        """
        [Summary]
        Register a new customer.

        :param full_name: The full name of the customer.
        :type full_name: str
        :param username: The username for the customer. Should be unique.
        :type username: str
        :param password: The password for the customer.
        :type password: str
        :param age: The age of the customer.
        :type age: int
        :param address: The address of the customer.
        :type address: str
        :param gender: The gender of the customer.
        :type gender: str
        :param marital_status: The marital status of the customer.
        :type marital_status: str

        :raises UniqueUsernameError: If the provided username already exists during registration.
        """
        pass

    def delete_customer(self, username):
        """
        [Summary]
        Delete a customer.

        :param username: The username of the customer to be deleted.
        :type username: str
        """
        pass

    # Additional methods for other functionalities...
