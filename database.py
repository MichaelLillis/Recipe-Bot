import pyrebase
 
def patch():
    from urllib.parse import quote
    # Monkey patch pyrebase: replace quote function in pyrebase to workaround a bug.
    # See https://github.com/thisbejim/Pyrebase/issues/294.
    pyrebase.pyrebase.quote = lambda s, safe=None: s

    def get_url(self, token=None):
        path = self.path
        self.path = None
        if path.startswith('/'):
            path = path[1:]
        if token:
            return "{0}/o/{1}?alt=media&token={2}".format(self.storage_bucket, quote(path, safe=''), token)
        return "{0}/o/{1}?alt=media".format(self.storage_bucket, quote(path, safe=''))

    pyrebase.pyrebase.Storage.get_url = lambda self, token=None: \
        get_url(self, token)


# Insert your config
firebaseConfig = {
    "apiKey": "xxxxxxxxxxxxxxxxxx",
    "authDomain": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
    "databaseURL": "https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "projectId": "xxxxxxxxxxxxxxxxxxxx",
    "storageBucket": "xxxxxxxxxxxxxxxxxxxxxxxx",
    "messagingSenderId": "1111111111111111111",
    "appId": "1: 11111111111111: web: xxxxxxxxxxxxxxxxxxxxxx",
    "measurementId": "xxxxxxxxxxxxxxxxxxx"
}
 
