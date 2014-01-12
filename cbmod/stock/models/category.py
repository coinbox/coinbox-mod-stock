import cbpos

import cbpos.mod.base.models.common as common
from cbpos.mod.base.models import StoredFile

from sqlalchemy import func, Table, Column, Integer, String, Float, Boolean, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method, Comparator

class Category(cbpos.database.Base, common.Item):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))

    image_id = Column(Integer, ForeignKey('storedfiles.id'))

    parent = relationship("Category", backref="children", remote_side=[id])
    _image = relationship("StoredFile")

    @hybrid_property
    def display(self):
        return self.name
    
    @display.expression
    def display(self):
        return self.name

    def __repr__(self):
        return "<Category %s>" % (self.name,)

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