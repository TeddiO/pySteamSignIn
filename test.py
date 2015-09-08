from bottle import run, request, route
from steamsignin import SteamSignIn

@route('/')
def main():

	shouldLogin = request.query.get('login')

	if shouldLogin != None:
		steamLogin = SteamSignIn()
		steamLogin.RedirectUser(steamLogin.ConstructURL('http://82.39.161.25:8080/processlogin'))

	return 'Click <a href="/?login=true">to log in</a>'


@route('/processlogin')
def process():

	returnData = request.params

	steamLogin = SteamSignIn()
	steamID = steamLogin.ValidateResults(returnData)

	print(steamID)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug = True, reloader = False)