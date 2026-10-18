from bs4 import BeautifulSoup
import requests


URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
soup = (BeautifulSoup(response.text, "html.parser"))

titles = soup.find_all(name="h3", class_="title")
for title in titles:
    print(f"{title.getText()}")