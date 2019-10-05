# Find room in London

![](https://github.com/davidmoremad/find-room-in-london/workflows/Scheduled%20Workflow/badge.svg)

In my first days in London it was very tedious to spend every day consulting the 
new rooms and apartments in the different web pages (spareroom, myrooms, etc...) 
so I made this small script to store everything in a CSV file and thus be able to 
make generic queries about all available rooms.

This dummy script lists all rooms available on https://myrooms.co.uk and 
https://spareroom.co.uk and store them in an excel to make your own queries 
(their webs sucks).

### Usage

```bash
python3 find-room-in-london.py myrooms
python3 find-room-in-london.py spareroom
```

