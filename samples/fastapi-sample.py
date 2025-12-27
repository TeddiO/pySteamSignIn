import os, sys
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# Not ideal, but for the sake of an example
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
from pysteamsignin.steamsignin import SteamSignIn

app = FastAPI()

@app.get('/')
def main(login = None):
	if login != None:
		steamLogin = SteamSignIn()
		# FastAPI expects an explicit return on the route.
		return steamLogin.RedirectUser(steamLogin.ConstructURL('http://localhost:8080/processlogin'))

	return HTMLResponse('Click <a href="/?login=true">to log in</a>')

@app.get('/processlogin/')
def process(request: Request):

	steamLogin = SteamSignIn()
	steamID = steamLogin.ValidateResults(request.query_params)

	if steamID is not False:
		return HTMLResponse('We logged in successfully!<br />SteamID: {0}'.format(steamID))
	else:
		return HTMLResponse('Failed to log in, bad details?')

	# At this point, redirect the user to a friendly URL.

if __name__ == '__main__':
	uvicorn.run(app, host="0.0.0.0", port = 8080)
