from bs4 import BeautifulSoup
import requests

root_url = "http://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm"
pages_to_scrap = 3000
out = open('./out.txt', 'a')

def getText(url):
    try:
        r = requests.get(url)    
        data = r.text
        soup = BeautifulSoup(data, features="lxml")    
        div = soup.find('div', attrs={"class": "conteneur-messages-pagi"})
        all_p = div.find_all('p')
        for p in all_p:
            out.write(p.text)
    except:
        print("URL not found")
    
def fetch_thread():
    global root_url
    try:
        r = requests.get(root_url)
        data = r.text
        soup = BeautifulSoup(data, features="lxml")    

        topic_list = soup.find('ul', attrs={"class": "topic-list"})
        all_links = topic_list.find_all('a')

        list_links = []

        for l in all_links:
            parse = l.attrs['href'].split('-')
            test = False
            if 'tinder' in parse:    
                test = True
            if not test:
                list_links.append('http://www.jeuxvideo.com' + l.attrs['href'])

        root_url = 'http://www.jeuxvideo.com' + soup.find('a', attrs={"class": "pagi-suivant-actif"}).attrs['href']

        return list_links
    except:
        print("Erreur lors de la récupération des threads")
    
def main():
    global pages_to_scrap        
    while pages_to_scrap > 0:
        links = fetch_thread()
        for l in links:
            getText(l)
            pages_to_scrap -= 1   
    

main()
out.close()