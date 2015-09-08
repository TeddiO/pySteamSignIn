import requests
from urllib.parse import urlencode

'''
	Steam OpenID 2 Sign in class
		- Light framework that will return the 64 bit SteamID if they succesfully log in. 
		- Has some bottlepy support to ensure the user gets redirected correctly.


'''

class SteamSignIn():

	_provider = 'http://steamcommunity.com/openid/login'

	try:
		import bottle
		from bottle import response

		#This is designed to redirect the user. Only functional when using bottlepy
		#Any other system will require you to redirect the user in another way.
		def RedirectUser(self, strPostData):
			response.status = 303
			response.set_header('Location', "{0}?{1}".format(_provider,strPostData ))	
			response.add_header('Content-Type', 'application/x-www-form-urlencoded')
			return response
	except Exception as error:
		print('Bottle is not installed! Cannot use RedirectUser()')

		
	#This is the basic setup for getting steam to acknowledge our request for OpenID (2).
	#We specify a responseURL because hey, easy.
	#Returns a string that is safe to use via a POST.	
	def ConstructURL(self, responseURL):

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
		reqData = requests.post(provider, validationArgs)

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

