import requests
import time
from datetime import date
from bs4 import BeautifulSoup
from .room import Room

class MyRooms:

    DOMAIN = 'https://myrooms.co.uk'
    URL_ROOMS = DOMAIN + '/properties/'
    URL_ROOMS_PAGE = URL_ROOMS + 'page/%s/'

    URL_UPLOADS = 'https://myrooms.co.uk/wp-content/uploads/'
    _HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    def __init__(self, min_price=180, max_price=290):
        self._filters = "?price=%i%%2C%i" % (min_price, max_price)

    def _get_soup(self, url):
        '''
        Make request & return soup
        '''
        time.sleep(0.5)
        url = url + self._filters
        r = requests.get(url, headers=self._HEADERS)
        if r.status_code == 200:
            return BeautifulSoup(r.content, 'lxml')
        else:
            print('[X] Response %s .Something went wrong.' % r.status_code)
            exit(1)

    def _get_room_info(self, room_soup):
        '''
        Parse HTML to Object
        '''
        room = Room()

        head = room_soup.find('div', {"class":"room-head"})
        pict = head.a['data-image-src'].replace(self.URL_UPLOADS,'')[:7] # Date of the photo
        body = room_soup.find('div', {"class":"room-body"})

        room.desc = str(body.h3.string)
        room.url = str(head.a['href'])
        room.available_now = bool('available-now-box' in room_soup['class'])
        room.week_price = int(head.find('div', {"class":"price"}).text.replace('WEEKLY','').strip()[1:])
        room.location = body.p.text.strip() if body.p else ""
        for li in body.find_all('li'):
            room.topics.append(li.text.strip())
        try:
            room.photos_taken_on = date(int(pict[:4]), int(int(pict[-2:])), 1)
        except:
            room.photos_taken_on = None

        return room

    def _get_rooms_info(self, rooms_soup):
        '''
        Iterate rooms & return object list
        '''
        rooms = list()
        for room in rooms_soup.find_all('div', {"class":"room-box"}):
            rooms.append(self._get_room_info(room))
        return rooms

    def get_rooms(self):
        '''
        Main method
        '''
        rooms = list()
        
        soup = self._get_soup(self.URL_ROOMS)
        rooms.extend(self._get_rooms_info(soup))
        
        pages = int(soup.find_all('a', {"class":"page-numbers"})[-2].string)
        for i in range(1, pages + 1):
            print('Loading... Page:%i/%i \t Rooms: %i' % (i, pages, len(rooms)))
            soup = self._get_soup(self.URL_ROOMS_PAGE % i)
            rooms.extend(self._get_rooms_info(soup))

        return rooms