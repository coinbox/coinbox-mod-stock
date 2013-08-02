import cbpos

from cbpos.mod.stock.models import Product, Category

from cbpos.mod.base.controllers import FormController

class CategoriesFormController(FormController):
    cls = Category
    
    def fields(self):
        return {"name": (cbpos.tr.stock._("Name"), ""),
                "parent": (cbpos.tr.stock._("Parent Category"), None),
                "image": (cbpos.tr.stock._("Image"), None),
                }
    
    def items(self):
        session = cbpos.database.session()
        return session.query(Category)
    
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
        
        return {"name": (cbpos.tr.stock._("Name"), ""),
                "description": (cbpos.tr.stock._("Description"), ""),
                "reference": (cbpos.tr.stock._("Reference"), ""),
                "code": (cbpos.tr.stock._("Code"), ""),
                "price": (cbpos.tr.stock._("Price"), 0),
                "currency": (cbpos.tr.stock._("Currency"), currency.default),
                "in_stock": (cbpos.tr.stock._("In Stock"), True),
                "quantity": (cbpos.tr.stock._("Quantity"), 0),
                "category": (cbpos.tr.stock._("Category"), None),
                "image": (cbpos.tr.stock._("Image"), None),
                }
    
    def items(self):
        session = cbpos.database.session()
        return session.query(Product)
    
    def canDeleteItem(self, item):
        return True
    
    def canEditItem(self, item):
        return True
    
    def canAddItem(self):
        return True
    
    def getDataFromItem(self, field, item):
        return getattr(item, field)
