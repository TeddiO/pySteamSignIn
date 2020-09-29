import sys, os
from bottle import run, request, route

# Not ideal, but for the sake of an example
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
from steamsignin import SteamSignIn

@route('/')
def main():

	shouldLogin = request.query.get('login')

	if shouldLogin is not None:
		steamLogin = SteamSignIn()
		steamLogin.RedirectUser(steamLogin.ConstructURL('http://localhost:8080/processlogin'))

	return 'Click <a href="/?login=true">to log in</a>'


@route('/processlogin')
def process():

	returnData = request.params

	steamLogin = SteamSignIn()
	steamID = steamLogin.ValidateResults(returnData)

	print('SteamID returned was: ', steamID)

	if steamID is not False:
		return 'We logged in successfully!<br />SteamID: {0}'.format(steamID)
	else:
		return 'Failed to log in, bad details?'

	# At this point, redirect the user to a friendly URL.

	
if __name__ == '__main__':
    run(host='localhost', port=8080, debug = True, reloader = False)
