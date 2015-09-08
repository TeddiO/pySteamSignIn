import requests, re
from urllib.parse import urlencode

try:
	import bottle
	from bottle import response

except ImportError as error:
	print('Bottle is not installed! Cannot use RedirectUser()')

'''
	Steam OpenID 2 Sign in class
		- Light framework that will return the 64 bit SteamID if they succesfully log in. 
		- Has some bottlepy support to ensure the user gets redirected correctly.
		- Tries to be as friendly as possible. 


'''

class SteamSignIn():

	_provider = 'http://steamcommunity.com/openid/login'


	def RedirectUser(self, strPostData):
		if bottle == None:
			return
		response.status = 303
		response.set_header('Location', "{0}?{1}".format(self._provider,strPostData ))	
		response.add_header('Content-Type', 'application/x-www-form-urlencoded')
		return response

		
	#This is the basic setup for getting steam to acknowledge our request for OpenID (2).
	#We specify a responseURL because hey, easy.
	#Returns a string that is safe to use via a POST.	
	def ConstructURL(self, responseURL):

		#Just test to see if http or https is in the string. If not, we'll add the string
		#(OpenID requires the protocol type to be specified)
		refinedScripts = re.search('(?:http)', responseURL)
		if refinedScripts == None or refinedScripts.group(0) == None:
			responseURL = "http://{0}".format(responseURL)

		authParameters = {
			"openid.ns":"http://specs.openid.net/auth/2.0",
			"openid.mode": "checkid_setup",
			"openid.return_to": responseURL, 
			"openid.realm": responseURL, 
			"openid.identity": "http://specs.openid.net/auth/2.0/identifier_select", 
			"openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
		}

		return urlencode(authParameters)


	#Takes a dict type object. This should be provided by whatever framework you're using with all 
	#the GET variables passed on.
	def ValidateResults(self,results):

		validationArgs ={
		'openid.assoc_handle': results['openid.assoc_handle'],
		'openid.signed': results['openid.signed'],
		'openid.sig' : results['openid.sig'],
		'openid.ns': results ['openid.ns']
		}

		#Basically, we split apart one of the args steam sends back only to send it back to them to validate!
		#We also append check_authentication which tells OpenID 2 to actually yknow, validate what we send.
		signedArgs = results['openid.signed'].split(',')

		for item in signedArgs:
			itemArg = 'openid.{0}'.format(item)
			if results[itemArg] not in validationArgs:
				validationArgs[itemArg] = results[itemArg]

		validationArgs['openid.mode'] = 'check_authentication'

		#Just use requests to quickly fire the data off.
		reqData = requests.post(self._provider, validationArgs)
		reqData.connection.close()

		#is_valid:true is what Steam returns if something is valid. The alternative is is_valid:false which obviously, is false. 
		if re.search('is_valid:true', reqData.text):
			matched64ID = re.search('http://steamcommunity.com/openid/id/(\d+)', results['openid.claimed_id'])
			if matched64ID != None or matched64ID.group(1) != None:
				return matched64ID.group(1)
			else:
				#If we somehow fail to get a valid steam64ID, just return false
				return False
		else:
			#Same again here
			return False

