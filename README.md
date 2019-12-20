# python_deutschepost
This is a python access to the DeutschePost PaketPlus API. Specifically the (extended) Internetmarken products.

## What is this API for?

DeutschePost has (at least) 2 apis:

1. Internetmarke SOAP API. There is a very good python wrapper for it http://git.sysmocom.de/python-inema/
2. Deutsche Post REST https://api-qa.deutschepost.com/dpi-apidoc/ . There seems to be no python wrapper for it (yet). 
   * The Internetmarke products are also available through this API, however the REST API is only a wrapper for the underlying SOAP API. 
   * **Some Internetmarke products are "extended" through this API**. For example is the "Warenpost International" (with a customs form) only available with this API.
   * This module is the start to make at least the "extended" Internetmarke products available in python.

## Problems

Because the Internetmarke SOAP API is wrapped by a REST API, some responses are soap responses (xml), and some are rest responses (json).

Only a few of the api calls from https://api-qa.deutschepost.com/dpi-apidoc  are forwarded to the Internetmerke API.

