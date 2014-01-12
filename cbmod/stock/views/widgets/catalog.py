import cbpos
logger = cbpos.get_logger(__name__)

from cbmod.base.views.widgets import Catalog

from cbmod.stock.models import Product, Category

class ProductCatalog(Catalog):
    
    def filter(self, query, search):
        filtered = query.filter(Product.name.like('%{}%'.format(search)) | \
                                (Product.code == search) | \
                                Product.description.like('%{}%'.format(search))
                                )
        return filtered
    
    def getAll(self, search=None):
        session = cbpos.database.session()
        query = session.query(Product)
        if search is not None:
            query = self.filter(query, search)
        return ((p, p.image.path if p.image else None) for p in query)
    
    def getChildren(self, parent=None, search=None):
        session = cbpos.database.session()
        product_query = session.query(Product).filter(Product.category == parent)
        category_query = session.query(Category).filter(Category.parent == parent)
        
        if search is not None:
            product_query = self.filter(product_query, search)
        return [((c, c.image.path if c.image else None) for c in category_query),
                ((p, p.image.path if p.image else None) for p in product_query)]
