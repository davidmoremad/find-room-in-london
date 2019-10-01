#!/usr/bin/env python3
import fire
import csv
from myrooms import MyRooms
from spareroom import SpareRoom

def _save_results(filename, rooms):
    results = [room.__dict__ for room in rooms]
    f = open(filename + '.csv', 'w')
    csvwriter = csv.writer(f)
    count = 0
    for emp in results:
        if count == 0:
            header = emp.keys()
            csvwriter.writerow(header)
            count += 1
        try:
            csvwriter.writerow(emp.values())
        except Exception as e:
            pass
    f.close()
    print('[+] Resuls saved: ./{}.csv'.format(filename))

def myrooms():
    rooms = MyRooms().get_rooms()
    _save_results('myrooms', rooms)

def spareroom():
    rooms = SpareRoom().get_rooms()
    _save_results('spareroom', rooms)

if __name__ == '__main__':
    fire.Fire()