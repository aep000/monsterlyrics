from flask import Flask, request, redirect, jsonify
def songExists1(songID,q):
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    con = mdb.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = con.cursor()
    cur.execute(q)
    return cur.fetchone() is not None
def authenticate(func):
    def wrapper():
        request.args.get('auth')
        query = "SELECT * FROM auth WHERE code='"+auth+"'"
        if songExists1(1,query):
            
        else:
            return redirect("/", code=302)
    return wrapper

def login():
    name = request.args.get('user')
    pas = request.args.get('pass')
    hpass = hashlib.sha224(pas).hexdigest()
    query = "SELECT * FROM auth WHERE "
    if songExists1()


'''
def Nauth(func):
    auth = request.args.get('auth')
    query = "SELECT * FROM auth WHERE code='"+auth+"'"
    if songExists(1,query):
        return func()
    else:
        return redirect("/dashboard", code=302)

def login():
'''
