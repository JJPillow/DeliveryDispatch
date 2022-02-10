# Jennifer Pillow pillje@hotmail.com
# This program simulates a package delivery service. There are 40 packages
# to deliver, each with optional delivery requirements.

import csv
import datetime
from DistanceGraph import Location, Graph, dijkstra_shortest_path
from Package import Package
from Truck import Truck
from HashTable import HashTable

# Global variables
start_time = datetime.datetime.strptime('0800', "%H%M")  # Start time for delivery day is 8:00am
hash_table = HashTable()
dist_graph = Graph()
truck_1 = Truck(1)
truck_2 = Truck(2)
truck_3 = Truck(3)
TRUCK_SPEED = 0.3       # 18 mph is 0.3 miles/min


def main():
    """
    The main method for the program.
    """
    # import delivery locations and create vertices for graph
    dist_name_file = "Distance Names.csv"
    locations = []
    with open(dist_name_file, 'r') as csv_dist_name:
        csv_dist_reader = csv.reader(csv_dist_name)
        for row in csv_dist_reader:
            name = row[0]
            address = row[1]
            zipcode = row[2]
            new_location = Location(name, address, zipcode)
            dist_graph.add_location(new_location)
            locations.append(new_location)

    # import distance data and create graph
    dist_data_file = "Distance Data.csv"
    with open(dist_data_file, 'r') as csv_dist_data:
        csv_data_reader = csv.reader(csv_dist_data)
        row_index = 0
        for row in csv_data_reader:
            for col_index in range(row_index):
                dist_graph.add_distance(locations[row_index], locations[col_index], float(row[col_index]))
            row_index += 1

    # update distance graph with shortest distances using dijkstra's shortest path
    for loc in dist_graph.adj_list:
        dijkstra_shortest_path(dist_graph, loc)
    setup_hash_table()
    user_interface()


def user_interface():
    """
    Displays a user interface to the console.
    """
    print("\nPackage Delivery Monitor")

    # loop until exit is chosen
    is_exit = False
    while not is_exit:
        print("\nOptions:")
        print("1. Check Status at EOD")
        print("2. Check Status of All Packages at Specified Time")
        print("3. Check Status of Package at Specified Time")
        print("4. Exit the Program")
        option = input("Chose an option (1-4): ")
        if option == "1":
            # setup_hash_table()
            reset()
            # Run full day code
            end_t = sim_day()
            # Display status for all packages and total distance for trucks
            hash_table.print_all_packages()
            total_dist = truck_1.distance + truck_2.distance + truck_3.distance
            print("Truck 1: ", round(truck_1.distance, 1), " miles")
            print("Truck 2: ", round(truck_2.distance, 1), " miles")
            print("Truck 3: ", round(truck_3.distance, 1), " miles")
            print("Total miles: ", round(total_dist, 1))
            print("Day Ended: ", end_t.time())
        elif option == "2":
            # setup_hash_table()
            reset()
            stop_time = validate_time_input("all package statuses")
            # Run code till stop time
            sim_day(stop_time)
            # Display status for all packages and distance travelled for trucks
            print("Displaying all package data at: ", stop_time.time())
            hash_table.print_all_packages()
            total_dist = truck_1.distance + truck_2.distance + truck_3.distance
            print("Truck 1: ", round(truck_1.distance, 1), " miles")
            print("Truck 2: ", round(truck_2.distance, 1), " miles")
            print("Truck 3: ", round(truck_3.distance, 1), " miles")
            print("Total miles: ", round(total_dist, 1))
        elif option == "3":
            reset()
            stop_time = validate_time_input("package status")
            err_mess = "Please choose a valid package number!"
            pack = None
            while pack is None:
                try:
                    pack_num = int(input("Choose a package (1-40): "))
                    pack = hash_table.search(pack_num)
                except ValueError:
                    pass
                if pack is None:
                    print(err_mess)
            # run code till stop time
            sim_day(stop_time)
            # display status for chosen package
            print("Package#: ", str(pack.package_id), " Status at ", stop_time.time(), ": ", pack.status)
        elif option == "4":
            is_exit = True
        else:
            print("Please pick a valid option!")


