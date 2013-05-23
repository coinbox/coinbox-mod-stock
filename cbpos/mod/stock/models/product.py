import cbpos

import cbpos.mod.base.models.common as common
from cbpos.mod.stock.models import ProductImage, DiaryEntry

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

from cbpos.mod.currency.models import CurrencyValue

class Product(cbpos.database.Base, common.Item):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False, default='')
    reference = Column(String(255), nullable=True, unique=True)
    code = Column(String(255), nullable=True, unique=True)
    
    price = Column(CurrencyValue(), nullable=False, default=0)
    _quantity = Column('quantity', Integer, nullable=True, default=None)
    
    currency_id = Column(String(3), ForeignKey('currencies.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    image_id = Column(Integer, ForeignKey('productimages.id'))
    
    category = relationship("Category", backref="products")
    currency = relationship("Currency", backref="products")
    image = relationship("ProductImage", backref="products")

    def __init__(self, *args, **kwargs):
        q = None
        if 'quantity' in kwargs:
            q = kwargs['quantity']
            del kwargs['quantity']
        if 'in_stock' in kwargs:
            if not kwargs['in_stock']:
                q = None
            del kwargs['in_stock']
        kwargs['_quantity'] = q
        super(Product, self).__init__(*args, **kwargs)

    @hybrid_property
    def display(self):
        return self.name
    
    @display.expression
    def display(self):
        return self.name

    def __repr__(self):
        return "<Product %s>" % (self.name,)

    @hybrid_property
    def in_stock(self):
        return self._quantity is not None

    @in_stock.setter
    def in_stock(self, value):
        if not value:
            self._quantity = None
        elif value and self._quantity is None:
            self._quantity = 0

    @in_stock.expression
    def in_stock(cls):
        return cls.quantity != None

    @hybrid_property
    def quantity(self):
        return self._quantity

    @quantity.expression
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        d = DiaryEntry()
        d.update(operation='edit', quantity=value, product=self)

    def quantity_in(self, value):
        if self._quantity is None:
            return
        self._quantity += value
        d = DiaryEntry()
        d.update(operation='in', quantity=value, product=self)

    def quantity_out(self, value):
        if self._quantity is None:
            return
        self._quantity -= value
        d = DiaryEntry()
        d.update(operation='out', quantity=value, product=self)
