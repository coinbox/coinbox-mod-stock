import cbpos

from cbmod.stock.models import Product, Category

from cbmod.base.controllers import FormController

class CategoriesFormController(FormController):
    cls = Category
    
    def fields(self):
        return {"name": (cbpos.tr.stock_("Name"), ""),
                "parent": (cbpos.tr.stock_("Parent Category"), None),
                "image": (cbpos.tr.stock_("Image"), None),
                }
    
    def items(self):
        session = cbpos.database.session()
        return session.query(Category)
    
    def canDeleteItem(self, item):
        session = cbpos.database.session()
        
        # Check if it has a sub-category
        category_count = session.query(Category).filter(Category.parent == item).count()
        if category_count != 0:
            return False
        
        # Check if it has products
        product_count = session.query(Product).filter(Product.category == item).count()
        if product_count != 0:
            return False
        
        # If not we can delete it
        return True
    
    def canEditItem(self, item):
        return True
    
    def canAddItem(self):
        return True
    
    def getDataFromItem(self, field, item):
        return getattr(item, field)

class ProductsFormController(FormController):
    cls = Product
    
    def fields(self):
        
        import cbmod.currency.controllers as currency
        
        return {"name": (cbpos.tr.stock_("Name"), ""),
                "description": (cbpos.tr.stock_("Description"), ""),
                "reference": (cbpos.tr.stock_("Reference"), ""),
                "code": (cbpos.tr.stock_("Code"), ""),
                "price": (cbpos.tr.stock_("Price"), 0),
                "currency": (cbpos.tr.stock_("Currency"), currency.default),
                "in_stock": (cbpos.tr.stock_("In Stock"), True),
                "quantity": (cbpos.tr.stock_("Quantity"), 0),
                "category": (cbpos.tr.stock_("Category"), None),
                "image": (cbpos.tr.stock_("Image"), None),
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