def setup_hash_table():
    """
    Creates the hash table and populates it with package data from an external CSV file.
    """
    hash_table.clear_table()

    # import package data from csv file to hash table
    package_file = "Package File.csv"
    with open(package_file, 'r') as csvPackage:
        csv_reader_package = csv.reader(csvPackage)

        for hash_row in csv_reader_package:
            package_id = int(hash_row[0])
            addr = hash_row[1]
            city = hash_row[2]
            state = hash_row[3]
            zcode = hash_row[4]
            deadline = hash_row[5]
            weight = hash_row[6]
            notes = hash_row[7]
            package = Package(package_id, addr, city, state, zcode, deadline, weight, notes)
            hash_table.insert(package)


def reset():
    """
    Calls reset method for all the trucks and packages.
    """
    truck_1.reset_truck()
    truck_2.reset_truck()
    truck_3.reset_truck()
    hash_table.reset_packages()


def can_drive(dist, time=540.0):
    """
    Determines if the truck has enough time to drive the specified distance.

    :param dist: the distance to travel
    :type dist: float
    :param time: optional time in minutes, default is 540.0 (8am-5pm: 9 hrs = 540 minutes)
    :type time: float
    :return: the truck has enough time to drive the distance
    :rtype: bool
    """
    return TRUCK_SPEED * time >= dist


def run_route(truck, begin_time=start_time,
              end_time=datetime.datetime.strptime('1700', "%H%M")):
    """
    Simulates a truck route delivering the loaded packages.  Returns the earlier of: time the route
    completes or the specified end_time.

    The truck starts at the hub location, then drives to each address to deliver packages, in order
    by the delivery deadline.  Uses a greedy algorithm to determine the next nearest address. The
    truck returns to the hub when all packages have been delivered.

    :param truck: the truck to drive the route
    :type truck: Truck
    :param begin_time: optional time to begin route
    :type begin_time: datetime.datetime
    :param end_time: optional time to end the route (default: EOD)
    :type end_time: datetime.datetime
    :return: earlier of: the time the route completes, or the optional specified end_time
    :rtype: datetime.datetime
    """
    if len(truck.packages) < 1:
        return begin_time
    start_loc = list(dist_graph.adj_list.keys())[0]   # address of WGU Hub
    curr_loc = start_loc
    curr_time = begin_time
    next_dist = float("inf")
    time_rem = (end_time - begin_time).seconds/60

    # sort package locations into lists based on delivery deadline
    nine_am_queue = []      # packages with a 9:00 am deadline
    ten_am_queue = []       # packages with a 10:30 am deadline
    eod_queue = []          # packages with EOD deadline
    for mail in truck.packages:
        del_addr = dist_graph.search_location(mail.address)
        if '9:00' in mail.deadline:
            if del_addr not in nine_am_queue:
                if del_addr in ten_am_queue:
                    ten_am_queue.remove(del_addr)
                if del_addr in eod_queue:
                    eod_queue.remove(del_addr)
                nine_am_queue.append(del_addr)
        elif '10:30' in mail.deadline:
            if (del_addr not in ten_am_queue) and (del_addr not in nine_am_queue):
                if del_addr in eod_queue:
                    eod_queue.remove(del_addr)
                ten_am_queue.append(del_addr)
        else:
            if (del_addr not in ten_am_queue) and (del_addr not in nine_am_queue):
                if del_addr not in eod_queue:
                    eod_queue.append(del_addr)

    unvisited_queue = eod_queue     # set default queue

    # if there are packages with a 10:30 am deadline time switch lists to put them first on route
    if len(ten_am_queue) > 0:
        unvisited_queue = ten_am_queue

    # if there are packages with a 9:00 am deadline time switch lists to put them first on route
    if len(nine_am_queue) > 0:
        unvisited_queue = nine_am_queue

    # find location in unvisited queue with shortest distance
    while len(unvisited_queue) > 0:
        sm_index = 0
        if len(unvisited_queue) == 1:
            next_dist = dist_graph.distance[(curr_loc, unvisited_queue[0])]
        else:
            for i in range(1, len(unvisited_queue)):
                # compare (distance from curr_loc to loc(i)) with (distance from curr_loc to loc(sm_index))
                sm_dist = dist_graph.distance[(curr_loc, unvisited_queue[sm_index])]
                if dist_graph.distance[(curr_loc, unvisited_queue[i])] < sm_dist:
                    sm_index = i    # update sm_index with index of smallest distance
                    next_dist = dist_graph.distance[(curr_loc, unvisited_queue[i])]
                else:
                    next_dist = sm_dist
        if can_drive(next_dist, time_rem):
            truck.drive(next_dist)
            curr_loc = unvisited_queue[sm_index]  # travel to shortest dist location

            time_rem -= next_dist / TRUCK_SPEED
            travel_t = next_dist/TRUCK_SPEED
            curr_time = curr_time + datetime.timedelta(seconds=travel_t * 60)
            dlvr_time = curr_time.time()

            for mail in reversed(truck.packages):  # reversed so indexes changed by removal have already been iterated
                if dist_graph.search_location(mail.address) == curr_loc:
                    truck.deliver_package(mail, dlvr_time.strftime("%X"))
        else:
            truck.drive(TRUCK_SPEED * time_rem)
            curr_time = curr_time + datetime.timedelta(seconds=time_rem * 60)
            return curr_time

        unvisited_queue.pop(sm_index)
        # if there are no packages with a 9:00 deadline deliver the 10:30 deadline packages
        if len(unvisited_queue) < 1:
            unvisited_queue = ten_am_queue
        # if there are no packages with a 10:30 deadline deliver the EOD packages
        if len(unvisited_queue) < 1:
            unvisited_queue = eod_queue

    # return to hub
    hub_dist = dist_graph.distance[(curr_loc, start_loc)]
    if can_drive(hub_dist, time_rem):
        truck.drive(hub_dist)
        drive_time = hub_dist / TRUCK_SPEED
        curr_time = curr_time + datetime.timedelta(seconds=drive_time * 60)
    else:
        truck.drive(TRUCK_SPEED * time_rem)
        curr_time = curr_time + datetime.timedelta(seconds=time_rem * 60)
        return curr_time
    return curr_time


