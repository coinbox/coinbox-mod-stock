import cbpos

import cbpos.mod.base.models.common as common
from cbpos.mod.stock.models import DiaryEntry
from cbpos.mod.base.models import StoredFile

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
    
    image_id = Column(Integer, ForeignKey('storedfiles.id'))
    
    category = relationship("Category", backref="products")
    currency = relationship("Currency", backref="products")
    _image = relationship("StoredFile")

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
        d = DiaryEntry(operation='edit', quantity=value)
        self.diaryentries.append(d)

    def quantity_in(self, value):
        if self._quantity is None:
            return
        self._quantity += value
        d = DiaryEntry(operation='in', quantity=value)
        self.diaryentries.append(d)

    def quantity_out(self, value):
        if self._quantity is None:
            return
        self._quantity -= value
        d = DiaryEntry(operation='out', quantity=value)
        self.diaryentries.append(d)

    @hybrid_property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, value):
        if isinstance(value, basestring):
            # If value is a path
            size = cbpos.config["stock", "default_image_size"]
            format = cbpos.config["stock", "default_image_format"]
            self._image = StoredFile.image(value , size, format)
        else:
            # value is a StoredFile
            self._image = value
    
    @image.deleter
    def image(self):
        self._image = None
