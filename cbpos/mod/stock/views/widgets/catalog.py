import cbpos
logger = cbpos.get_logger(__name__)

from cbpos.mod.base.views.widgets import Catalog

from cbpos.mod.stock.models import Product, Category

class ProductCatalog(Catalog):
    
    def filter(self, query, search):
        filtered = query.filter(Product.name.like('%{}%'.format(search)) | \
                                (Product.code == search) | \
                                Product.description.like('%{}%'.format(search))
                                )
        return filtered
    
    def getAll(self, search=None):
        session = cbpos.database.session()
        query = session.query(Product, Product.name)
        if search is not None:
            query = self.filter(query, search)
        for (p, n) in query:
            yield (p, n, (p.image.path if p.image else None))
    
    def getChildren(self, parent=None, search=None):
        session = cbpos.database.session()
        product_query = session.query(Product, Product.name).filter(Product.category == parent)
        category_query = session.query(Category, Category.name).filter(Category.parent == parent)
        
        if search is not None:
            product_query = self.filter(product_query, search)
        return [category_query.all(),
                product_query.all()]
