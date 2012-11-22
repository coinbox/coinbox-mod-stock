import cbpos

from cbpos.mod.stock.models import Product, Category

from cbpos.mod.base.controllers import FormController

class CategoriesFormController(FormController):
    cls = Category
    
    def fields(self):
        return {"name": (cbpos.tr.auth._("Name"), ""),
                "parent": (cbpos.tr.auth._("Parent Category"), None),
                }
    
    def items(self):
        session = cbpos.database.session()
        items = session.query(Category.display, Category).all()
        return items
    
    def canDeleteItem(self, item):
        session = cbpos.database.session()
        category_count = session.query(Category).filter(Category.parent == item).count()
        if category_count != 0:
            return False
        product_count = session.query(Product).filter(Product.category == item).count()
        if product_count != 0:
            return False
    
    def canEditItem(self, item):
        return True
    
    def canAddItem(self):
        return True
    
    def getDataFromItem(self, field, item):
        return getattr(item, field)

class ProductsFormController(FormController):
    cls = Product
    
    def fields(self):
        
        import cbpos.mod.currency.controllers as currency
        
        return {"name": (cbpos.tr.auth._("Name"), ""),
                "description": (cbpos.tr.auth._("Description"), ""),
                "reference": (cbpos.tr.auth._("Reference"), ""),
                "code": (cbpos.tr.auth._("Code"), ""),
                "price": (cbpos.tr.auth._("Price"), 0),
                "currency": (cbpos.tr.auth._("Currency"), currency.default),
                "in_stock": (cbpos.tr.auth._("In Stock"), True),
                "quantity": (cbpos.tr.auth._("Quantity"), 0),
                "category": (cbpos.tr.auth._("Category"), None), 
                }
    
    def items(self):
        session = cbpos.database.session()
        items = session.query(Product.display, Product).all()
        return items
    
    def canDeleteItem(self, item):
        return True
    
    def canEditItem(self, item):
        return True
    
    def canAddItem(self):
        return True
    
    def getDataFromItem(self, field, item):
        return getattr(item, field)
