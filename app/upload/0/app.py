from flask import abort, redirect, url_for, Flask

app = Flask(__name__)

@app.route('/')
def index():
    a =1 
    if a==1:
        return redirect(url_for('login23'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return "abc"

@app.route('/login2')
def login23():
    return "abc2"
        
if __name__ == '__main__': 
    app.run(debug=True)
