from tornado.web import URLSpec as U

from icecat.views import HomeHandler, UpdateHandler, ProductHandler

HANDLERS = [
    U(r'/', HomeHandler, name='home'),
    U(r'/update/', UpdateHandler, name='update'),
    U(r'/product/(?P<product_id>[0-9]*)/',ProductHandler, name='product')
]