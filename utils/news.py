from bs4 import BeautifulSoup
import requests
import os 


def get_article_links(ticker:str):
    html = requests.get(f"https://www.moneycontrol.com/news/tags/{ticker}.html")
    soup = BeautifulSoup(html.text, "html.parser")

    
    if ticker not in soup.title.text:
        raise Exception("Invalid ticker")
        
    links = set()
    ul = soup.find("ul", id="cagetory")
    if ul:
        li_elements = ul.find_all("a")
        for a in li_elements:
            links.add(a.get("href"))
    return links


def get_article(link:str):
    html = requests.get(link)
    soup = BeautifulSoup(html.text, "html.parser")
    content = soup.find("div", id="contentdata")
    if content:
        return content.text



def save_all_articles(ticker:str, directory="data"):

    if not os.path.exists(directory):
        os.mkdir(directory)

    links = get_article_links(ticker)
    for count,link  in enumerate(links):
        
        content = get_article(link)
        if content:
            path = os.path.join(directory, ticker +"_"+  str(count) + ".txt")
            with open(path, "w") as f:
                f.write(content)

save_all_articles("RELIANCE")