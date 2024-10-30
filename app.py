
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

    edit = request.args.get('edit')

    delete = request.args.get('delete')

    cookie = request.cookies.get('user_data')

    if cookie == None:
        return redirect(f"{url_for('login')}")
    
    user = json.loads(cookie)
    user['fname'] = user['name'].split()[0]

    sql = '''
        SELECT *
        FROM Trecos
        WHERE
        `user_id` = %s
        AND `status` != 'del'
        ORDER BY data DESC;
        '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (user['id'],))
    trecos = cur.fetchall()
    cur.close()

    return render_template('home.html', trecos=trecos, user=user, edit=edit, delete=delete)

@app.route('/login', methods=['GET', 'POST'])

def login():

    error = ''

    if request.method == 'POST':

        form = dict(request.form)
        
        sql = '''
        SELECT `id`, `nome`
        FROM Users
        WHERE `email` = %s
        AND `senha` = SHA1(%s)
        AND `status` = 'on';
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

    sucess = False

    cookie = request.cookies.get('user_data')

    if cookie == None:
        return redirect(f"{url_for('login')}")

    user = json.loads(cookie)
    user['fname'] = user['name'].split()[0]

    if request.method == 'POST':
        form = dict(request.form)

        sql = '''
        INSERT INTO trecos (
        `user_id`,
        `nome`,
        `foto`,
        `descricao`,
        `localizacao`
        ) VALUES (
            %s, %s, %s, %s, %s)
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (user['id'], form['nome'], form['foto'], form['descricao'], form['localizacao'],))
        mysql.connection.commit()
        cur.close()

        sucess = True

    return render_template('new.html', user=user, sucess=sucess)

@app.route('/view/<id>')
def view(id):

    cookie = request.cookies.get('user_data')

    if cookie == None:
        return redirect(f"{url_for('login')}")

    user = json.loads(cookie)
    user['fname'] = user['name'].split()[0]

    sql = '''
        SELECT `id`, `data`, `foto`, `nome`, `descricao`, `localizacao`
        FROM Trecos
        WHERE `status` = 'on' AND `user_id` = %s
        '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (user['id'],))
    treco = cur.fetchone()
    cur.close()

    return render_template('view.html', treco=treco, user=user)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):

    cookie = request.cookies.get('user_data')

    if cookie == None:
        return redirect(f"{url_for('login')}")

    user = json.loads(cookie)
    user['fname'] = user['name'].split()[0]

    if request.method == 'POST':

        form = dict(request.form)

        sql = '''
            UPDATE Trecos SET 
                foto = %s,
                nome = %s,
                descricao = %s,
                localizacao = %s
            WHERE status = 'on'
                AND user_id = %s
                AND id = %s
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (form['foto'], form['nome'], form['descricao'], form['localizacao'], user['id'], id,))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home', edit=True))

    sql = '''
        SELECT id, data, foto, nome, descricao, localizacao
        FROM Trecos
        WHERE status = 'on' AND user_id = %s AND id = %s
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (user['id'], id,))
    treco = cur.fetchone()
    cur.close()

    return render_template('edit.html', user=user, treco=treco)

@app.route('/delete/<id>')
def delete(id):

    cookie = request.cookies.get('user_data')
    if cookie == None:
        return redirect(url_for('login'))
    user = json.loads(cookie)
    user['fname'] = user['name'].split()[0]

    sql = '''
        UPDATE trecos SET
            status = 'del'
        WHERE user_id = %s
            AND id = %s
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (user['id'], id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('home', delete=True))

@app.route('/logout')
def logout():

    resp = make_response(redirect(url_for('login')))

    resp.set_cookie('user_data', '', expires=0)

    return resp
    

if __name__ == '__main__':
    app.run(debug=True)
