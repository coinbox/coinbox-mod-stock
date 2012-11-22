from PySide import QtGui

import cbpos

from cbpos.mod.stock.controllers import ProductsFormController
from cbpos.mod.currency.models.currency import Currency
from cbpos.mod.stock.models import Product, Category

from cbpos.mod.base.views import FormPage

class ProductsPage(FormPage):
    controller = ProductsFormController()
    
    def widgets(self):
        price = QtGui.QDoubleSpinBox()
        price.setMinimum(0)

        in_stock = QtGui.QCheckBox()
        in_stock.stateChanged.connect(self.onInStockCheckBox)
        
        quantity = QtGui.QDoubleSpinBox()
        quantity.setMinimum(0)

        return (("name", QtGui.QLineEdit()),
                ("description", QtGui.QTextEdit()),
                ("reference", QtGui.QLineEdit()),
                ("code", QtGui.QLineEdit()),
                ("price", price),
                ("currency", QtGui.QComboBox()),
                ("in_stock", in_stock),
                ("quantity", quantity),
                ("category", QtGui.QComboBox())
                )
    
    def onInStockCheckBox(self, event):
        in_stock = self.f["in_stock"].isChecked()
        self.f["quantity"].setEnabled(in_stock)
    
    def getDataFromControl(self, field):
        if field in ('name', 'reference', 'code'):
            data = self.f[field].text()
        elif field == 'description':
            data = self.f[field].toPlainText()
        elif field in ('price', 'quantity'):
            data = self.f[field].value()
        elif field == 'in_stock':
            data = self.f[field].isChecked()
        elif field in ('currency', 'category'):
            selected_index = self.f[field].currentIndex()
            if selected_index == -1:
                data = None
            else:
                data = self.f[field].itemData(selected_index)
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field in ('name', 'description', 'reference', 'code'):
            self.f[field].setText(data)
        elif field == 'in_stock':
            self.f[field].setChecked(data)
        elif field == 'currency':
            session = cbpos.database.session()
            items = session.query(Currency.display, Currency).all()
            self.f[field].clear()
            for i, item in enumerate(items):
                self.f[field].addItem(*item)
                if item[1] == data:
                    self.f[field].setCurrentIndex(i)
        elif field == 'category':
            session = cbpos.database.session()
            items = session.query(Category.display, Category).all()
            self.f[field].clear()
            self.f[field].addItem("", None)
            for i, item in enumerate(items):
                self.f[field].addItem(*item)
                if item[1] == data:
                    self.f[field].setCurrentIndex(i+1)
