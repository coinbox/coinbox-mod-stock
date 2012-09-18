import cbpos

from cbpos.mod.base.widgets import Catalog

from cbpos.mod.stock.models import Product, Category

class ProductCatalog(Catalog):
    
    def getAll(self, search=None):
        session = cbpos.database.session()
        query = session.query(Product, Product.name)
        #if self.show_only_in_stock:
        #    query = query.filter(Product.in_stock)
        if search is not None:
            query = query.filter(Product.name.like('%%%s%%' % (search,)))
        return query.all()
    
    def getChildren(self, parent=None, search=None):
        session = cbpos.database.session()
        product_query = session.query(Product, Product.name)
        #if self.show_only_in_stock:
        #    product_query = product_query.filter(Product.in_stock)
        return [session.query(Category, Category.name).filter(Category.parent == parent).all(),
                product_query.filter(Product.category == parent).all()]
