import os, atexit, json, msal, requests
cache = msal.SerializableTokenCache()
if os.path.exists("my_cache.bin"):
    cache.deserialize(open("my_cache.bin", "r").read())
atexit.register(lambda:
    open("my_cache.bin", "w").write(cache.serialize())
    # Hint: The following optional line persists only when state changed
    if cache.has_state_changed else None
    )

_AZURE_CLI = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
username = "johndoe@rayluombaoutlook.onmicrosoft.com"
scopes = [
    #"https://graph.microsoft.com/.default",  # Proprietary tokens can't be verified
    #"api://73a45c2a-b33b-47e7-87a4-7ea09449330f/Secret",  # scp would be "Secret"
    "api://73a45c2a-b33b-47e7-87a4-7ea09449330f/.default",  # scp would still be "Secret"
]
app = msal.PublicClientApplication(
    _AZURE_CLI,
    authority="https://login.microsoftonline.com/organizations",
    token_cache=cache,
    )
result = None
accounts = app.get_accounts(username=username)
if accounts:
    result = app.acquire_token_silent(scopes, account=accounts[0])
if not result:
    result = app.acquire_token_interactive(scopes, login_hint=username)
print(json.dumps(result, indent=2))
resp = requests.get("http://localhost:5000/resource", headers={
    "Authorization": f"Bearer {result['access_token']}",
})
print(resp, resp.text, resp.headers)
