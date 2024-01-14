"""
Scraping von URLs von speisekarte.de

"""


import scrapy
from speisekarte.items import RestaurantItem


class MyprojectSpider(scrapy.Spider):
   name = "speisen"
   allowed_domains = ["speisekarte.de"]
   start_urls = [
      "https://www.speisekarte.de/staedteverzeichnis"
   ]
   
   #Buchstaben URLs: Bsp.: https://www.speisekarte.de/staedteverzeichnis/a ... z
   
   def parse(self, response):
       for link in response.css("div.container > nav > ul > li > a::attr('href')").getall():
           new_url = ("https://www.speisekarte.de" + link)
           yield response.follow(new_url, callback=self.parse_pages)
       
    #alle Seiten für Buchstaben URLs falls vorhanden: Bsp.: https://www.speisekarte.de/staedteverzeichnis/a?page=1 ... 10   
   def parse_pages(self, response):
       step_url = []
       try:
           max_page = int(response.css("nav.row.m-0 > ul > li > a.page-link::attr('href')")[-2].get().split("=")[-1]) #letzte Seitenanzahl als Int speichern
           for i in range (1, max_page+1):
               new_page = (response.request.url + "?page=" + str(i))
               step_url.append(new_page)      
       except:
           step_url.append(response.request.url)
        
       for steps in step_url:
          yield response.follow(steps, callback=self.parse_cities)
          
          #AUSKOMMENTIEREN FÜR TESTZWECKE (yield Zeile als Kommentar, wenn nur bis zur dieser Methode getestet werden soll, sonst wird alles an die nöchste Methode übergeben):
          #with open ("testing/scraping/step1.txt", "a") as f:
          #    f.write(f"{steps}\n")
    
    #alle Städte raussuchen      
   def parse_cities(self, response):
       for stadt in response.css("div.col3 > a::attr('href')").getall():
           stadt_url = ("https://www.speisekarte.de" + stadt)
           yield response.follow(stadt_url, callback=self.parse_rest_cat)
           
           #AUSKOMMENTIEREN FÜR TESTZWECKE (yield Zeile als Kommentar, wenn nur bis zur dieser Methode getestet werden soll, sonst wird alles an die nöchste Methode übergeben):
           #with open ("testing/scraping/step2.txt", "a") as f:
            #   f.write(f"{stadt_url}\n")

    #alle Kategorien raussuchen 
    # ACHTUNG: Seit Version 1.28-127 von speisekarte.de sind nur noch 5 Restaurantkategorien auf der Stadtübersicht zu finden
    #          Beim letzten Scraping am 18.05.2023 waren noch alle Kategorien sichtbar
    #          Stand 26.07.2023: Alle Restaurants werden jetzt direkt in der Stadtübersicht angezeigt: Bsp.: speisekarte/hamburg/restaurants?page=1 ... 299 statt nur die 100 besten
                  
   def parse_rest_cat(self, response):
       for categorie in response.css("a.d-block.sidebar-link.btn::attr('href')").getall():
           kategorie_url = ("https://www.speisekarte.de" + categorie)
           yield response.follow(kategorie_url, callback=self.parse_pages2)

           #AUSKOMMENTIEREN FÜR TESTZWECKE (yield Zeile als Kommentar, wenn nur bis zur dieser Methode getestet werden soll, sonst wird alles an die nöchste Methode übergeben):
           #with open ("testing/scraping/step3.txt", "a") as f:
           #    f.write(f"{kategorie_url}\n")
            
    #durch alle Seiten der Kategorien durchgehen
   def parse_pages2(self, response):
       step_url2 = []
       try:
           max_page2 = int(response.css("nav.row.m-0 > ul > li > a.page-link::attr('href')")[-2].get().split("=")[-1]) #letzte Seitenanzahl als Int speichern
           for i in range (1, max_page2+1):
               new_page2 = (response.request.url + "?page=" + str(i))
               step_url2.append(new_page2)      
       except:
           step_url2.append(response.request.url)
        
       for steps2 in step_url2:
           yield response.follow(steps2, callback=self.parse_menus)

           #AUSKOMMENTIEREN FÜR TESTZWECKE (yield Zeile als Kommentar, wenn nur bis zur dieser Methode getestet werden soll, sonst wird alles an die nöchste Methode übergeben):
           #with open ("testing/scraping/step4.txt", "a") as f:
            #   f.write(f"{steps2}\n")
    
      #Alle Urls der Speisekarten rausholen      
   def parse_menus(self, response):
       for menu in response.css("div.search-result-content > h3 > a::attr('href')").getall():
           menu_url = (menu + "/speisekarte")
           #yield response.follow(menu_url, callback=self.parse_speisekarten)

           #AUSKOMMENTIEREN FÜR TESTZWECKE (yield Zeile als Kommentar, wenn nur bis zur dieser Methode getestet werden soll, sonst wird alles an die nöchste Methode übergeben):
           with open ("testing/scraping/step5", "a") as f:
               f.write(f"{menu_url}\n")
           
         
     #Jede Speisekarte durchparsen, nochmal als separates Skript für weniger gleichzeitige Auslastung in spiders/only_url_parse
