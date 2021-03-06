from PySide import QtGui

import cbpos
import sys

from cbmod.stock.controllers import ProductsFormController
from cbmod.currency.models.currency import Currency
from cbmod.stock.models import Product, Category

from cbmod.base.views import FormPage
from cbmod.base.views.widgets import ImagePicker

class ProductsPage(FormPage):
    controller = ProductsFormController()
    
    def widgets(self):
        price = QtGui.QDoubleSpinBox()
        price.setRange(0, sys.maxint)

        in_stock = QtGui.QCheckBox()
        in_stock.stateChanged.connect(self.onInStockCheckBox)
        
        quantity = QtGui.QDoubleSpinBox()
        quantity.setRange(0, sys.maxint)

        return (("name", QtGui.QLineEdit()),
                ("description", QtGui.QTextEdit()),
                ("reference", QtGui.QLineEdit()),
                ("code", QtGui.QLineEdit()),
                ("price", price),
                ("currency", QtGui.QComboBox()),
                ("in_stock", in_stock),
                ("quantity", quantity),
                ("category", QtGui.QComboBox()),
                ("image", ImagePicker())
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
        if field in ('name', 'description', 'reference', 'code'):
            self.f[field].setText(data)
        elif field == 'price':
            self.f[field].setValue(data)
        elif field == 'quantity':
            if data is None:
                self.f[field].setValue(0)
            else:
                self.f[field].setValue(data)
        elif field == 'in_stock':
            self.f[field].setChecked(data)
            self.f['quantity'].setEnabled(data)
        elif field == 'currency':
            session = cbpos.database.session()
            self.f[field].clear()
            for i, item in enumerate(session.query(Currency)):
                self.f[field].addItem(item.display, item)
                if item == data:
                    self.f[field].setCurrentIndex(i)
        elif field == 'category':
            session = cbpos.database.session()
            self.f[field].clear()
            self.f[field].addItem("", None)
            for i, item in enumerate(session.query(Category)):
                self.f[field].addItem(item.display, item)
                if item == data:
                    self.f[field].setCurrentIndex(i+1)
        elif field == 'image':
            self.f[field].setImage(data)
