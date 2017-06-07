from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from bs4 import BeautifulSoup
from ScrapyProject.items import ScrapedDataItem, ScrapedImageItem
import urllib
from PIL import ImageFile
import sys
sys.path.append('C:/Users/SimónContreras/Desktop/E3/Workbench/TextClassifier')
from classifier import classify
from entities import get_urls, get_entities, limpieza, juntar


def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = urllib.request.urlopen(uri)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return p.image.size
            break
    file.close()
    return  None   


#funcion que permite arreglar los links de imagenes obtenidos, debido a que algunas son rutas relativas y deben ser convertidos a rutas web
def ajuste_img_src(link, response):
                if not link.startswith('h'):
                    return response.url.partition("com")[0] + response.url.partition("com")[1] + link
                else:
                    return link
                    
                    
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.fisicalab.com/apartado/ley-de-ampere'
    ]

    def parse(self, response):
        
        #Se guardan todos los links de imagenes
        Imagenes = response.xpath('//img[not(ancestor::footer) and not(ancestor::header)]/@src').extract()
        
        #se guarda la url de la pagina actual
        url = response.url
        
        #Lista de parrafos, imagenes y listas de texto
        Lista_completa = response.xpath('//p[not(ancestor::footer) and not(ancestor::*[contains(@class,"nav")]) ]  | //img[not(ancestor::footer) and not(ancestor::header)]/@src | //ul[not(ancestor::footer) and not(@class)]').extract()
        
        
        #Se guarda el titulo de la pagina
        titulo = response.xpath('string(//title)').extract()[0]

        
        
        Lista_imagenes_final = []
        Lista_informaciones_final = []
        
        
        #
        k = 1
        l = 0
        leer = 1
        for item in Lista_completa:
            if leer == 1:
                if item in Imagenes:
                    link = ajuste_img_src(item,response)
                    width , height = getsizes(link)
                    Lista_imagenes_final.append([link,"imagen",k,titulo,url,width,height])
                    k = k + 1 
                else:
                    soup = BeautifulSoup(item, 'html.parser')
                    texto = soup.get_text()
                    if not(texto == ""):
                        if texto.endswith(":"):
                            soup2 = BeautifulSoup(Lista_completa[l + 1], 'html.parser')
                            if soup2.get_text() == "":
                                Lista_informaciones_final.append([texto,"informacion",k,titulo,url])
                            else:
                                Lista_informaciones_final.append([texto + "\n" + soup2.get_text(),"informacion",k,titulo,url])
                            leer = 0
                        else:
                            Lista_informaciones_final.append([texto,"informacion",k,titulo,url])
                        k = k + 1
            else:
                leer = 1
            l = l + 1
       
        
        #A partir de aca se pueden utilizar o guardar los parrafos y imagenes, que estan en la Listas: Lista_imagenes_final y  Lista_informaciones_final
        #cada elemento de la lista de parrafos contiene: [texto, tipo de dato, orden, titulo(tema), url de la pagina] 
        #cada elemento de la lista de imagenes contiene: [url de imagen, tipo de dato, orden, titulo(tema), url de la pagina, ancho,alto] 

        for img in Lista_imagenes_final:
            ScrapedImageItem(order=img[2], topic=img[3], url=img[4], information=img[0], width=img[5], height=img[6]).save()

        for info in Lista_informaciones_final:
            classified = classify('C:/Users/SimónContreras/Desktop/E3/Workbench/TextClassifier/classifier_bayes.pickle',
                                  info[0])
            entities, meta = get_entities(info[0])
            tag = juntar(limpieza(entities))
            urls = get_urls(meta)
            ScrapedDataItem(order=info[2],
                            topic=info[3],
                            url=info[4],
                            information=info[0],
                            classification=classified,
                            tags=tag,
                            metadata=urls).save()

        #Busqueda automatica de nuevas paginas, se basa en encontrar todos los links(<a>) de cada nueva pagina, 
        #luego comprobar que el texto que muestran se encuentre en la lista de temas.
        #Por ahora no cambiemos la Lista_temas
        
        Lista_temas = ["Ley de Lorentz","Ley de Biot-Savart"]
        urls = response.xpath("//a")
        for item in urls:
            if item.xpath("string()").extract()[0] in Lista_temas:
                yield scrapy.Request(response.urljoin(item.xpath("@href").extract()[0]), callback=self.parse)
           

runner = CrawlerRunner()
d = runner.crawl(QuotesSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished