# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
import mariadb
import os
import re

app = Flask(__name__)

app.secret_key = 'secret'

UPLOAD_FOLDER = os.getcwd()
uid = 0;
userLogin = "";

@app.route('/')
	
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		#cursor = cur(MySQLdb.cursors.DictCursor)
		conn = connect()
		cur = conn.cursor()
		cur.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password, ))
		account = cur.fetchone()
		cur.close()
		conn.close()
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[1]
			global uid, userLogin
			uid = session['id']
			userLogin = session['username']
			return redirect(url_for('upload_file'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop(0, None)
	session.pop(1, None)
	session.pop(2, None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg=''	
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form  :
		username = request.form['username']
		password = request.form['password']
		conn = connect()
		cur = conn.cursor()
		cur.execute('SELECT * FROM user WHERE username = %s', (username, ))
		account = cur.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password :
			msg = 'Please fill out the form !'
		else:
			cur.execute('INSERT INTO user VALUES (NULL, %s, %s )', (username, password, ))
			conn.commit()
			msg = 'You have successfully registered !'
		cur.close()
		conn.close()
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
	msg = "login successfully" 
	file_path= '/app/static/upload/'+str(uid)+'/'
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file :
			filename = secure_filename(file.filename)
			if not os.path.exists(file_path+filename):
				app.config['UPLOAD_FOLDER'] = file_path
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				conn = connect()
				cur = conn.cursor()
				cur.execute('INSERT INTO file VALUES (NULL, %s, %s, %s, %s )', (uid, filename, file_path+filename, userLogin, ))
				conn.commit()
				msg = 'You have successfully uploaded!'
				cur.close()
				conn.close()
			else :
				msg = "upload failed! File exists."
		# return render_template('index.html', file=os.listdir(file_path), msg=msg)
	list_file = []
	list_file = sync_database( file_path, os.listdir(file_path) )
	# return redirect(url_for('sync_database'))
	return render_template('index.html', list_file=list_file, msg=msg)

def sync_database(file_path, file):
	list_file=[]
	conn = connect()
	cur = conn.cursor()
	for f in file: 
		#   cur.execute('SELECT * FROM user WHERE username = %s', (username, ))
		cur.execute('SELECT * FROM file WHERE file_path = %s', (file_path + f, )) 
		if (cur.fetchone()) == None :
			cur.execute('INSERT INTO file VALUES (NULL, %s, %s, %s, %s )', (uid, f, file_path+f, userLogin, ))
			conn.commit()
		
	cur.execute('SELECT * FROM file ORDER BY id ASC;')
	list_file=list(cur.fetchall())
	cur.close()
	conn.close()
	# return render_template('index.html', file=list_file)cur
	return list_file

@app.route('/app/static/upload/<uid>/<name>')
def download_file(name, uid):
    return send_from_directory('/app/static/upload/'+str(uid)+'/', name)

def connect():
	conn = mariadb.connect(
		host='localhost',
		port= 3306,
		user='root',
		password='a',
		database='flaskTest')
	return conn

