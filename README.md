# python_deutschepost
Warning: so far only the test system works, but not with the production data. 

This wrapper makes it possible to create shipping labels "Warenpost International" of this form:

![example.png](example.png)



## DeutschePost API Structure

DeutschePost has (at least) 2 APIs:

1. Internetmarke SOAP API. There is a very good python wrapper for it http://git.sysmocom.de/python-inema/
2. Deutsche Post REST https://api-qa.deutschepost.com/dpi-apidoc/ . There seems to be no python wrapper for it (yet). 
   * The Internetmarke products are also available through this API, however the REST API is only a wrapper for the underlying SOAP API. 
   * **Some Internetmarke products are "extended" through this API**. For example is the "Warenpost International" (with a customs form) only available with this API.  The Internetmarke API  only offers  "Warenpost International" (**without** a customs form), and it is not clear if this is valid.
   * This module offers these "extended" Internetmarke products available in python.

## Problems

Because the Internetmarke SOAP API is wrapped by a REST API, some responses are soap responses (xml), and some are rest responses (json).

Only a few of the api calls from https://api-qa.deutschepost.com/dpi-apidoc  are forwarded to the Internetmarke API.

This creates the weird situation that even though 1 api is used, the fractured underlying apis and systems are painfully obvious. 
