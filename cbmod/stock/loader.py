import cbpos
from cbpos.modules import BaseModuleLoader

class ModuleLoader(BaseModuleLoader):
    def load_models(self):
        from cbmod.stock.models import Category, Product, DiaryEntry
        return [Category, Product, DiaryEntry]

    def test_models(self):
        from cbmod.stock.models import Category, Product
    
        session = cbpos.database.session()
    
        cat1 = Category(name='Root1', parent=None)
        cat2 = Category(name='Sub1', parent=cat1)
        cat3 = Category(name='Sub2', parent=cat1)
        cat4 = Category(name='Sub2-Sub1', parent=cat3)
        cat5 = Category(name='Root2', parent=None)
    
        from cbmod.currency.models import Currency
        
        LBP = session.query(Currency).filter_by(id="LBP").one()
        EUR = session.query(Currency).filter_by(id="EUR").one()
    
        p1 = Product(name='MAPED PENCILS 12-BOX', description='12 pencils box Maped', reference='ref123',
                     code='code123', price=1000, currency=LBP, quantity=10, category=cat1)
        p2 = Product(name='MAPED SINGLE PENCIL', description='1 pencil Maped', reference='ref122',
                     code='code12345', price=250, currency=LBP, quantity=20, category=cat2)
        p3 = Product(name='MAPED ERASER', description='Rounded Maped Eraser', reference='ref133',
                     code='code456', price=2, currency=EUR, quantity=5, category=cat3)
        p4 = Product(name='PHOTOCOPY B/W', description='Black and White Photocopy', reference='',
                     code='12345', price=250, currency=LBP, quantity=None, category=cat4, in_stock=False)
        p5 = Product(name='ANNAHAR', description='An-Nahar Lebanese Daily Newspaper', reference='789',
                     code='barcode135', price=2000, currency=LBP, quantity=None, category=cat5, in_stock=False)
    
        [session.add(p) for p in (p1, p2, p3, p4, p5)]
        session.commit()

    def menu(self):
        from cbpos.interface import MenuRoot, MenuItem
        from cbmod.stock.views import CategoriesPage, ProductsPage, StockDiaryPage
        
        return [[MenuRoot('stock',
                          label=cbpos.tr.stock_('Stock'),
                          icon=cbpos.res.stock('images/menu-stock.png')
                          )],
                [MenuItem('products', parent='stock',
                          label=cbpos.tr.stock_('Products'),
                          icon=cbpos.res.stock('images/menu-products.png'),
                          page=ProductsPage
                          ),
                 MenuItem('categories', parent='stock',
                          label=cbpos.tr.stock_('Categories'),
                          icon=cbpos.res.stock('images/menu-categories.png'),
                          page=CategoriesPage
                          ),
                 MenuItem('stock-diary', parent='stock',
                          label=cbpos.tr.stock_('Stock Diary'),
                          icon=cbpos.res.stock('images/menu-stock-diary.png'),
                          page=StockDiaryPage
                          )
                 ]
                ]
