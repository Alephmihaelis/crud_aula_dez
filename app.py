
from datetime import datetime, timedelta
from flask import Flask, json, make_response, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'trecosdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_USE_UNICODE'] = True
app.config['MYSQL_CHARSET'] = 'utf8mb4'

mysql = MySQL(app)

@app.before_request
def before_request():
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")
    cur.execute("SET lc_time_names = 'pt_BR'")
    cur.close()

@app.route('/')
def home():

    cookie = request.cookies.get('user_data')

    if cookie == None:
        return redirect(f"{url_for('login')}")

    user_id = '2'
    sql = '''
        SELECT *
        FROM Trecos
        WHERE
        id = %s
        AND status != 'del'
        ORDER BY data DESC;
            '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (user_id,))
    trecos = cur.fetchall()
    cur.close()

    return render_template('list.html', trecos=trecos)

@app.route('/login', methods=['GET', 'POST'])

def login():

    error = ''

    if request.method == 'POST':

        form = dict(request.form)
        
        sql = '''
        SELECT id, nome
        FROM Users
        WHERE email = %s
        AND senha = SHA1(%s)
        AND status = 'on';
        '''

        cur = mysql.connection.cursor()
        cur.execute(sql, (form['email'], form['password'], ))
        user = cur.fetchone()
        cur.close()

        if user != None:
            resp = make_response(redirect(url_for('home')))
            cookie_data = {
            'id': user['id'],
            'name': user['nome']
        }
        expires = datetime.now() + timedelta(day=365)
        resp.set_cookie('user_data', json.dumps(
            cookie_data), expires=expires)

        return resp

    else:
        error = 'Login e/ou senha errados!'

    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
