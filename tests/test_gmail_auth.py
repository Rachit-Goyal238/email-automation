from auth.gmail_auth import GmailAuthenticator

auth = GmailAuthenticator()

creds = auth.authenticate()

print()

print("Authentication Successful!")

print()

print(creds.valid)