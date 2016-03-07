import scrapy
import re

from scrapy.contrib.loader import ItemLoader
from americanas_crawl.items import Product

class AmericanasSpider(scrapy.Spider):
    name = 'americanas_spider'
    #allowed_domains = ["americanas.com.br"]
    #start_urls = ['http://www.americanas.com.br/linha/314388/alimentos-e-bebidas/chocolates-importados']
    start_urls = [
'http://www.americanas.com.br/linha/314388/alimentos-e-bebidas/chocolates-importados'
'http://www.americanas.com.br/linha/315788/alimentos-e-bebidas/bebidas-alcoolicas',
'http://www.americanas.com.br/linha/314083/alimentos-e-bebidas/espumantes-champagne',
'http://www.americanas.com.br/linha/314370/alimentos-e-bebidas/vinhos',
'http://www.americanas.com.br/linha/314045/alimentos-e-bebidas/bomboniere',
'http://www.americanas.com.br/linha/342150/alimentos-e-bebidas/panetones-e-colombas',
'http://www.americanas.com.br/linha/314061/alimentos-e-bebidas/biscoitos',
'http://www.americanas.com.br/linha/285368/utilidades-domesticas/vinho',
'http://www.americanas.com.br/linha/316829/eletrodomesticos/adega-de-vinho',
# 'http://www.americanas.com.br/linha/262488/audio/ipod-e-acessorios',
# 'http://www.americanas.com.br/linha/263029/tv-e-home-theater/home-theater',
#'http://www.americanas.com.br/linha/262437/audio/equipamentos-para-dj',
# 'http://www.americanas.com.br/linha/267011/automotivo/som-automotivo?WT.mc_id=menuLateral-somAutomotivo/',
 'http://www.americanas.com.br/linha/267033/automotivo/dvd-automotivo',
# 'http://www.americanas.com.br/linha/368134/automotivo/central-multimidia',
# 'http://www.americanas.com.br/linha/291248/beleza-e-saude/barbeadores',
# 'http://www.americanas.com.br/linha/291288/beleza-e-saude/depiladores',
# 'http://www.americanas.com.br/linha/291589/beleza-e-saude/chapinhas-pranchas-',
# 'http://www.americanas.com.br/linha/291542/beleza-e-saude/escovas-pentes-e-tesouras',
# 'http://www.americanas.com.br/linha/291668/beleza-e-saude/maquina-de-cortar-cabelo',
# 'http://www.americanas.com.br/linha/279669/brinquedos/barbie',
# 'http://www.americanas.com.br/linha/279688/brinquedos/bonecas',
# 'http://www.americanas.com.br/linha/279649/brinquedos/bonecos',
# 'http://www.americanas.com.br/linha/279691/brinquedos/esportes'
# 'http://www.americanas.com.br/linha/279788/brinquedos/hot-wheels',
# 'http://www.americanas.com.br/loja/226762/games',
'http://www.americanas.com.br/linha/347990/games/console-xbox-one',
'http://www.americanas.com.br/linha/351258/games/jogos-xbox-one',
#'http://www.americanas.com.br/linha/355352/games/acessorios-xbox-one',
'http://www.americanas.com.br/linha/291045/games/console-xbox-360',
'http://www.americanas.com.br/linha/291228/games/jogos-xbox-360',
#'http://www.americanas.com.br/linha/291066/games/jogos-kinect',
#'http://www.americanas.com.br/linha/291231/games/acessorios-xbox-360',
'http://www.americanas.com.br/linha/351535/games/console-playstation-4',
'http://www.americanas.com.br/linha/356437/games/jogos-playstation-4',
#'http://www.americanas.com.br/linha/356438/games/acessorios-playstation-4',
'http://www.americanas.com.br/linha/291327/games/jogos-pc',
'http://www.americanas.com.br/linha/291380/games/console-ps-vita',
'http://www.americanas.com.br/linha/291473/games/jogos-ps-vita',
#'http://www.americanas.com.br/linha/355372/games/console-nintendo-wiiu',
#'http://www.americanas.com.br/linha/350932/games/jogos-nintendo-wiiu',
'http://www.americanas.com.br/linha/291314/games/console-nintendo-wii',
'http://www.americanas.com.br/linha/291282/games/jogos-nintendo-wii',
'http://www.americanas.com.br/linha/291317/games/console-nintendo-3ds',
'http://www.americanas.com.br/linha/291431/games/jogos-nintendo-3ds',
#'http://www.americanas.com.br/linha/291432/games/console-nintendo-dsi',
#'http://www.americanas.com.br/linha/291449/games/jogos-nintendo-dsi-ds'
'http://www.americanas.com.br/linha/345399/celulares-e-telefones/iphone',
#'http://www.americanas.com.br/linha/350392/celulares-e-telefones/smartphone',
'http://www.americanas.com.br/linha/350392/celulares-e-telefones/smartphone/marcas-nokia',
'http://www.americanas.com.br/linha/350392/celulares-e-telefones/smartphone/marcas-motorola',
'http://www.americanas.com.br/linha/350392/celulares-e-telefones/smartphone/marcas-lg',
#'http://www.americanas.com.br/sublinha/350373/celulares-e-telefones/smartphone/smartphone-multichips',
'http://www.americanas.com.br/linha/350392/celulares-e-telefones/smartphone/marcas-samsung',
# 'http://www.americanas.com.br/linha/316691/eletrodomesticos/secadora-de-roupa-e-centrifuga',
# 'http://www.americanas.com.br/linha/316808/eletrodomesticos/lavadora-de-roupa-e-tanquinho',
# 'http://www.americanas.com.br/linha/316828/eletrodomesticos/micro-ondas',
# 'http://www.americanas.com.br/linha/316690/eletrodomesticos/lava-loucas',
# 'http://www.americanas.com.br/linha/316788/eletrodomesticos/geladeira-refrigerador',
# 'http://www.americanas.com.br/linha/316868/eletrodomesticos/freezer',
# 'http://www.americanas.com.br/linha/316830/eletrodomesticos/forno',
# 'http://www.americanas.com.br/linha/316689/eletrodomesticos/fogao',
# 'http://www.americanas.com.br/linha/316848/eletrodomesticos/cooktop',
'http://www.americanas.com.br/linha/315442/dvds-e-blu-ray/boxes-e-colecoes',
'http://www.americanas.com.br/linha/315255/dvds-e-blu-ray/series-de-tv',
#'http://www.americanas.com.br/linha/315209/dvds-e-blu-ray/lancamentos',
# 'http://www.americanas.com.br/linha/278252/eletroportateis/grill-sanduicheira-e-torradeira',
# 'http://www.americanas.com.br/linha/278197/eletroportateis/liquidificadores',
# 'http://www.americanas.com.br/loja/227763/eletroportateis?WT.mc_id=mapasite_eletroportateis',
 'http://www.americanas.com.br/linha/278193/eletroportateis/chocolateria-e-fondue',
'http://www.americanas.com.br/linha/278151/eletroportateis/churrasqueiras-e-utensilios',
# 'http://www.americanas.com.br/linha/278268/eletroportateis/bebedouros-e-purificadores',
'http://www.americanas.com.br/linha/278191/eletroportateis/cafeteiras-e-chaleiras',
'http://www.americanas.com.br/linha/290624/esporte-e-lazer/tenis-squash-e-badmiton',
# 'http://www.americanas.com.br/linha/290748/esporte-e-lazer/volei',
# 'http://www.americanas.com.br/linha/324410/esporte-e-lazer/running',
#'http://www.americanas.com.br/linha/290619/esporte-e-lazer/pesca',
'http://www.americanas.com.br/linha/290564/esporte-e-lazer/skate-e-skate-eletrico',
#'http://www.americanas.com.br/linha/290562/esporte-e-lazer/patinete',
'http://www.americanas.com.br/linha/290538/esporte-e-lazer/patins',
# 'http://www.americanas.com.br/linha/290828/esporte-e-lazer/natacao-hidroginastica',
#'http://www.americanas.com.br/linha/290616/esporte-e-lazer/mergulho',
'http://www.americanas.com.br/linha/290628/esporte-e-lazer/lutas-e-artes-marciais',
#'http://www.americanas.com.br/linha/290614/esporte-e-lazer/kart',
#'http://www.americanas.com.br/linha/290535/esporte-e-lazer/golfe',
'http://www.americanas.com.br/linha/290608/esporte-e-lazer/futebol',
'http://www.americanas.com.br/linha/290285/esporte-e-lazer/basquete',
#'http://www.americanas.com.br/linha/291611/esporte-e-lazer/camping',
'http://www.americanas.com.br/linha/290286/esporte-e-lazer/bicicleta',
'http://www.americanas.com.br/linha/267868/informatica/notebook',
'http://www.americanas.com.br/linha/348528/informatica/ultrabook',
'http://www.americanas.com.br/linha/267968/informatica/apple',
'http://www.americanas.com.br/linha/267908/informatica/tablets-e-ipad',
#'http://www.americanas.com.br/linha/326224/instrumentos-musicais/instrumentos-de-corda',
#'http://www.americanas.com.br/linha/326139/instrumentos-musicais/instrumentos-de-sopro',
'http://www.americanas.com.br/linha/326278/instrumentos-musicais/bateria',
#'http://www.americanas.com.br/linha/326118/instrumentos-musicais/percussao',
'http://www.americanas.com.br/linha/228507/livros/historia-em-quadrinhos',
'http://www.americanas.com.br/linha/230995/livros/mais-vendidos',
'http://www.americanas.com.br/linha/262909/tv-e-home-theater/tv',
'http://www.americanas.com.br/linha/289581/relogios/relogios',
'http://www.americanas.com.br/linha/285259/utilidades-domesticas/chopeira'
]

    def parse(self, response):
        for a in response.css('div.paginado article .top-area-product > a').extract():
            url = re.search(r'href=[\"|\'](?P<href>[^\"\']+)[\"|\']', a).groupdict()['href']
            yield scrapy.Request(url, callback=self.parse_product)

        #url = response.css('a.next::attr(href)').extract()
        #if url:
        #    yield scrapy.Request(url[0], callback=self.parse)

    def parse_product(self, response):
        p = ItemLoader(item=Product(), response=response)
        p.add_css('nome', 'h1 > span[itemprop=name]::text')
        p.add_value('url', response.url)
        p.add_css('descricaoLongaHtml','.infoProdBox')
        p.add_css('descricaoLonga','.infoProdBox')
        #p.add_css('detalhes','.ficha-tecnica table tr th::text, .ficha-tecnica table tr td::text')
        p.add_css('image','ul.a-carousel-list > li > img', re='src=[\"|\'](?P<src>[^\"\']+)[\"|\']')
        p.add_css('categorias','div[class=breadcrumb-box] span[itemprop=name]::text')
        yield p.load_item()
