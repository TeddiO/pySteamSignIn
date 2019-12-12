from bottle import run, request, route
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

	print(steamID)

if __name__ == '__main__':
    run(host='localhost', port=8080, debug = True, reloader = False)
