
class Address(dict):
    def __init__(self):
        self['name'] = None
        self['house _number'] = None
        self['street'] = None
        self['street2'] = None
        self['street3'] = None
        self['post_code'] = None
        self['city'] = None
        self['state'] = None
        self['country'] = None
        self['country_code'] = None   #  https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv


class Entity(dict):
    def __init__(self):
        self['id'] = None
        self['description'] = None
        self['address'] = Address()
        self['email'] = None
        self['phone'] = None


class Locations(list): 
    def __init__(self):
        pass

        
class UId(dict):
    def __init__(self):
        self['sku'] = None
        self['barcode'] = None


class Item(dict):
    def __init__(self):
        self['sku'] = UId()
        self['description'] = None
        self['weight'] = None
        self['description_short'] = None
        self['description_long'] = None
        self['production_date'] = None
        self['expiration_date'] = None
        self['price'] = None


class ItemStack(dict):
    def __init__(self):
        self['item'] = Item()
        self['number'] = None


class Warehouse(dict): 
    def __init__(self):
        self['id'] = None  # warehouse id  
        self['item_stacks'] = []  # list of ItemStack
        self['entity'] = Entity()  # this contains the entity id, which could own multiple warehouses
        self['shipping_cost_per_item'] = None
        self['storage_cost_per_item_per_month'] = None
        self['base_fee'] = None
        self['item_takein_cost_per_item'] = None
        


class Shipment(dict):
    def __init__(self):
        self['id'] = None
        self['description'] = None
        self['notes'] = None
        self['send_date'] = None
        self['last_location'] = None
        self['last_status'] = None
        self['receive_date'] = None
        self['recipient_info'] = Entity()
        self['sender_info'] = Entity()
        self['shipping_fees'] = []
        self['import_fees'] = []
        self['item_stacks'] = []  # list of ItemStack

 
