class SalesService:
    """
    [Summary]
    Service responsible for displaying goods to customers and managing sales.

    [Attributes]
    :param app: The Flask application instance.
    :type app: Flask

    [Methods]
    :raises InsufficientFundsError: If a customer has insufficient funds during a sale.
    :raises InsufficientStockError: If there is not enough stock during a sale.

    """

    def __init__(self, app):
        """
        [Summary]
        Constructor method for SalesService.

        :param app: The Flask application instance.
        :type app: Flask
        """
        self.app = app

    def display_available_goods(self):
        """
        [Summary]
        Display a list of available goods.

        :return: A list of dictionaries containing good name and price.
        :rtype: list
        """
        pass

    def get_goods_details(self, name):
        """
        [Summary]
        Get full information related to a specific good.

        :param name: The name of the good.
        :type name: str

        :return: Full information about the good.
        :rtype: dict
        """
        pass
