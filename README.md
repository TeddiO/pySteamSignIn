# pySteamSignIn
A small Python 3 class designed to get Steam OpenID 2 sign-in up and running as quick as possible.

As of this moment in time there's not really any 'decent' Steam Openid libraries that give any proper documentation or insight in terms of how to actually use them. Alongside this they're often fairly bloated and problematic. As a result of this pySteamSignIn is a lite class designed to let you plug in Steam Auth as quick as possible and let you start returning results immediately. 

## Lets quickly get authentication rolling

The power behind this is it provides the entire auth process over two (or three, if you're using bottlepy) functions.
The first function is ConstructURL, which takes a string and returns a string

The string to pass is whatever page the user is going to be sent back to as a result of logging in with Steam.

```Python
from steamsignin import SteamSignIn

steamLogin = SteamSignIn()
encodedData = steamLogin.ConstructURL('https://0.0.0.0:8080/processlogin'))
ForwardClientToSteamPage(encodedData) #Not a real function, but the next action you'd take
...
```

At this point you forward the client on with a post request to https://steamcommunity.com/openid/login and you'll get thrown a bunch of stuff back. 

The important thing here is that you get thet GET returned data put into a  dictionary to then pass on to ValidateResults


```python
#Some function where the data has been passed in a dictionary no less
steamLogin = SteamSignIn()
returnedSteamID = steamLogin.ValidateResults(dictionaryGoesHere)
#Perform checks to see if you actually have something that isn't false
...
```
And that's the general gist of it! At this point the user has been validated by Steam's own servers so the Steam64ID returned is one that can be trusted and you can use it to store information, you can set cookies on the current client and so on. 

### If you use Bottle...

An additional helper function has been provided under the guise of RedirectUser.
This will just relay the user on your behalf to the Steam site, as such 

```Python
steamLogin = SteamSignIn()
steamLogin.RedirectUser(steamLogin.ConstructURL('https://0.0.0.0:8080/processlogin'))
...
```

## Finally

Hopefully this helps someone out in terms of getting Steam OpenID and Python working in harmony. There's a few solutions for Flask and Django (which are basically glorified wrappers for python-openid) but both of them can still result in a fair few steps.

This is based on OpenID 2.0 and **not** OpenID Connect 1.0. I'm not 100% on the various changes required, but it can possibly be used for an understanding behind the statelent OpenID connect functionality as well. 


