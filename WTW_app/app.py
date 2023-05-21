import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from WTW_app.settings import SETTINGS
from WTW_app.routers.films import films_router
from WTW_app.routers.directors import directors_router

logger = logging.getLogger()


app = FastAPI(title=SETTINGS.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def scrap_data():
    import requests
    from bs4 import BeautifulSoup
    from progressbar import progressbar
    from WTW_app.repositories.interfaces import IFilmsRepository
    from WTW_app.repositories.films_in_memory import films_in_memory
    
    print('Data scrapping started...')
    print('Getting the data responses...')

    responses = []

    for url in SETTINGS.scrap_data_urls:
        partial_list_response = requests.get(url)
        responses.append(partial_list_response)

    print('Extracting the data responses...')

    movies_list = []

    for resp in responses:
        partial_s_list = BeautifulSoup(resp.text, 'html.parser')
        movies = partial_s_list.find_all("div", class_="lister-item mode-advanced")
        movies_list.append(movies)

    movies_list = [movie for m_list in movies_list for movie in m_list]
    
    print('Scrapping movies\' data:')
    
    for movie in progressbar(movies_list, redirect_stdout=True):
        # Get the movie's title
        title_element = movie.find('h3').find('a')
        if title_element is not None:
            title = title_element.text
        else:
            title = "Title not found"
            
        # Get the link providing to the movie's details
        f_details_reflink = movie.find('h3').find('a')['href']
        film_details_url = f'https://www.imdb.com{f_details_reflink}fullcredits'
        
        # Get the year of movie's production
        year_element = movie.find('h3').find('span', class_='lister-item-year')
        if year_element is not None:
            year = year_element.text.split(' ')
            if len(year) > 1:
                year = year[1].strip('()')
            else:
                year = year[0].strip('()')
            year = int(year)
        else:
            year = 2000
            
        # Get the movie's rating
        rate_element = movie.find('div', class_='ratings-bar').find('strong')
        if rate_element is not None:
            rate = rate_element.text
            rate = float(rate)
        else:
            rate = 6.6
            
        # Get the movie's description
        paragraphs = movie.find_all('p', class_='text-muted')
        description_element = paragraphs[1]
        if description_element is not None:
            description = description_element.text.strip()
        else:
            description = "Description not found"
            
        # Get the movie's image url
        details_response = requests.get(film_details_url)
        soup_details = BeautifulSoup(details_response.text, 'html.parser')
        img_url_element = soup_details.find('div', class_='subpage_title_block').find('img', class_='poster')
        if img_url_element is not None:
            img_url = img_url_element['src']
        else:
            img_url = None
            
        # print(title)
        # print(year)
        # print(rate)
        # print(description)
        # print(img_url)
        # print('------------------------------------\n')
        
        films_repository: IFilmsRepository = films_in_memory
        
        films_repository.add_film(
        title=title,
        year=year,
        rate=rate,
        img_url=img_url,
        director_id=1
    )
        
    
app.add_event_handler("startup", scrap_data)

app.include_router(films_router)
app.include_router(directors_router)