import cbpos
from cbpos.modules import BaseModuleMetadata

class ModuleMetadata(BaseModuleMetadata):
    base_name = 'stock'
    version = '0.1.0'
    display_name = 'Products Inventory Module'
    dependencies = (
        ('base', '0.1'),
        ('currency', '0.1'),
    )
    config_defaults = (
        ('mod.stock', {
                       'default_image_size': (200, 200),
                       'default_image_format': 'jpg',
                       }
         ),
    )
