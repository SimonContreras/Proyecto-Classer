from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from bs4 import BeautifulSoup
from twisted.internet import reactor
import scrapy
from ScrapyProject.items import ScrapedDataItem, ScrapedImageItem

#funcion que permite arreglar los links de imagenes obtenidos, debido a que algunas son rutas relativas y deben ser convertidos a rutas web
def ajuste_img_src(Lista, response):
            for i in range(len(Lista)):
                if not Lista[i][0].startswith('h'):
                    Lista[i][0] = response.url.partition("com")[0] + response.url.partition("com")[1] + Lista[i][0]
                    
                    
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://www.fisicalab.com/apartado/campo-magnetico-creado-corriente-electrica#contenidos'
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
                    Lista_imagenes_final.append([item,"imagen",k,titulo,url])
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
        ajuste_img_src(Lista_imagenes_final,response)
        
        #A partir de aca se pueden utilizar o guardar los parrafos y imagenes, que estan en la Listas: Lista_imagenes_final y  Lista_informaciones_final
        #cada elemento de la lista contiene: [texto o url de imagen, tipo de dato, orden, titulo(tema), url de la pagina]
        
        for info in Lista_informaciones_final:
            print("-----Parrafo----\n")
            print("orden: "+ str(info[2]) +"\n")
            print("tema: "+ info[3] +"\n")
            print("url: "+ info[4] +"\n")
            print("texto: \n"+ info[0] +"\n")
            print("--------------\n")
            ScrapedDataItem(order=info[2], topic=info[3], url=info[4], information=info[0]).save()

        for imagen in Lista_imagenes_final:
            ScrapedImageItem(order=imagen[2], topic=imagen[3], url=imagen[4], information=imagen[0]).save()


        
        #Busqueda automatica de nuevas paginas, se basa en encontrar todos los links(<a>) de cada nueva pagina, 
        #luego comprobar que el texto que muestran se encuentre en la lista de temas.
        #Por ahora no cambiemos la Lista_temas
        
        Lista_temas = ["Ley de Lorentz","Ley de Lorentz","Ley de Ampère"]
        urls = response.xpath("//a")
        for item in urls:
            if item.xpath("string()").extract()[0] in Lista_temas:
                yield scrapy.Request(response.urljoin(item.xpath("@href").extract()[0]), callback=self.parse)
           
                
            
        
       
        
     
        

            
            
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()
d = runner.crawl(QuotesSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished