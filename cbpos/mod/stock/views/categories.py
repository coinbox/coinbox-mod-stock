from PySide import QtGui

import cbpos

from cbpos.mod.stock.controllers import CategoriesFormController
from cbpos.mod.stock.models import Category, Product

from cbpos.mod.base.views import FormPage

class CategoriesPage(FormPage):
    controller = CategoriesFormController()
    
    def widgets(self):
        return (("name", QtGui.QLineEdit()),
                ("parent", QtGui.QComboBox())
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
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field == 'name':
            self.f[field].setText(data)
        elif field == 'parent':
            session = cbpos.database.session()
            query = session.query(Category)
            if data is not None:
                query = query.filter(Category.id != data.id)
            self.f[field].clear()
            self.f[field].addItem("", None)
            for item in query:
                self.f[field].addItem(item.display, item)
