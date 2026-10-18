from bs4 import BeautifulSoup
import requests

url = "https://news.ycombinator.com/news"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all(class_="athing submission")
for article in titles:
    name = article.find(class_="titleline").find("a").getText()
    article_id = article.get("id")
    score = soup.find(id=f"score_{article_id}").getText()
    print(f"Article name: {name}\n"+
          f"Score: {score}\n")
















# with open("Web Devs (Day 41 -)/Day 45/website.html") as fp:
#     contents = BeautifulSoup(fp, 'html.parser')
    
# # print(contents.prettify())

# anchor_tags = contents.find_all(name="a")
# for tag in anchor_tags:
#     print(tag.get_text())