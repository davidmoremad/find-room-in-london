import requests
import re
from datetime import date
from bs4 import BeautifulSoup
from .room import Room

class SpareRoom:

    DOMAIN = 'https://www.spareroom.co.uk'
    URL_ROOMS = DOMAIN + '/flatshare'
    URL_SEARCH = URL_ROOMS + '/search.pl?nmsq_mode=normal&action=search&max_per_page=&flatshare_type=offered&search=London+Zone+1+to+2&min_rent=%i&max_rent=%i&per=pw&available_search=N&day_avail=10&mon_avail=08&year_avail=2019&min_term=0&max_term=0&days_of_wk_available=7+days+a+week&showme_rooms=Y'

    def __init__(self, min_price=180, max_price=290):
        r = requests.get(self.URL_SEARCH % (min_price, max_price))
        s = BeautifulSoup(r.content, 'lxml')
        self.url = r.url + 'offset=%i'
        self.pages = int(int(s.find("p", {"class":"navcurrent"}).findAll("strong")[1].string[:-1]) / 10)

    def _get_soup(self, url):
        '''
        Make request & return soup
        '''
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 200:
            return BeautifulSoup(r.content, 'lxml')
        elif r.status_code == 301:
            print('Finalizado')
            exit(0)
        else:
            print('[X] Response %s .Something went wrong.' % r.status_code)
            exit(1)

    def _get_room_info(self, room_soup):
        '''
        Parse HTML to Object
        '''
        room = Room()

        header = room_soup.find("header", {"class":"desktop"})
        body = room_soup.find("div", {"class":"desktop"})

        room.title = str(header.h1.text.strip().encode('utf-8'))
        room.desc = str(body.p.text.strip().replace('\r\n','').encode('utf-8'))
        room.url = str(self.DOMAIN + header.a['href'])
        room.location = str(header.find("span",{"class":"listingLocation"}).text)
        room.type = str(header.find("em",{"class":"shortDescription"}).text.replace(room.location, ''))
        price = header.find('strong', {"class":"listingPrice"}).text.strip()
        room.pw_price = '-'.join(re.findall('[0-9]{3,4}', price)) if 'pw' in price else None
        room.pcm_price = '-'.join(re.findall('[0-9]{3,4}', price)) if 'pcm' in price else None
        room.bills_included = bool('Bills inc.' in header.find("em",{"class":"listingPriceDetails"}).text)
        room.available_now = bool('Available Now' in body.text)
        room.new_today = bool(room_soup.find("mark",{"class":"new-today"}))

        return room

    def _get_rooms_info(self, rooms_soup):
        '''
        Iterate rooms & return object list
        '''
        rooms = list()
        for room in rooms_soup.find_all('article'):
            rooms.append(self._get_room_info(room))
        return rooms

    def get_rooms(self):
        '''
        Main method
        '''
        rooms = list()
        
        for i in range(0, 500, 10):
            print('[ ] Visited pages:%i/%i \tRooms: %i' % (i+1, i+10, len(rooms)))
            soup = self._get_soup(self.url % i)
            rooms.extend(self._get_rooms_info(soup))

        return rooms