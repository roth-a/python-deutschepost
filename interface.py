

class Address(dict):
	def __init__(self):
		self['name'] = None
		self['house_number'] = None
		self['street'] = None
		self['street2'] = None
		self['street3'] = None
		self['post_code'] = None
		self['city'] = None
		self['state'] = None
		self['country'] = None
		self['country_code'] = None   #  https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv

	
	def fill(self, name, street, street2, post_code, city, state, country_code, house_number = None):
		self['name'] = name
		if house_number is None:			
			self['street'], self['house_number'] = self.street_split(street)
		else:
			self['street'] = street
			self['house_number'] = str(house_number)			
		self['street2'] = street2
		self['post_code'] = post_code
		self['city'] = city
		self['state'] = state
		self['country_code'] = country_code
		
		
		
	def street_split(self, street):
		"""
		Splits a street (with house number) into a street, house_number

		Parameters
		----------
		street : TYPE
			DESCRIPTION.

		Returns
		-------
		street_name : TYPE
			DESCRIPTION.
		house_number : TYPE
			DESCRIPTION.

		"""
		street_name = street
		house_number = ""
		if not isinstance(street, str): 
			return street_name, house_number

		street_splitted = street.split(' ')
		if street_splitted[-1][:-1].isdigit():   # the [:-1] accounts for the fact, that a house number could be:  35b
			street_name = " ".join(street_splitted[:-1])	
			house_number = street_splitted[-1]	


		for substr in ["Str.", "Straße"]:
			if len(street_splitted)<2:		
				substr = substr.lower()
				if substr in street_splitted[0].lower():
					idx = street_splitted[0].lower().find(substr)  + len(substr)
					street_name = street_splitted[0][:idx]
					house_number = street_splitted[0][idx:]

		return street_name, house_number

class Entity(dict):
	def __init__(self):
		self['id'] = None
		self['description'] = None
		self['address'] = Address()
		self['email'] = None
		self['phone'] = None
		self['fax'] = None


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

 
