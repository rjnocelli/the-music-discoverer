from datetime import datetime, timedelta
from collections import defaultdict
from bs4 import BeautifulSoup
import httpx

london = '24426-uk-london'
barcelona = '28714-spain-barcelona'
girona = '56332-spain-girona'
figueres = '71256-spain-figueres'

start_time = datetime.now()
end_time = start_time + timedelta(days=200)
end_loop = False

def run_scraper(city: str, start_time: datetime, end_time: datetime):
    concerts = defaultdict(lambda: defaultdict(lambda: defaultdict(dict , **{'links': set()})))
    page = 1
    exit_loop = False
    with httpx.Client() as client:
        while not exit_loop:
            url = 'https://www.songkick.com/metro-areas/{}?page={}'
            response = client.get(url.format(city, page))
            soup = BeautifulSoup(response.text, 'html.parser')
            concert_data = soup.find_all(class_='event-listings-element')
            
            # ojo con esto – que no es lo mismo que esto -
            for c_d in concert_data:
                date = c_d.get('title').strip().split('–')[0].strip()
                parsed_date = datetime.strptime(date, '%A %d %B %Y')
                
                if parsed_date > end_time:
                    exit_loop = True
                    break
                
                event_data = c_d.find_all(class_='event-details-wrapper')
                for a in event_data:
                    event_link = a.find(class_='event-link')
                    if event_link:
                        event_link_href = event_link.get('href')
                        if event_link.span:
                            name = event_link.span.text.strip()
                            concerts[parsed_date][name]['links'].add(event_link_href) 
            print_scraper_data(concerts)
            page += 1
        return concerts

def print_scraper_data(data: dict):            
    for k, v in data.items():
        for j, l in v.items():
            print(f"{k} - {j} - {'- '.join(l['links'])}")
                
run_scraper(london, start_time, end_time)