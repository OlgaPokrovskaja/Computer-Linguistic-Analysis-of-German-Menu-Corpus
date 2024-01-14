# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


"""

Definition der Scrapy Items und Aufbau des resultierenden Korpus

"""
import scrapy

class RestaurantItem(scrapy.Item):
    restaurantname = scrapy.Field()
    kategorie = scrapy.Field()
    adresse_str_h = scrapy.Field()
    adresse_stadt_p = scrapy.Field()
    url = scrapy.Field()
    datum = scrapy.Field() 
    adresse_stadt = scrapy.Field()
    adresse_plz = scrapy.Field()
    adresse_straße = scrapy.Field()
    speisen = scrapy.Field()
    


class DishItem(scrapy.Item):
    speisenname = scrapy.Field()
    preis = scrapy.Field()
    beschreibung = scrapy.Field()
    beschreibung_zusatz = scrapy.Field()
    speisen_zusatz = scrapy.Field()
    beschreibung_sizes = scrapy.Field()

class SizesItem(scrapy.Item):
    beschreibung_zusatz_sizes = scrapy.Field()
    preis_zusatz_sizes = scrapy.Field()
    