def sim_day(end_time=datetime.datetime.strptime('1700', "%H%M")):
    """
    Loads packages on all trucks and sends them on their routes.  Returns the earlier of the time
    all routes are completed with the delivery of all 40 packages, or the user specified end_time.

    :param end_time: optional time to end simulation before EOD
    :type end_time: datetime.datetime
    :return: earlier time of: user-specified time or time all routes have been completed
    :rtype: datetime.datetime
    """
    p1 = [13, 14, 15, 16, 19, 20, 21, 34, 39]
    p2 = [1, 3, 5, 7, 8, 11, 12, 18, 22, 23, 24, 29, 30, 36, 37, 38]
    p3 = [2, 4, 6, 9, 10, 17, 25, 26, 27, 28, 31, 32, 33, 35, 40]

    # send truck_1
    for j in p1:
        truck_1.load_package(hash_table.search(j))
    trip1 = run_route(truck_1, start_time, end_time)

    # send truck_2
    for k in p2:
        truck_2.load_package(hash_table.search(k))
    trip2 = run_route(truck_2, start_time, end_time)

    # determine the earliest time at which a truck returns to hub
    if trip1 < trip2:
        next_time = trip1
    else:
        next_time = trip2

    # truck 3 leaves at 9:50am or whenever a driver is available, whichever is later
    t3_leave = datetime.datetime.strptime('0950', "%H%M")
    if end_time < t3_leave:
        return end_time
    if next_time < t3_leave:
        next_time = t3_leave

    for m in p3:
        truck_3.load_package(hash_table.search(m))
    trip3 = run_route(truck_3, next_time, end_time)

    done_time = trip1
    if trip2 > done_time:
        done_time = trip2
    if trip3 > done_time:
        done_time = trip3
    return done_time


def validate_time_input(prnt):
    """
    Validates user input of a string in HHMM format and converts it to a datetime.

    :param prnt: string to change text displayed to the user
    :type prnt: str
    :return: the time entered by the user converted to datetime
    :rtype: datetime.datetime
    """
    inp_time = None
    while inp_time is None:
        try:
            prt_str = "Input a time to see " + prnt + ", 24-hr clock format(HHMM) (ex: 0935 or 1632): "
            inp_time = datetime.datetime.strptime(input(prt_str), "%H%M")
            if inp_time <= start_time:
                inp_time = None
                print("Enter a time after 0800")
        except ValueError:
            print("Please enter a valid time in HHMM format")

    return inp_time


if __name__ == "__main__":
    main()
