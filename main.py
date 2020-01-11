# https://github.com/reddit-archive/reddit/wiki/OAuth2-Python-Example
import json, logging, requests, os, base64, datetime
import hashlib
import pprint
pp = pprint.PrettyPrinter()


logger = logging.getLogger(str(os.getpid()) +'."'+__file__+'"')
logger.info('Loaded '+ __file__)

# these line only for debug
# fh = logging.FileHandler(__file__ + '.log')
# fh.setLevel(logging.DEBUG)
# logger.addHandler(fh)




from pytz import timezone
import xml.etree.ElementTree as ET
import python_deutschepost.interface as bk
from pdfrw import PdfReader, PdfWriter, PageMerge



class PaketPlus:
	def __init__(self, config, test=True):
		self.config = config['test_paketplus'] if test else config['production_paketplus']
		self.test = test
		self.wallet_balance = None
		self.token = None
		if self.test:
			self.base_url = 'https://api-qa.deutschepost.com/'
		else:
			self.base_url = 'https://api.deutschepost.com/'

		
		self.token = self.get_user_token()
		
		logger.debug('initialized PaketPlus as test=' + str(test) )
	
	def __str__(self):
		return str({
			'config':self.config,
			'test':self.test,
			'wallet_balance':self.wallet_balance,
			'token':self.token,
			'base_url':self.base_url})
	
	def api_call(self, url, method='get', oauth=None,
				 params=None, files=None, data=None, headers = None, 
				 response_is_json = True, return_full=False):
		# see examples here https://www.programcreek.com/python/example/2253/requests.put   or  https://stackoverflow.com/questions/44855616/how-to-add-a-new-item-using-python-etsy-http-api-methods  
		full_url = self.base_url + url
		
		response = requests.request(method, full_url,  data=data, params=params, 
								  files=files, headers=headers)   
		
		if response.status_code != requests.codes.ok:
			logger.debug(str(s) for s in (method, full_url, data, params, files))
		try:
			if return_full:
				return response
			else:
				return json.loads(response.text) if response_is_json else response.text
		except (TypeError, ValueError):
			logger.exception('json.loads(response.text) raised error')
			return response.text
	
		
	def gen_full_headers(self):
		def compute_1c4a_hash(partner_id, req_ts, key_phase, key):
			# trim leading and trailing spaces of each argument
			# idenitcal function as in https://gitlab.com/gsauthof/python-inema/tree/master
			partner_id = partner_id.strip()
			req_ts = req_ts.strip()
			key_phase = key_phase.strip()
			key = key.strip()
			# concatenate with "::" separator
			inp = "%s::%s::%s::%s" % (partner_id, req_ts, key_phase, key)
			# compute MD5 hash as 32 hex nibbles
			md5_hex = hashlib.md5(inp.encode('utf8')).hexdigest()
			# return the first 8 characters
			return md5_hex[:8]

		def gen_timestamp():
			de_zone = timezone("Europe/Berlin")
			de_time = datetime.datetime.now(de_zone)
			return de_time.strftime("%d%m%Y-%H%M%S")
		
		
		if self.token is None:
			authorization_str = ":".join([self.config['portokasse']['user'], self.config['portokasse']['password']])
			authorization = base64.b64encode(authorization_str.encode()).decode()
			full_authorization_str = 'Basic ' + authorization
			logger.debug('get_user_token authorization_str= ' + pp.pformat(authorization_str))
		else:
			full_authorization_str = 'Bearer '+ self.token
		
		timestamp = self.config['1C4A']['request_timestamp'] if self.test else gen_timestamp()
		headers = {
			'Content-Type': 'application/json',
			'Accept': '',
			'Authorization': full_authorization_str,
			'KEY_PHASE': '1',
			'PARTNER_ID': self.config['1C4A']['partner_id'],
			'REQUEST_TIMESTAMP': timestamp,
			'PARTNER_SIGNATURE': (self.config['1C4A']['partner_signature'] if self.test else 
									 compute_1c4a_hash(self.config['1C4A']['partner_id'], 
										  timestamp, 
										  self.config['1C4A']['key_phase'], 
										  self.config['1C4A']['key'])),
		}
		logger.debug('get_user_token header= ' + pp.pformat(headers))
		return headers
	
	
	def get_user_token(self):
		"""
		https://api-qa.deutschepost.com/dpi-apidoc/#/reference/authentication/access-token/get-access-token	
	
		Returns
		-------
		TYPE
			DESCRIPTION.
		"""
		
		response = self.api_call('v1/auth/accesstoken', 
							method='get', headers=self.gen_full_headers(), response_is_json = False)
		
		logger.debug('get_user_token response: ' + pp.pformat(response))
		xml = ET.fromstring(response)
		
		token = None
		for child in xml:
			for child2 in child:
				for child3 in child2:
					if "userToken" in child3.tag:
						token = child3.text
					if "walletBalance" in child3.tag:
						self.wallet_balance = float(child3.text)/100
		
		logger.info('get_user_token token: ' + str(token))
		return token
		
		
	def list_available_products(self):
		products = """
		PPL-ID		Produkt													 Preis in Cent\n
				 \n
				10246  Warenpost International		XS	Non-EU		  Untracked	   320\n
				10247  Warenpost International		S	 Non-EU		  Untracked	   370\n
				10248  Warenpost International		M	 Non-EU		  Untracked	   700\n
				10249  Warenpost International		L	 Non-EU		  Untracked	  1700\n
				10250  Warenpost International		XS	Non-EU		  Tracked		 545\n
				10251  Warenpost International		S	 Non-EU		  Tracked		 595\n
				10252  Warenpost International		M	 Non-EU		  Tracked		 925\n
				10253  Warenpost International		L	 Non-EU		  Tracked		1925\n
				10254  Warenpost International		XS	EU			  Untracked	   381\n
				10255  Warenpost International		S	 EU			  Untracked	   440\n
				10256  Warenpost International		M	 EU			  Untracked	   833\n
				10257  Warenpost International		L	 EU			  Untracked	  2023\n
				10258  Warenpost International		XS	EU			  Tracked		 649\n
				10259  Warenpost International		S	 EU			  Tracked		 708\n
				10260  Warenpost International		M	 EU			  Tracked		1101\n
				10261  Warenpost International		L	 EU			  Tracked		2291\n
				10272  Warenpost International		KT	Non-EU		  Untracked	   100\n
				10273  Warenpost International		KT	Non-EU		  Tracked		 325\n
				10270  Warenpost International		KT	EU			  Untracked	   100\n
				10271  Warenpost International		KT	EU			  Tracked		 325\n
				10280  Warenpost International		XS	Non-EU		  Unterschrift	570\n
				10281  Warenpost International		S	 Non-EU		  Unterschrift	620\n
				10282  Warenpost International		M	 Non-EU		  Unterschrift	950\n
				10283  Warenpost International		L	 Non-EU		  Unterschrift   1950\n
				10284  Warenpost International		XS	EU			  Unterschrift	678\n
				10285  Warenpost International		S	 EU			  Unterschrift	738\n
				10286  Warenpost International		M	 EU			  Unterschrift   1131\n
				10287  Warenpost International		L	 EU			  Unterschrift   2321\n
				10292  Warenpost International		KT	EU			  Unterschrift	350\n
				10293  Warenpost International		KT	Non-EU		  Unterschrift	350\n

				""".replace('				', '')
		return products
		
	
	def create_order(self, product_code, shipment):
		"""

		Parameters
		----------
		product_code : int or str
			See self.list_available_products() for product codes
		shipment: interface.Shipment type
			DESCRIPTION.

		Returns
		-------
		item_ids : TYPE
			List of label/item ids
		response: response object
		"""
		def _2str(*args, sep=' '):
			cleaned_args = [str(arg) for arg in args if not arg is None]
			return sep.join(cleaned_args)
		
		sender = shipment['sender_info']
		recipient = shipment['recipient_info']
		
		
		total_amount = sum([item_stack['number'] for item_stack in shipment['item_stacks']])
		total_weight = max(1, sum([item_stack['number'] * item_stack['item']['weight'] if (not item_stack['item']['weight'] is None) else 100
							   for item_stack in shipment['item_stacks']]))
		
		values = {
		  "customerEkp": _2str(self.config['portokasse']['ekp']),
		  "orderStatus": "FINALIZE",  
		  "paperwork": {
			 "contactName": _2str(sender['address']['name']),
			 "pickupType": "CUSTOMER_DROP_OFF",
			 "awbCopyCount": 1
		  },
		  "items": [
			{
			  "product": _2str(product_code),
			  "serviceLevel": "STANDARD",
			  "recipient": _2str(recipient['address']['name']),
			  "recipientPhone": _2str(recipient['phone']),
			  "recipientFax": _2str(recipient['fax']),
			  "recipientEmail": _2str(recipient['email']),
			  "addressLine1": _2str(recipient['address']['street'], 
							   recipient['address']['house_number']),
			  "addressLine2": _2str(recipient['address']['street2']),
			  "addressLine3": _2str(recipient['address']['street3']),
			  "city": _2str(recipient['address']['city']),
			  "state": _2str(recipient['address']['state']),
			  "postalCode": _2str(recipient['address']['post_code']),
			  "destinationCountry": _2str(recipient['address']['country_code']),
			  "shipmentAmount": total_amount,
			  "shipmentCurrency": "EUR",
			  "shipmentGrossWeight": total_weight,
			  "senderName": _2str(sender['address']['name']),
			  "senderAddressLine1": _2str(sender['address']['street'], 
									 sender['address']['house_number']) ,
			  "senderAddressLine2": _2str(sender['address']['street2']),
			  "senderCountry": _2str(sender['address']['country_code']),
			  "senderCity": _2str(sender['address']['city']),
			  "senderPostalCode": _2str(sender['address']['post_code']),
			  "senderPhone": _2str(sender['phone']),
			  "senderEmail": _2str(sender['email']),
			  "shipmentNaturetype": "SALE_GOODS",			  			  
			  "contents": [
				{
				  "contentPieceDescription": _2str(item_stack['item']['description_short']),
				  "contentPieceNetweight": 
					  item_stack['number'] * item_stack['item']['weight'] if (not item_stack['item']['weight'] is None) else 100,
				  "contentPieceOrigin": _2str(sender['address']['country_code']),
				  "contentPieceAmount": _2str(item_stack['number']),
				  "contentPieceValue": item_stack['number'] * item_stack['item']['price']
				}
			  for item_stack in shipment['item_stacks']]
			}
		  ]
		}
		
		# create order
		response = self.api_call('dpi/shipping/v1/orders', 
					method='post', 
					 data=json.dumps(values), headers=self.gen_full_headers())
		
		logger.debug('create_order response: ' + pp.pformat(response))
		if not 'shipments' in response:
			logger.warning('No label was created. ' +' response: ' + pp.pformat(response))
			logger.debug('values = ' + str(values))
			return None, response
