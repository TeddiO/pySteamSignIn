# pySteamSignIn
A lightweight Python 3 helper class for getting OpenID 2.0 Steam sign-in up and running quickly.

There aren’t really any Steam-specific OpenID 2.0 sign-in libraries that provide clear documentation or insight into how the flow actually works. Most guidance instead points people at generic OpenID libraries, which are often overkill for Steam and fairly bloated in practice.

As a result of this pySteamSignIn is designed to let you plug in Steam Auth as quick as possible and let you start returning results immediately.

## Installation
pySteamSignIn is now available on pip!

`pip install steamsignin`

## Lets quickly get authentication rolling

The power behind this is it provides the entire auth process over two (or three, if you're using bottlepy / Flask / FastAPI) functions.
The first function is ConstructURL, which takes a string and returns a string

The string to pass is whatever page the user is going to be sent back to as a result of logging in with Steam.

```Python
from pysteamsignin.steamsignin import SteamSignIn

steamLogin = SteamSignIn()
encodedData = steamLogin.ConstructURL('https://0.0.0.0:8080/processlogin'))
ForwardClientToSteamPage(encodedData) #Not a real function, but the next action you'd take
...
```

At this point you forward the client on with a post request to https://steamcommunity.com/openid/login and you'll get thrown a bunch of stuff back. 

The important thing here is that you get thet GET returned data put into a  dictionary to then pass on to ValidateResults


```python
# Some function where the data has been passed in a dictionary no less
steamLogin = SteamSignIn()
returnedSteamID = steamLogin.ValidateResults(dictionaryGoesHere)
# Perform checks to see if you actually have something that isn't false
...
```
And that's the general gist of it! At this point the user has been validated by Steam's own servers so the Steam64ID returned is one that can be trusted.
### If you use Bottlepy, Flask or FastAPI...

An additional helper function has been provided under the guise of RedirectUser.
This will just relay the user on your behalf to the Steam site, as such 

```Python
steamLogin = SteamSignIn()
steamLogin.RedirectUser(steamLogin.ConstructURL('https://0.0.0.0:8080/processlogin'))
# In the case of Flask / FastAPI, return the above RedirectUser call instead.
...
```

## Dependencies
The core of pySteamSignIn uses only the Python standard library and does not depend on external HTTP clients such as requests.
Optional helper functions are provided for common web frameworks (Bottle, Flask, FastAPI) and are only enabled if those frameworks are already installed.

## Finally

Hopefully this helps someone out in terms of getting Steam OpenID and Python working in harmony. There's a few solutions for Flask and Django (which are basically glorified wrappers for python-openid) but both of them can still result in a fair few steps.

This is based on OpenID 2.0 and **not** OpenID Connect / OAuth 2.

If you require a Go version of this library, this is available [here](https://github.com/TeddiO/GoSteamAuth).


