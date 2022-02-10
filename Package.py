# Jennifer Pillow pillje@hotmail.com

class Package:
    """
    A class used to represent a package to be delivered.

    Attributes
    ----------
    package_id : int
        the ID number for the package, should be unique
    address : str
        the street address for delivery of the package
    city : str
        the city for delivery of the package
    state : str
        the state for delivery of the package
    zipcode : str
        the zipcode for delivery of the package
    deadline : str
        the time the package must be delivered by
    weight : int
        the weight of the package
    notes : str
        special notes providing constraints for the package
    status : str
        the status of the package (default 'AT HUB')

    Methods
    ---------
    __repr()
        Returns a formatted string representation of the package.
    """

    def __init__(self, package_id, address, city, state, zipcode, deadline, weight, notes, status='AT HUB'):
        """
        Constructor for the Package class.

        :param package_id: the ID number for the package, should be unique
        :type package_id: int
        :param address: the street address for delivery of the package
        :type address: str
        :param city: the city for delivery of the package
        :type city: str
        :param state: the state for delivery of the package
        :type state: str
        :param zipcode: the zipcode for delivery of the package
        :type zipcode: str
        :param deadline: the time the package must be delivered by
        :type deadline: str
        :param weight: the weight of the package
        :type weight: str
        :param notes: special notes providing constraints for the package
        :type notes: str
        :param status: optional status of the package (default 'AT HUB')
        :type status: str
        """
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.weight = weight
        self.status = status
        self.notes = notes
        self.state = state

    def __repr__(self):
        """
        Returns a formatted string representation of the package.

        Returned string includes the package_id, full address, the package weight, and the status.
        Overrides the default __repr__(self) method.

        :return: a formatted string representation of the package
        :rtype: str
        """
        ret_string = "(ID: {}".format(self.package_id)
        ret_string += " Address: " + self.address + " " + self.city + ", " + self.state
        ret_string += " " + self.zipcode + " Weight: " + self.weight + " Status: " + self.status + ")"
        return ret_string
