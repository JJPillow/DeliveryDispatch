# Jennifer Pillow pillje@hotmail.com

from Package import Package


class Truck:
    """A class used to represent a delivery truck

    Attributes
    ----------
    packages : list
        a list of packages that are loaded on the truck
    distance : float
        the total distance travelled by the truck during the delivery day
    truck_id : int
        an identifying number for the truck, should be unique for each instance

    Methods
    --------
    get_num_packages()
        Returns the number of packages in the truck's package list
    load_package(package)
        Adds a package to the trucks package list
    deliver_package(package, del_time)
        Removes the package from the trucks package list and updates the package status
    drive(dist)
        Increases the truck's distance attribute by the amount of the passed value dist.
    empty_truck()
        Removes all packages from the truck's package list
    reset_truck()
        Removes all packages from the truck's package list and sets the truck's distance parameter to zero
    __repr__():
        Returns a formatted string representation of the truck.
    """

    def __init__(self, tr_id):
        """
        Constructor for the Truck class

        :param tr_id: The identifying number for the truck, should be unique
        :type tr_id: int
        """
        self.packages = []
        self.distance = 0.0
        self.truck_id = tr_id

    def get_num_packages(self):
        """
        Returns the number of packages in the truck's package list

        :return: The number of packages in the truck's package list
        :rtype: int
        """
        return len(self.packages)

    def load_package(self, package):
        """
        Adds a package to the truck's package list.

        Only adds package if: the package is not None type, not already in the truck's package list,
        the truck's package list has less than 16 packages, and the package status is "AT HUB".

        :param package: The package to add to the truck
        :type package: Package
        :return: The success of adding the package to the truck
        :rtype: bool
        """
        if package is not None and package not in self.packages:
            if self.get_num_packages() < 16 and package.status == "AT HUB":
                self.packages.append(package)
                package.status = ("EN ROUTE ON TRUCK " + str(self.truck_id))
                return True
        # print("package", package.package_id, " load error on truck", self.truck_id)
        return False

    def deliver_package(self, package, del_time):
        """
        Removes a package from the truck's package list and changes the status.

        :param package: package to deliver
        :type package: Package
        :param del_time: delivery time
        :type del_time: str
        """
        if package in self.packages:
            package.status = "Delivered at " + del_time  # add delivery time
            self.packages.remove(package)
        else:
            print("delivery error for package ", package.package_id)

    def drive(self, dist):
        """
        Increases the truck's distance attribute by the amount of the passed value dist.

        :param dist: The distance the truck travelled
        :type dist: float
        """
        self.distance += dist

    def empty_truck(self):
        """
        Removes all packages from the truck's package list
        """
        self.packages.clear()

    def __repr__(self):
        """
        Returns a formatted string representation of the truck.

        Returned string includes the truck_id, # of packages in package list, the package IDs
        for the packages in the package list, and the distance travelled.  Overrides the default
        __repr__(self) method.

        :return: A string representation of the truck
        :rtype: str
        """
        ret_str = "Truck " + str(self.truck_id)
        ret_str += " # of Packages: " + str(self.get_num_packages()) + "  Package IDs: "
        for package in self.packages:
            ret_str += str(package.package_id) + ", "
        ret_str = ret_str[:-2]
        ret_str += "  Distance Travelled: " + str(self.distance)
        return ret_str

    def reset_truck(self):
        """
        Removes all packages from the truck's package list and sets the truck's distance parameter to zero.
        """
        self.empty_truck()
        self.distance = 0
