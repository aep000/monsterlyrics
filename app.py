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
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
@app.route('/', methods=['GET', 'POST'])
def index():
    f = open('index.html','r');
    return f.read()
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
    							<p><form method="get" action="/">
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
        Id = item['id']
        html += "<tr><td><image src="+albumart+" /></td><td>"+name+"</td><td>"+album+"</td><td>"+artists+'</td><td><audio controls><source src="'+preview+'" type="audio/mpeg"></td><td><a href="/vote?id='+Id+'" class="button fit">Vote</a></td></tr>'
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
def songExists(songID):
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
    cur.execute("SELECT * FROM votes WHERE songid = '"+songID+"'")
    return cur.fetchone() is not None
@app.route("/vote", methods=['GET', 'POST'])
def storeData():
    songID = request.args.get('id')
    query = "SELECT * FROM votes WHERE songid = '"+songID+"'"
    if songExists(songID):
        query = "UPDATE votes SET anthemid = anthemID + 1 WHERE songID = '"+songID+"'";
        dbinsert(query)
    else:
        query = "INSERT INTO votes (songid, votes) VALUES ('"+songID+"',1)"
        dbinsert(query)
    return "IT WORKED"




#('Username', 'Password')

if __name__=="__main__":
    app.debug = True
    app.run()
