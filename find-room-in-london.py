#!/usr/bin/env python3
import sys
import bs4
import argparse
import json, csv
from myrooms.main import MyRooms
from spareroom.main import SpareRoom

def cmdline_args():
    # Make parser object
    p = argparse.ArgumentParser()
    
    p.add_argument("--myrooms", action="store_true", help="Search on myrooms.co.uk")
    p.add_argument("--spareroom", action="store_true", help="Search on spareroom.co.uk")

    return(p.parse_args())

def save_results(filename, rooms):
    results = [room.__dict__ for room in rooms]
    f = open(filename + '.csv', 'w')
    csvwriter = csv.writer(f)
    count = 0
    for emp in results:
        if count == 0:
            header = emp.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(emp.values())
    f.close()

def main(argv, args):
    rooms = list()

    if args.myrooms:
        rooms = MyRooms().get_rooms()
        save_results('myrooms', rooms)

    if args.spareroom:
        rooms = SpareRoom().get_rooms()
        save_results('spareroom', rooms)


if __name__ == '__main__':
    if sys.version_info<(3,0,0):
        sys.stderr.write("You need python 3.0 or later to run this script\n")
        sys.exit(1)
    
    args = cmdline_args()
    sys.exit(main(sys.argv[1:], args))