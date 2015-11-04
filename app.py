from flask import Flask, request, redirect, jsonify
import json
import os
import urllib
import psycopg2 as mdb
import urlparse
import sys
import logging

def dbquery(query):
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
    cur.execute(query)
    results =  cur.fetchall()
    con.close()
    return results
def dbinsert(query):
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
    cur.execute(query)
    con.commit()
    con.close()
def songExists(songID,q):
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



app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
@app.route('/', methods=['GET', 'POST'])
def index():
    query = "SELECT * FROM votes ORDER BY votes DESC LIMIT 5"
    retval = dbquery(query)
    c = 0
    url = "https://api.spotify.com/v1/tracks/?ids="
    for row in retval:
        songs[c]['songID'] = row[0]
        songs[c]['votes'] = row[1]
        url += row[0]
        c+=1
    url = url[:-1]
    search = urllib.urlopen(url);
    Datadict = json.loads(f.read())
    f = open('index.html','r');
    return search+f.read()

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    query ="DELETE FROM votes"
    dbinsert(query)
    return redirect("/dashboard", code=302)
@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    html ='''
    <!DOCTYPE HTML>
    <!--
    	Spectral by HTML5 UP
    	html5up.net | @n33co
    	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
    -->
    <html>
    	<head>
    		<title>Monsterlyrics</title>
    		<meta charset="utf-8" />
    		<meta name="viewport" content="width=device-width, initial-scale=1" />
                <script src="aep000.neocities.org/assets/js/jquery.min.js"></script>
                <script src="aep000.neocities.org/assets/js/jquery.scrollex.min.js"></script>
                <script src="aep000.neocities.org/assets/js/jquery.scrolly.min.js"></script>
                <script src="aep000.neocities.org/assets/js/skel.min.js"></script>
                <script src="aep000.neocities.org/assets/js/util.js"></script>
                <!--[if lte IE 8]><script src="aep000.neocities.org/assets/js/ie/respond.min.js"></script><![endif]-->
                <script src="aep000.neocities.org/assets/js/main.js"></script>
    		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
    		<link rel="stylesheet" href="https://aep000.neocities.org/assets/css/main.css" />
    		<!--[if lte IE 8]><link rel="stylesheet" href="aep000.neocities.org/assets/css/ie8.css" /><![endif]-->
    		<!--[if lte IE 9]><link rel="stylesheet" href="aep000.neocities.org/assets/css/ie9.css" /><![endif]-->
    	</head>
    	<body>

    		<!-- Page Wrapper -->
    			<div id="page-wrapper">

    				<!-- Header -->
    					<header id="header">
    						<h1><a href="/">Monsterlyrics</a></h1>
    						<nav id="nav">
    							<ul>
    								<li class="special">
    									<a href="#menu" class="menuToggle"><span>Menu</span></a>
    									<div id="menu">
    										<ul>
    											<li><a href="index.html">Home</a></li>
    											<li><a href="generic.html">Generic</a></li>
    											<li><a href="elements.html">Elements</a></li>
    											<li><a href="#">Sign Up</a></li>
    											<li><a href="#">Log In</a></li>
    										</ul>
    									</div>
    								</li>
    							</ul>
    						</nav>
    					</header>

    				<!-- Main -->
    					<article id="main">
    						<header>
    							<h2>Search</h2>
                                <a href="/reset" class="button fit">Reset</a>
    							<p><form method="get" action="/dashboard">
										<div class="row uniform">
											<div class="12u$">
												<input type="text" name="search" id="demo-name" value="" placeholder="Search for an Artist, Song, or Album" />

											</div>
                                            <div class="12u$">
												<ul class="actions">
													<li><input type="submit" value="Search" class="special" /></li>
                                                </ul>
                                            </div>
                                    </div>
                                </form></p>
    						</header>
    						<section class="wrapper style5">
    							<div class="inner">
    <!---<div class="table-wrapper"> -->
        <table class="alt">
            <thead>
                <tr>
                    <th>Album Cover</th>
                    <th>Name</th>
                    <th>Album</th>\
                    <th>Artists</th>
                    <th>Preview</th>
                    <th>Vote</th>
                </tr>
            </thead>
            <tbody>
    '''
    try:
        url ="https://api.spotify.com/v1/search?query="+request.args.get('search')+"&offset=0&limit=25&type=track".replace(' ','%20')
        f = urllib.urlopen(url);
        Datadict = json.loads(f.read())
        tot = "List of tracks\n"
        for item in Datadict['tracks']['items']:
            preview = item['preview_url']
            name = item['name']
            album = item['album']['name']
            albumart = item['album']['images'][1]['url']
            artists = ''
            for artist in item['artists']:
                artists += artist['name']+", "
            artists = artists[:-2]
            Id = item['id']
            html += "<tr><td><image src="+albumart+' height="100" width="100"/></td><td>'+name+"</td><td>"+album+"</td><td>"+artists+'</td><td><audio controls><source src="'+preview+'" type="audio/mpeg"></td><td><a href="/done?id='+Id+'" class="button fit">done</a></td><td><a href="/nodo?id='+Id+'" class="button fit">No Do</a></td></tr>'
            tot+="\nTrack Name: "+name+"\nalbum name: "+album+'\nalbum art: <img src="'+albumart+'"/>\nartists: '+artists+"\nId: "+Id+"\n"
        html += '''
        </tbody>
    </table>
    </div>
    </div>
    </section>
    </article>

    <!-- Footer -->
    <footer id="footer">
    <ul class="icons">
    <li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
    <li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
    <li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
    <li><a href="#" class="icon fa-dribbble"><span class="label">Dribbble</span></a></li>
    <li><a href="#" class="icon fa-envelope-o"><span class="label">Email</span></a></li>
    </ul>
    <ul class="copyright">
    <li>&copy; Untitled</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li>
    </ul>
    </footer>

    </div>

    <!-- Scripts -->
    <script src="aep000.neocities.org/assets/js/jquery.min.js"></script>
    <script src="aep000.neocities.org/assets/js/jquery.scrollex.min.js"></script>
    <script src="aep000.neocities.org/assets/js/jquery.scrolly.min.js"></script>
    <script src="aep000.neocities.org/assets/js/skel.min.js"></script>
    <script src="aep000.neocities.org/assets/js/util.js"></script>
    <!--[if lte IE 8]><script src="aep000.neocities.org/assets/js/ie/respond.min.js"></script><![endif]-->
    <script src="aep000.neocities.org/assets/js/main.js"></script>

    </body>
    </html>
        '''

        return html
    except:
        return html
@app.route('/search', methods=['GET', 'POST'])
def hello():
    html ='''
    <!DOCTYPE HTML>
    <!--
    	Spectral by HTML5 UP
    	html5up.net | @n33co
    	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
    -->
    <html>
    	<head>
    		<title>Monsterlyrics</title>
    		<meta charset="utf-8" />
    		<meta name="viewport" content="width=device-width, initial-scale=1" />
                <script src="aep000.neocities.org/assets/js/jquery.min.js"></script>
                <script src="aep000.neocities.org/assets/js/jquery.scrollex.min.js"></script>
                <script src="aep000.neocities.org/assets/js/jquery.scrolly.min.js"></script>
                <script src="aep000.neocities.org/assets/js/skel.min.js"></script>
                <script src="aep000.neocities.org/assets/js/util.js"></script>
                <!--[if lte IE 8]><script src="aep000.neocities.org/assets/js/ie/respond.min.js"></script><![endif]-->
                <script src="aep000.neocities.org/assets/js/main.js"></script>
    		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
    		<link rel="stylesheet" href="https://aep000.neocities.org/assets/css/main.css" />
    		<!--[if lte IE 8]><link rel="stylesheet" href="aep000.neocities.org/assets/css/ie8.css" /><![endif]-->
    		<!--[if lte IE 9]><link rel="stylesheet" href="aep000.neocities.org/assets/css/ie9.css" /><![endif]-->
    	</head>
    	<body>

    		<!-- Page Wrapper -->
    			<div id="page-wrapper">

    				<!-- Header -->
    					<header id="header">
    						<h1><a href="/">Monsterlyrics</a></h1>
    						<nav id="nav">
    							<ul>
    								<li class="special">
    									<a href="#menu" class="menuToggle"><span>Menu</span></a>
    									<div id="menu">
    										<ul>
    											<li><a href="index.html">Home</a></li>
    											<li><a href="generic.html">Generic</a></li>
    											<li><a href="elements.html">Elements</a></li>
    											<li><a href="#">Sign Up</a></li>
    											<li><a href="#">Log In</a></li>
    										</ul>
    									</div>
    								</li>
    							</ul>
    						</nav>
    					</header>

    				<!-- Main -->
    					<article id="main">
    						<header>
    							<h2>Search</h2>
    							<p><form method="get" action="/search">
										<div class="row uniform">
											<div class="12u$">
												<input type="text" name="search" id="demo-name" value="" placeholder="Search for an Artist, Song, or Album" />

											</div>
                                            <div class="12u$">
												<ul class="actions">
													<li><input type="submit" value="Search" class="special" /></li>
                                                </ul>
                                            </div>
                                    </div>
                                </form></p>
    						</header>
    						<section class="wrapper style5">
    							<div class="inner">
    <!---<div class="table-wrapper"> -->
        <table class="alt">
            <thead>
                <tr>
                    <th>Album Cover</th>
                    <th>Name</th>
                    <th>Album</th>\
                    <th>Artists</th>
                    <th>Preview</th>
                    <th>Vote</th>
                </tr>
            </thead>
            <tbody>
    '''
    try:
        url ="https://api.spotify.com/v1/search?query="+request.args.get('search')+"&offset=0&limit=25&type=track".replace(' ','%20')
        f = urllib.urlopen(url);
        Datadict = json.loads(f.read())
        tot = "List of tracks\n"
        for item in Datadict['tracks']['items']:
            preview = item['preview_url']
            name = item['name']
            album = item['album']['name']
            albumart = item['album']['images'][1]['url']
            artists = ''
            for artist in item['artists']:
                artists += artist['name']+", "
            artists = artists[:-2]
            Id = item['id']
            html += "<tr><td><image src="+albumart+' height="100" width="100"/></td><td>'+name+"</td><td>"+album+"</td><td>"+artists+'</td><td><audio controls><source src="'+preview+'" type="audio/mpeg"></td><td><a href="/vote?id='+Id+'" class="button fit">Vote</a></td></tr>'
            tot+="\nTrack Name: "+name+"\nalbum name: "+album+'\nalbum art: <img src="'+albumart+'"/>\nartists: '+artists+"\nId: "+Id+"\n"
        html += '''
        </tbody>
    </table>
    </div>
    </div>
    </section>
    </article>

    <!-- Footer -->
    <footer id="footer">
    <ul class="icons">
    <li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
    <li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
    <li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
    <li><a href="#" class="icon fa-dribbble"><span class="label">Dribbble</span></a></li>
    <li><a href="#" class="icon fa-envelope-o"><span class="label">Email</span></a></li>
    </ul>
    <ul class="copyright">
    <li>&copy; Untitled</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li>
    </ul>
    </footer>

    </div>

    <!-- Scripts -->
    <script src="aep000.neocities.org/assets/js/jquery.min.js"></script>
    <script src="aep000.neocities.org/assets/js/jquery.scrollex.min.js"></script>
    <script src="aep000.neocities.org/assets/js/jquery.scrolly.min.js"></script>
    <script src="aep000.neocities.org/assets/js/skel.min.js"></script>
    <script src="aep000.neocities.org/assets/js/util.js"></script>
    <!--[if lte IE 8]><script src="aep000.neocities.org/assets/js/ie/respond.min.js"></script><![endif]-->
    <script src="aep000.neocities.org/assets/js/main.js"></script>

    </body>
    </html>
        '''

        return html
    except:
        return html