"""
   def parse(self, response):
       
       #Zugriff auf die RestaurantItem Items in der Datei items.py
       restaurant_item = RestaurantItem()
       
       #Initialisierung von leeren Listen für alle dish-items, sowie zusätzlichen Beschreibungen
       speisen_items = []
       speisen_zusatz_items = []
       beschreibung_sizes_list = []


       
       #Scraping von genereller Info je Restaurant: Name, Kategorie, Adresse, Webpage-Link und Datum der letzten Änderung der Speisekarte.
       #Mit verschiedenen Ausnahmen, falls die Webpage einen etwas anderen Aufbau hat als sonst

       
       
       #Scraping vom Restaurantnamen
       try:
        restaurant_item['restaurantname'] = response.css("div.container > div.display-1::text").get().strip()
       except:
        restaurant_item['restaurantname'] = response.css("div.container > p.display-1::text").get().strip()
       
       #Scraping von der Kategorie, wenn nicht an der gedachten Stelle, dann wird "None" gespeichert
       try:
        restaurant_item['kategorie'] = response.css("a.breadcrumb-item::text")[-2].get().strip()
       except:
        restaurant_item['kategorie'] = None

       #Scraping von der Adresse
       #Im ersten Fall wird die Straße und Hausnummer, sowie die Stadt und Postleitzahl in einem Item gespeichert
       #Im zweiten Fall wird die Stadt, Postleitzahl und Straße mit Hausnummer in einzelnen Items gespeichert
       try:
            restaurant_item['adresse_str_h'] = response.css("address::text").get().strip()
            restaurant_item['adresse_stadt_p'] = response.xpath('//*[@id="one-pager-address"]/text()[2]').extract_first().strip()
       except:
            restaurant_item['adresse_stadt'] = response.css("p > span::text")[2].getall()
            restaurant_item['adresse_plz'] = response.css("p > span::text")[1].getall()
            restaurant_item['adresse_straße'] = response.css("p > span::text")[0].getall()
       
       #Aktuelle URl abspeichern
       restaurant_item['url'] = response.url


       #Scraping von den Datum, wenn nicht an der gedachten Stelle, dann bleibt es leer
       try:
         string = response.css("p.last-modified.onepager-text-max-width::text").get().strip() 
         words = string.split()
         restaurant_item['datum'] = words[-12]

       except:
          restaurant_item['datum'] = None 

       #Scraping von Speisennamen, Speisenbeschreibung, Speisenpreis
          
       for speisen in response.css("div.menu-entry-filter"):
           speisen_item = DishItem()
           size_item = SizesItem()
           
           #Zusammensetzung des Speisennamen aus unetrschiedlichen HTML-Containern, falls der Speisenname lang ist

           if speisen.css("div.grid-dishes > div.col-9.hyphens > b.dish.hyphens.d-block > a"):
                 name_anfang = speisen.css("div.grid-dishes > div.col-9 > b.dish.hyphens.d-block::text").get().strip()
                 name_mitte = speisen.css("div.grid-dishes > div.col-9.hyphens > b.dish.hyphens.d-block > a::text").get() 
                 name_ende = speisen.css("div.grid-dishes > div.col-9.hyphens > b::text")[+1].get().strip()
        
                 speisen_item['speisenname'] = name_anfang + " " + name_mitte + " " + name_ende

            #Scraping des Speisennamen, falls Speisenname kurz ist 

           else:
              speisen_item['speisenname'] = speisen.css("div.grid-dishes > div.col-9 > b.dish.hyphens.d-block::text").get().strip()

            #Scraping des Speisenpreises mit zwei möglichen Containern
        
           try:
              speisen_item['preis'] = speisen.css("div.grid-dishes > span::attr('content')")[0].getall()
           except:
              speisen_item['preis'] = speisen.css("div.grid-dishes > div.price > div > span::attr('content')").get()
      
           #Zusammensetzung der Speisenbeschreibung aus unterschiedlichen HTML-Containern, falls die Speisenbeschreibung lang ist

           if speisen.css("div.col-9.hyphens > a"):
                 beschreibung_anfang = speisen.css("div.grid-dishes > div.col-9.hyphens::text")[1].get().strip()
                 beschreibung_mitte = speisen.css("div.grid-dishes > div.col-9.hyphens > a::text").get() 
                 beschreibung_ende = speisen.css("div.grid-dishes > div.col-9.hyphens::text")[-1].get().strip()
                 speisen_item['beschreibung'] = beschreibung_anfang + " " + beschreibung_mitte + " " + beschreibung_ende 

         #Zusammensetzung der Speisenbeschreibung falls ein "break" ind er Speisenbeschreibung vorhanden ist

           else:
              beschreibung_bfbreak = speisen.css("div.grid-dishes > div.col-9.hyphens::text")[1].get().strip()
              if speisen.css("div.grid-dishes > div.col-9.hyphens::text")[-1].get():
                 beschreibung_afbreak = speisen.css("div.grid-dishes > div.col-9.hyphens::text")[-1].get().strip()
              else:
                 None
              speisen_item['beschreibung'] = beschreibung_bfbreak + " " + beschreibung_afbreak



              
           for menufilter in response.css("div.menu-entry-filter"):

            #Scraping der Zusatzbsechreibung, falls Speise unterschiedliche Speisengrößen anbietet
            
            if speisen.css("div > div.grid-dishes.sizes"):
               menu_list_beschr = speisen.css("div > div.grid-dishes.sizes > div.dish.dish-sizes::text").getall()
               menu_list_beschr = [[item.replace('\n', '').replace('\t', '').strip() for item in sublist if item.strip()] for sublist in [menu_list_beschr]]
               menu_list_pr = speisen.css("div > div.grid-dishes.sizes > div.price > span[itemprop = price]::attr('content')").getall()
               menu_list_pr = [[item.replace('\n', '').replace('\t', '').strip() for item in sublist if item.strip()] for sublist in [menu_list_pr]]
               
               
               for elem in menu_list_beschr:
                  if len(menu_list_beschr) != 0:
                     size_item['beschreibung_zusatz_sizes'] = elem
                     menu_list_beschr.pop(0)
                  else:
                     None

               for elems in menu_list_pr:
                  if len(menu_list_pr) != 0:
                     size_item['preis_zusatz_sizes'] = elems
                     menu_list_pr.pop(0)
                  else:
                     None


                  if size_item not in beschreibung_sizes_list:
                     beschreibung_sizes_list.append(size_item)


                  if len(beschreibung_sizes_list) != 0:
                     speisen_item['beschreibung_sizes'] = beschreibung_sizes_list[0]
                     beschreibung_sizes_list.pop(0)
                  else:
                     None                     

            else:
               None           
       
         #Scraping der Zusatzbsechreibung, falls Speise noch eine audführliche Speisenbeschreibung anbietet
               
           for menufilter in response.css("div.menu-entry-filter"):
              
              if speisen.css("div.col-12 > div.mt-2.mb-2 > div.mb-2 > div.entry-course.hyphens"):
                 menufilter_list = speisen.css("div.col-12 > div.mt-2.mb-2 > div.mb-2 > div.entry-course.hyphens::text").getall()
                 menufilter_list = [[item.replace('\n', '').replace('\t', '').strip() for item in sublist if item.strip()] for sublist in [menufilter_list]]
                 
                 for menufilter in menufilter_list:
                    if menufilter not in speisen_zusatz_items:
                       speisen_zusatz_items.append(menufilter)

                 if len(speisen_zusatz_items) != 0:
                    speisen_item['speisen_zusatz'] = speisen_zusatz_items[0]
                    speisen_zusatz_items.pop(0)
                 else:
                    None
              else:
                 None


           if speisen_item not in speisen_items:
              speisen_items.append(speisen_item)

      #Speichern aller aller Speisennamen, Speisenbeschreibungen, Speisenpreise in Item "speisen"
              
       restaurant_item['speisen'] = speisen_items

      #Output im JSON-Format der Restaurant-Items
       
       yield restaurant_item

       
        
Im Terminal laufen lassen:

für Testzwecke der CSS Anfragen, Webpage angeben in '': python -m scrapy shell '' 
Code Starten: python -m scrapy crawl speisen


"""                 

    
       