# 			raise Exception('No label was created. ' +' response: ' + pp.pformat(response))
		item_ids = [item['id'] for item in response['shipments'][0]['items']]
		logger.info('create_order item_ids: ' + pp.pformat(item_ids))
		return item_ids, response
	

	def retrieve_label(self, item_id, filename=None, return_pdf=True):
		"""
		Possible return values (defined in headers['Accept']) are:		
			“image/png” (A6)		
			“image/png+6x4” (6x4 inch)
			“application/pdf” (A6)
			“application/pdf+singlepage” (A6)
			“application/pdf+singlepage+6x4” (6x4 inch)
			“application/zpl” (A6)
			“application/zpl+rotated” (rotated by 90 degrees for label printers)
			“application/zpl+6x4” (6x4 inch)
			“application/zpl+rotated+6x4”  (6x4 inch and rotated by 90 degrees for label printers)
		"""
		
		headers = self.gen_full_headers()
		headers['Accept'] = 'application/pdf' if return_pdf else 'image/png'
			
		# create order
		response = self.api_call('dpi/shipping/v1/items/'+str(item_id)+'/label', 
					method='get', 
					headers=headers, return_full=True)
		logger.debug('retrieve_label response: ' + pp.pformat(response))
		
		file_ending = '.pdf' if return_pdf else '.png'
		if filename is None:
			filename  = (datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' 
						+ str(item_id) + file_ending)
		with open(filename , 'wb') as f:
			f.write(response.content)
		logger.debug('retrieve_label wrote_file: ' + pp.pformat(filename))
		return filename

	def add_signature_to_pdf(self, input_file, signature_filename="signature.pdf"):
		"""
		adding a signature (pdf) ontop of a pdf

		Returns
		-------
		output filename
		"""
		
		output_file = input_file[:-4] + '_signed.pdf'
		
		# define the reader and writer objects
		reader_input = PdfReader(input_file)
		writer_output = PdfWriter()
		watermark_input = PdfReader(signature_filename)
		watermark = watermark_input.pages[0]
		
		# go through the pages one after the next
		for current_page in range(len(reader_input.pages)):
			merger = PageMerge(reader_input.pages[current_page])
			merger.add(watermark).render()
		
		# write the modified content to disk
		writer_output.write(output_file, reader_input)	
		
		logger.debug('signed file: '+ input_file + ' --> ' + output_file)
		return output_file


##




