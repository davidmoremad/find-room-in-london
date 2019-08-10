#!/usr/bin/env python3
import sys
import bs4
import json, csv
from myrooms.main import MyRooms

def save_results(results):
    f = open('rooms.csv', 'w')
    csvwriter = csv.writer(f)
    count = 0
    for emp in results:
        if count == 0:
            header = emp.keys()
            csvwriter.writerow(header)
            count += 1
        csvwriter.writerow(emp.values())
    f.close()

def main(arguments):
    rooms = MyRooms().get_rooms()
    results = [room.__dict__ for room in rooms]
    save_results(results)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))