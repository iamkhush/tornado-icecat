import tornado.web
from tornado import template
from mongoengine import Q
from xml.dom.minidom import parse, parseString

from icecat.models import ProductInfo
import requests


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('home.html', products=None)

    def post(self):
        to_search = self.get_argument('search', None)
        if not to_search:
            self.redirect('/')

        if to_search.isdigit():
            products = ProductInfo.objects(product_id=to_search)
        else:
            products = ProductInfo.objects(supplier__icontains=to_search)
        count = len(products)
        if count:
            self.render('home.html',
                    products=products,
                       search=to_search,
                        count=count)
        else:
            self.render('update.html', search=to_search, error='')


class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('update.html', search=None, error='')

    def post(self):
        to_update = self.get_argument('update', None)
        if to_update and not to_update.isdigit():
            self.render('update.html', error=\
                'Product Id should be a number', search=None)

        r = requests.get('http://data.icecat.biz/export/freexml.int/EN/%s.xml'
                         % (to_update),
                auth=('iamkhush', 'ankushicecat29'))
        if r.status_code != 200:
            self.render('update.html',
                        error='Product Id is invalid',search=None)

        #xml parsing to be done here
        dom1 = parseString(r.content)
        #get product details
        products = dom1.getElementsByTagName('Product')
        product_id = products[0].getAttributeNode('ID').nodeValue
        name = products[0].getAttributeNode('Title').nodeValue
        thumbnail = products[0].getAttributeNode('ThumbPic').nodeValue
        picture = products[0].getAttributeNode('LowPic').nodeValue
        product_description = dom1.getElementsByTagName('ProductDescription')
        description = product_description[0].getAttributeNode('LongDesc').nodeValue
        suppliers = dom1.getElementsByTagName('Supplier')
        supplier = suppliers[0].getAttributeNode('Name').nodeValue
        print product_id,name,thumbnail,picture,description,supplier
        #save in db
        product = ProductInfo(product_id=int(product_id),
                              name=name,
                              thumbnail=thumbnail,
                              picture=picture,
                              description=description,
                              supplier=supplier)
        product.save(validate=False)
        self.redirect('/product/%s/' % (product_id))


class ProductHandler(tornado.web.RequestHandler):
    def get(self, product_id):
        products = ProductInfo.objects(product_id=product_id)
        if products:    
            self.render('productdisplay.html', product=products[0])
        raise tornado.web.HTTPError(404)