@app.route("/done", methods=['GET', 'POST'])
def setDone():
    songID = request.args.get('id')
    html = '''

    <html>
    <head>
    </head>
    <body>
    <form action="done2" method="get">
  ENTER URL: <input type="text" name="uri"><br>
  <input type="hidden" name="id" value="'''+songID+'''">
  <input type="submit" value="Submit">
  </form>
    </body>
    '''
    return html
@app.route("/done2", methods=['GET', 'POST'])
def setDone2():
    songID = request.args.get('id')
    url = request.args.get('uri')
    query = "INSERT INTO done (songid, url) VALUES ('"+songID+"', '"+url+"')"
    dbinsert(query)
    return redirect("/dashboard", code=302)
@app.route("/nodo", methods=['GET', 'POST'])
def setnodo():
    songID = request.args.get('id')
    query = "INSERT INTO nodo (songid) VALUES ('"+songID+"')"
    dbinsert(query)
    return redirect("/dashboard", code=302)
@app.route("/vote", methods=['GET', 'POST'])
def storeData():
    redir ="/cast"
    songID = request.args.get('id')
    query = "SELECT * FROM done WHERE songid = '"+songID+"'"
    query1 = "SELECT * FROM nodo WHERE songid = '"+songID+"'"
    if songExists(songID,query):
        redir +="?done=1&SID="+songID+"&nodo=0"
    elif songExists(songID,query1):
        redir +="?done=0&SID="+songID+"&nodo=1"
    else:
        redir +="?done=0&SID="+songID+"&nodo=0"
        query = "SELECT * FROM votes WHERE songid = '"+songID+"'"
        if songExists(songID,query):
            query = "UPDATE votes SET votes = votes + 1 WHERE songID = '"+songID+"'";
            dbinsert(query)
        else:
            query = "INSERT INTO votes (songid, votes) VALUES ('"+songID+"',1)"
            dbinsert(query)

    return redirect(redir, code=302)
