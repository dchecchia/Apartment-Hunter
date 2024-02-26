import telebot
from utilities import *


sites = {"bakeca.it": Bakeca, "immobiliare.it": Immobiliare, "idealista.it": Idealista, "casa.it": Casa}
sites_list = [key for key in sites.keys()]
database = {}

for site in sites_list:
    database[site] = []

loading = True

urls = ["Various Links", "of different websites", "with queries already", "configured", "i.e. immobiliare.it/padova/etc..."]

chat_id = ... # Canale Flaviuccia
bot = telebot.TeleBot("...")

def Checks(el):
    if not loading:
        try:
            price = float(el.price)
        except: return True

        #Flag prezzo a 10e nel caso in cui si tratti di scam
        if price == 10.0: return False

        if price>1600.0: return False
        return True
    else: return False

def SendMessage(element):
    text = f"Sito: {element.sito}\n" \
           f"Tipo: {element.tag}\n\n" \
           f"Link: {element.link}\n\n" \
           f"Prezzo: {element.price}€\n\n" \
           f"Varie: {element.attrs}"

    try:
        bot.send_message(chat_id, text)
    except Exception as e:
        print(f"Couldn't send message: {e}")
        time.sleep(30)
        SendMessage(element)

def main():
    while True:

        for site in sites_list:
            with open(f"Link Annunci/{site}.txt", 'r') as file:
                database[site] = file.read().splitlines()
                file.close()

        founds = {key: False for key in sites_list}

        #Per ogni link
        for url in urls:

            #Comprendi la piattaforma corrispondente
            for site in sites_list:
                if site in url:
                    try:
                        #Vedi se l'appartamento è per le camere, usa funzione camere. Altrimenti funzione appartamento
                        if "camer" in url or "stanze" in url: res = sites[site](url, "Camera")
                        else: res = sites[site](url, "Appartamento")
                    except Exception as e:
                        print(f"{e} when dealing with: {site}")

                    #Per ogni elemento nel risultato, se non si trova già nel database invialo, aggiungilo al database e raise flag
                    for el in res:
                        if el.link not in database[site]:
                            if Checks(el): SendMessage(el)
                            try:
                                database[site].append(el.link)
                            except Exception as e:
                                print(e)
                            founds[site] = True


        #Per ogni sito, se è stato trovato qualcosa dai l'alert e aggiorna il database
        for key in founds.keys():
            if founds[key]:
                print(f"Trovato per {key}")
                with open(f"Link Annunci/{key}.txt", 'w') as file:
                    for line in database[key]:
                        file.write(line+"\n")
                    file.close()

        #Se non hai trovato nulla, di' Tutto okay
        if not any(list(founds.values())): print("Tutto okay")
        if loading: return
        time.sleep(900)

if __name__=="__main__":
    main()
    bot.send_message(chat_id, "Loading completato.\nInizio ricerca...")
    loading = False
    main()