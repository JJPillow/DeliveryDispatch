# Jennifer Pillow pillje@hotmail.com

from Package import Package


class HashTable:
    """
    A class that creates a chaining hash table using a list of lists.

    Attributes
    -----------
    table : list
        a list holding the buckets for the chaining hash table

    Methods
    ----------
    search(key)
        Searches for a package in the hash table by package ID
    insert(package)
        Inserts a package into the hash table.
    remove(package_id)
        Removes a package from the hash table.
    print()
        Displays all packages in the hash table to the console, grouped by hash table bucket.
    print_all_packages()
        Displays all packages to the console, one package per line.
    print_package(key)
        Displays one selected package to the console.
    clear_table()
        Removes all packages from the hash table.
    """

    def __init__(self, num_buckets=10):
        self.table = []
        for i in range(num_buckets):
            self.table.append([])

    def search(self, key):
        """
        Searches for a package in the hash table by package ID

        :param key: the package ID value
        :type key: int
        :return: the package whose ID value matches, returns None if not found
        :rtype: Package
        """
        bucket = key % len(self.table)
        bucket_list = self.table[bucket]
        for item in bucket_list:
            if item.package_id == key:
                return item
        return None

    def insert(self, package):
        """
        Inserts a package into the hash table.

        :param package: the package to insert into the hash table
        :type package: Package
        :return: a bool indicating the success of the insertion
        :rtype: bool
        """
        key = package.package_id
        if self.search(key) is None:
            bucket = key % len(self.table)
            bucket_list = self.table[bucket]
            bucket_list.append(package)
            return True
        return False

    def remove(self, package_id):
        """
        Removes a package from the hash table.

        :param package_id: the package ID of the package to remove
        :type package_id: int
        """
        key = package_id
        bucket = key % len(self.table)
        bucket_list = self.table[bucket]

        if key in bucket_list:
            bucket_list.remove(key)

    def print(self):
        """
        Displays all packages in the hash table to the console, grouped by hash table bucket.
        """
        print('-------Hash Table-------')
        for package in self.table:
            print(str(package))

    def print_all_packages(self):
        """
        Displays all packages to the console, one package per line.
        """
        for row in self.table:
            for package in row:
                print(package)

    def reset_packages(self):
        """
        Resets status for all packages to "AT HUB".
        """
        for row in self.table:
            for package in row:
                package.status = "AT HUB"

    def print_package(self, key):
        """
        Displays one selected package to the console.

        :param key: the package ID of the package to display
        :type key: int
        """
        print(self.search(key))

    def clear_table(self):
        """
        Removes all packages from the hash table.
        """
        for row in self.table:
            row.clear()
