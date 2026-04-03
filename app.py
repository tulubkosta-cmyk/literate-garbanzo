import json
import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_users():
    if not os.path.exists('users.json'):
        return {}
    with open('users.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index_logged_in.html', username=session['username'])
    else:
        return render_template('index.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/do_register', methods=['POST'])
def do_register():
    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    if not login or not password:
        return "Ошибка: логин и пароль не могут быть пустыми!"
    users = load_users()
    if login in users:
        return f"Ошибка: пользователь {login} уже существует!"
    users[login] = password
    save_users(users)
    return f"Регистрация успешна! <a href='{url_for('login_page')}'>Войти</a>"

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/do_login', methods=['POST'])
def do_login():
    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    users = load_users()
    if login in users and users[login] == password:
        session['username'] = login
        return redirect(url_for('account'))
    else:
        return "Неверный логин или пароль."

@app.route('/account')
def account():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('account.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) eyelashes
