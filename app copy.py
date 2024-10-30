
from datetime import datetime, timedelta
from flask import Flask, json, make_response, redirect, render_template, request, url_for, g
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

g.user = {}

@app.before_request
def before_request():
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")
    cur.execute("SET lc_time_names = 'pt_BR'")
    cur.close()

    cookie = request.cookies.get('user_data')

    if cookie == None:
        return redirect(f"{url_for('login')}")

    user = json.loads(cookie)
    user['fname'] = user['name'].split()[0]

@app.route('/')
def home():

    sql = '''
        SELECT *
        FROM Trecos
        WHERE
        user_id = %s
        AND status != 'del'
        ORDER BY data DESC;
        '''

    cur = mysql.connection.cursor()
    cur.execute(sql, (user['id'],))
    trecos = cur.fetchall()
    cur.close()

    return render_template('home.html', trecos=trecos, user=user)

@app.route('/login', methods=['GET', 'POST'])

def login():

    error = ''

    if request.method == 'POST':

        form = dict(request.form)

        print('\n\n\n', form, '\n\n\n')
        
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

        print('\n\n\n', user, '\n\n\n')

        if user != None:
            resp = make_response(redirect(url_for('home')))
            cookie_data = {
            'id': user['id'],
            'name': user['nome']
            }

            print('\n\n\nCookie:', cookie_data, '\n\n\n')
            # Data em que o cookie espira
            expires = datetime.now() + timedelta(days=365)
            # Adiciona o cookie à página
            resp.set_cookie('user_data', json.dumps(
                cookie_data), expires=expires)
            
            return resp

        else:
            error = 'Login e/ou senha errados!'

    return render_template('login.html', error=error)

@app.route('/new', methods=['GET', 'POST'])
def new():

    return render_template('new.html')

if __name__ == '__main__':
    app.run(debug=True)