@app.route("/cast", methods=['GET', 'POST'])
def cast():
    songID = request.args.get('SID')
    done = request.args.get('done')
    nodo = request.args.get('nodo')
    if done == '1':
        query = "SELECT * FROM done WHERE songid = '"+songID+"'"
        retval = dbquery(query)
        url=""
        for row in retval:
            url = row[1]
        html = '''
        <!DOCTYPE HTML>
        <!--
        	Spectral by HTML5 UP
        	html5up.net | @n33co
        	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
        -->
        <html>
        	<head>
        		<title>Generic - Spectral by HTML5 UP</title>
        		<meta charset="utf-8" />
        		<meta name="viewport" content="width=device-width, initial-scale=1" />
        		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
        		<link rel="stylesheet" href="http://aep000.neocities.org/assets/css/main.css" />
        		<!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
        		<!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
        	</head>
        	<body>

        		<!-- Page Wrapper -->
        			<div id="page-wrapper">

        				<!-- Header -->
        					<header id="header">
        						<h1><a href="index.html">Spectral</a></h1>
        						<nav id="nav">
        							<ul>
        								<li class="special">
        									<a href="#menu" class="menuToggle"><span>Menu</span></a>
        									<div id="menu">
        										<ul>
        											<li><a href="index.html">Home</a></li>
        											<li><a href="generic.html">Generic</a></li>
        											<li><a href="elements.html">Elements</a></li>
        											<li><a href="#">Sign Up</a></li>
        											<li><a href="#">Log In</a></li>
        										</ul>
        									</div>
        								</li>
        							</ul>
        						</nav>
        					</header>

        				<!-- Main -->
        					<article id="main">
        						<header>
        							<h2>THIS SONG HAS ALREADY BEEN DONE</h2>
        							<a href = "'''+url+'''"><p>CLICK HERE TO SEE IT</p></a>
        						</header>
        					</article>

        				<!-- Footer -->
        					<footer id="footer">
        						<ul class="icons">
        							<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
        							<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
        							<li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
        							<li><a href="#" class="icon fa-dribbble"><span class="label">Dribbble</span></a></li>
        							<li><a href="#" class="icon fa-envelope-o"><span class="label">Email</span></a></li>
        						</ul>
        						<ul class="copyright">
        							<li>&copy; Untitled</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li>
        						</ul>
        					</footer>

        			</div>

        		<!-- Scripts -->
        			<script src="http://aep000.neocities.org/assets/js/jquery.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/jquery.scrollex.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/jquery.scrolly.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/skel.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/util.js"></script>
        			<!--[if lte IE 8]><script src="http://aep000.neocities.org/assets/js/ie/respond.min.js"></script><![endif]-->
        			<script src="http://aep000.neocities.org/assets/js/main.js"></script>

        	</body>
        </html>
        '''
    elif nodo == '1':
        html = '''
        <!DOCTYPE HTML>
        <!--
        	Spectral by HTML5 UP
        	html5up.net | @n33co
        	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
        -->
        <html>
        	<head>
        		<title>Generic - Spectral by HTML5 UP</title>
        		<meta charset="utf-8" />
        		<meta name="viewport" content="width=device-width, initial-scale=1" />
        		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
        		<link rel="stylesheet" href="http://aep000.neocities.org/assets/css/main.css" />
        		<!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
        		<!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
        	</head>
        	<body>

        		<!-- Page Wrapper -->
        			<div id="page-wrapper">

        				<!-- Header -->
        					<header id="header">
        						<h1><a href="index.html">Spectral</a></h1>
        						<nav id="nav">
        							<ul>
        								<li class="special">
        									<a href="#menu" class="menuToggle"><span>Menu</span></a>
        									<div id="menu">
        										<ul>
        											<li><a href="index.html">Home</a></li>
        											<li><a href="generic.html">Generic</a></li>
        											<li><a href="elements.html">Elements</a></li>
        											<li><a href="#">Sign Up</a></li>
        											<li><a href="#">Log In</a></li>
        										</ul>
        									</div>
        								</li>
        							</ul>
        						</nav>
        					</header>

        				<!-- Main -->
        					<article id="main">
        						<header>
        							<h2>SORRY WE ARE NOT GOING TO DO THIS ONE</h2>
        							<a href = "/"><p>CLICK HERE TO RETURN TO THE HOMEPAGE</p></a>
        						</header>
        					</article>

        				<!-- Footer -->
        					<footer id="footer">
        						<ul class="icons">
        							<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
        							<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
        							<li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
        							<li><a href="#" class="icon fa-dribbble"><span class="label">Dribbble</span></a></li>
        							<li><a href="#" class="icon fa-envelope-o"><span class="label">Email</span></a></li>
        						</ul>
        						<ul class="copyright">
        							<li>&copy; Untitled</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li>
        						</ul>
        					</footer>

        			</div>

        		<!-- Scripts -->
        			<script src="http://aep000.neocities.org/assets/js/jquery.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/jquery.scrollex.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/jquery.scrolly.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/skel.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/util.js"></script>
        			<!--[if lte IE 8]><script src="http://aep000.neocities.org/assets/js/ie/respond.min.js"></script><![endif]-->
        			<script src="http://aep000.neocities.org/assets/js/main.js"></script>

        	</body>
        </html>
        '''
    else:
        html = '''
        <!DOCTYPE HTML>
        <!--
        	Spectral by HTML5 UP
        	html5up.net | @n33co
        	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
        -->
        <html>
        	<head>
        		<title>Generic - Spectral by HTML5 UP</title>
        		<meta charset="utf-8" />
        		<meta name="viewport" content="width=device-width, initial-scale=1" />
        		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
        		<link rel="stylesheet" href="http://aep000.neocities.org/assets/css/main.css" />
        		<!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
        		<!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
        	</head>
        	<body>

        		<!-- Page Wrapper -->
        			<div id="page-wrapper">

        				<!-- Header -->
        					<header id="header">
        						<h1><a href="index.html">Spectral</a></h1>
        						<nav id="nav">
        							<ul>
        								<li class="special">
        									<a href="#menu" class="menuToggle"><span>Menu</span></a>
        									<div id="menu">
        										<ul>
        											<li><a href="index.html">Home</a></li>
        											<li><a href="generic.html">Generic</a></li>
        											<li><a href="elements.html">Elements</a></li>
        											<li><a href="#">Sign Up</a></li>
        											<li><a href="#">Log In</a></li>
        										</ul>
        									</div>
        								</li>
        							</ul>
        						</nav>
        					</header>

        				<!-- Main -->
        					<article id="main">
        						<header>
        							<h2>YOUR VOTE HAS BEEN PROCESSED</h2>
        							<a href = "/"><p>CLICK HERE TO RETURN TO THE HOMEPAGE</p></a>
        						</header>
        					</article>

        				<!-- Footer -->
        					<footer id="footer">
        						<ul class="icons">
        							<li><a href="#" class="icon fa-twitter"><span class="label">Twitter</span></a></li>
        							<li><a href="#" class="icon fa-facebook"><span class="label">Facebook</span></a></li>
        							<li><a href="#" class="icon fa-instagram"><span class="label">Instagram</span></a></li>
        							<li><a href="#" class="icon fa-dribbble"><span class="label">Dribbble</span></a></li>
        							<li><a href="#" class="icon fa-envelope-o"><span class="label">Email</span></a></li>
        						</ul>
        						<ul class="copyright">
        							<li>&copy; Untitled</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li>
        						</ul>
        					</footer>

        			</div>

        		<!-- Scripts -->
        			<script src="http://aep000.neocities.org/assets/js/jquery.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/jquery.scrollex.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/jquery.scrolly.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/skel.min.js"></script>
        			<script src="http://aep000.neocities.org/assets/js/util.js"></script>
        			<!--[if lte IE 8]><script src="http://aep000.neocities.org/assets/js/ie/respond.min.js"></script><![endif]-->
        			<script src="http://aep000.neocities.org/assets/js/main.js"></script>

        	</body>
        </html>
        '''
    return html



#('Username', 'Password')

if __name__=="__main__":
    app.debug = True
    app.run()
