import requests, re, time
from bs4 import BeautifulSoup

class Annuncio:
    def __init__(self, sito, tag, link, img, price, *attrs):
        self.sito = sito
        self.tag = tag
        self.link = link
        self.img = img
        self.price = re.sub('\D', '', price).replace(" ", "")
        self.attrs = attrs

    def __str__(self):
        return f"{self.tag}\nLink: {self.link}\nImg: {self.img}\nPrice: {self.price}\nAttrs: {self.attrs}\n\n\n"


def Bakeca(link, type) -> list:
    sito = "Bakeca"
    lista = []
    keywords = {"regex_item": ".*annuncio-foto-grande.*"}
    headers = {"headers":"parameters"}

    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")

    regex = re.compile(keywords['regex_item'])
    results = soup.find_all("section", class_=regex)

    for res in results:
        element = list(res.children)[0]

        href = element['href']

        img_link, price = Bakeca_img_price(href)

        lista.append(Annuncio(sito, type, href, img_link, price, []))

    return lista

def Bakeca_img_price(link) -> tuple[str, str]:

    banned_phrases = ["appartamento arredato centro padova", "Monolocale in affitto a Padova (COMPLETAMENTE ARREDATO)", "BILOCALE IN AFFITO A PADOVA"]

    ##Prendi link
    headers = {"headers":"parameters"}

    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")

    ##La slide con l'immagine contiene CarouselCell nel nome classe, price per il prezzo
    regex_img = re.compile(".*w-full h-full object-center object-contain.*")
    regex_price = re.compile(".*meta-block bg-transparent w-1/2 p-2 text-gray-900.*")

    ##Trova la prima slide e prendi src, se non c'è immagine fai None
    try:
        img_link = soup.find("img", class_=regex_img)['src']
    except: img_link = None

    ##Trova prezzo
    try:
        price = soup.find("div", class_=regex_price).get_text()
    except:
        price = None

    for phrase in banned_phrases:
        if phrase in soup.text:
            price = "10"

    return img_link, price


def Immobiliare(link, type) -> list:
    sito = "Immobiliare"
    keywords = {"key":"words"}

    lista = []
    req = requests.get(link)
    soup = BeautifulSoup(req.content, "html.parser")

    ##Trova tutti gli annunci
    results = soup.find_all(class_=keywords['item'])

    for res in results:
        element = list(res.children)[0]

        href = element['href']

        ##Trova immagine e prezzo
        img_link, price = Immobiliare_img_price(href)

        ##Trova caratteristiche
        caratt = [f"{el['aria-label']}: {el.get_text()}" for el in res.find_all("li", class_=keywords["caratt"])]

        lista.append(Annuncio(sito, type, href, img_link, price, caratt))

    return lista
def Immobiliare_img_price(link) -> tuple[str, str]:

    ##Prendi link
    req = requests.get(link)
    soup = BeautifulSoup(req.content, "html.parser")

    ##La slide con l'immagine contiene CarouselCell nel nome classe, price per il prezzo
    regex_price = re.compile(".*price.*")

    ##Trova la prima slide e prendi srcset, se non c'è immagine fai None
    try:
        img_link = list(soup.find("nd-showcase", class_="nd-mosaicGallery__item nd-ratio nd-ratio--standard").childGenerator())[1]['src']
    except:
        img_link = None

    ##Trova prezzo
    try:
        price = soup.find("li", class_=regex_price).get_text()
    except:
        price = None

    return img_link, price

def Idealista(link, type) -> list:
    sito = "Idealista"
    ##Headers altrimenti non fa entrare
    headers = {"headers":"parameters"}

    ##Keywords utili per ricerca del singolo annuncio, più regex per le caratteristiche
    keywords = {"item": "item-info-container",
                "caratt":"item-detail" }
    lista = []
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    ##Trova tutti gli annunci
    results = soup.find_all("div", class_=keywords['item'])

    for res in results:

        href = "https://www.idealista.it"+res.a['href']
        if "pro" in href:
            href = "https://www.idealista.it"+list(res.children)[3]['href']
        ##Trova immagine e prezzo
        img_link = None
        try:
            price = res.find("span", class_="item-price h2-simulated").get_text()
        except:
            price = None

        ##Trova caratteristiche
        caratt = [res_2.get_text() for res_2 in res.find_all("span", class_="item-detail")]

        lista.append(Annuncio(sito, type, href, img_link, price, caratt))

    return lista

def Casa(link, type)->list:
    sito = "Casa.it"

    headers = {"headers":"parameters"}
    
    img_link = None

    lista = []
    req = requests.get(link, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")

    results = soup.find('div', class_='list').find_all('article')

    for res in results:

        try:
            href = "https://www.casa.it"+res.find('a', 'csa-gallery__imga')['href']
        except: href = ""

        try:
            price = res.find('div', re.compile('.*price.*')).text
            price = re.sub('\D', '', price)
        except: price = None

        try:
            caratt = [f"{element.text}" for element in res.find_all('div', "grid-item info-features__item grid-item grid-item--behavior-fixed")]
        except:
            caratt = []

        lista.append(Annuncio(sito, type, href, img_link, price, caratt))

    return lista

if __name__=="__main__":
    pass