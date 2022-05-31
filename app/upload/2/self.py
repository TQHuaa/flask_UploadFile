from flask import Flask
import mariadb 

app = Flask(__name__)

def connect():
	return mariadb.connect(
		host = 'localhost',
		port = 3306,
		user = 'root',
		password = 'a',
		database= 'flaskTest'
	)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
	return render_template()
	
@app.route('/login', methods = ['GET', 'POST'])
def login():
	return
	
