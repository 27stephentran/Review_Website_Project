from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']

        if action == 'login':
            # Handle login
            pass
        elif action == 'register':
            return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/register')
def register():
    return "Registration Page (To be implemented)"

if __name__ == '__main__':
    app.run(debug=True)