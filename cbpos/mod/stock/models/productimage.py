import os
from cStringIO import StringIO

import logging
logger = logging.getLogger(__name__)

import cbpos

import cbpos.mod.base.models.common as common

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, LargeBinary, Enum, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

class ProductImage(cbpos.database.Base, common.Item):
    __tablename__ = 'productimages'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), default='')
    filetype = Column(Enum('png', 'jpg'))
    content = deferred(Column("content", LargeBinary))

    def __init__(self, filename):
        basename = os.path.basename(filename)
        dummy, ext = os.path.splitext(basename)
        filetype = ext[1:]
        with open(filename, 'r') as f:
            content = f.read()
        
        super(ProductImage, self).__init__(filetype=filetype, content=content, filename=basename)

    @hybrid_property
    def display(self):
        return self.filename
    
    @display.expression
    def display(self):
        return self.filename

    @hybrid_property
    def path(self):
        cache = self.cached()
        if not os.path.isfile(cache):
            with open(cache, 'w') as f:
                f.write(self.content)
        return cache

    def cached(self):
        return cbpos.res.stock('cache/{}.{}'.format(self.id, self.filetype))

    def __repr__(self):
        return "<ProductImage %s>" % (self.filename,)
