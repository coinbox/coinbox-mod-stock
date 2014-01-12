from PySide import QtGui

import cbpos
logger = cbpos.get_logger(__name__)

from cbmod.stock.controllers import CategoriesFormController
from cbmod.stock.models import Category, Product

from cbmod.base.views import FormPage
from cbmod.base.views.widgets import ImagePicker

class CategoriesPage(FormPage):
    controller = CategoriesFormController()
    
    def widgets(self):
        return (("name", QtGui.QLineEdit()),
                ("parent", QtGui.QComboBox()),
                ("image", ImagePicker())
                )
    
    def getDataFromControl(self, field):
        if field == 'name':
            data = self.f[field].text()
        elif field == 'parent':
            selected_index = self.f[field].currentIndex()
            if selected_index == -1:
                data = None
            else:
                data = self.f[field].itemData(selected_index)
        elif field == 'image':
            image = self.f[field].image()
            path = self.f[field].image_path()
            if image:
                data = image
            elif path:
                data = path
            else:
                data = None
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field == 'name':
            self.f[field].setText(data)
        elif field == 'parent':
            session = cbpos.database.session()
            query = session.query(Category)
            
            self.f[field].clear()
            self.f[field].addItem("", None)
            
            if self.item is None:
                for i, item in enumerate(query):
                    self.f[field].addItem(item.display, item)
            else:
                # Remove the category itself from the list of parents
                query = query.filter(Category.id != self.item.id)
                
                selected_index = 0
                for i, item in enumerate(query):
                    self.f[field].addItem(item.display, item)
                    
                    if item.id == self.item.parent_id:
                        selected_index = i+1 # Don't forget the first "" item
                
                self.f[field].setCurrentIndex(selected_index)
        elif field == 'image':
            self.f[field].setImage(data)
