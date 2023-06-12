from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# MySQL Connection
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flask_db'
mysql = MySQL(app)

# Settings
app.secret_key = 'l_-2oidvsw6#z_w_t&y(d!v7q8ra4*1qzmrz7iv&zqp!46aizq'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM user')
    data = cur.fetchall()
    return render_template('index.html', users = data)

@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (full_name, phone, email) VALUES (%s, %s, %s)", (fullname, phone, email))
        mysql.connection.commit()
        flash('User added successfully')
        
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def get_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE id_user = %s", (id))
    data = cur.fetchall()
    
    return render_template('update.html', user = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_user(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE user
                    SET full_name = %s,
                        phone = %s,
                        email = %s
                    WHERE id_user = %s
                    """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash("User updated successfully")
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM user WHERE id_user = {0}'.format(id))
    mysql.connection.commit()
    flash('User removed successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)