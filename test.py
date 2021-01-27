# copy this file  and deutschepost.yaml to ../

import python_deutschepost
import yaml

#%%
with open("config.yaml", "r") as file:
	config = list(yaml.load_all(file))[0]

paket_plus = python_deutschepost.PaketPlus(config, test=True)

#%%
# print(paket_plus.get_user_token())
# print(paket_plus.wallet_balance)
#%%

sender = python_deutschepost.interface.Entity()
recipient = python_deutschepost.interface.Entity()

sender['address']['name'] = 'Marge Bouvier'
sender['address']['house_number'] = '10'
sender['address']['street'] = 'Düsseldorfer Straße '
sender['address']['post_code'] = '11001'
sender['address']['city'] = 'Berlin'
sender['address']['country_code'] = 'DE'   # country codes can be found here: https://country-code.cl/

recipient['address']['name'] = 'Homer Simpson'
recipient['address']['house_number'] = '4'
recipient['address']['street'] = 'Market Square.'
recipient['address']['post_code'] = '53911'
recipient['address']['city'] = 'Springfield'
recipient['address']['country_code'] = 'US'   # country codes can be found here: https://country-code.cl/

shipment = python_deutschepost.interface.Shipment()
shipment['sender_info'] = sender
shipment['recipient_info'] = recipient


item_stacks = [python_deutschepost.interface.ItemStack()]
item_stacks[0]['number'] = 2
item_stacks[0]['item']['description_short'] = 'Flash light'
item_stacks[0]['item']['price'] = 12.99

shipment['item_stacks'] = item_stacks
# pprint(shipment)
item_ids = paket_plus.create_order(10251, shipment)
#%%
filenames = [paket_plus.retrieve_label(item_id) for item_id in item_ids]

signed_filenames = [paket_plus.add_signature_to_pdf(filename) for filename in filenames]
print(signed_filenames)

#%%
