from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
#My sql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'crudflask'
mysql = MySQL(app)
#Settings
app.secret_key = 'mysecretkey'
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM  contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',(fullname, phone, email)) 
        mysql.connection.commit()
        flash('Contact add succesfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE contacts
                    SET fullname = %s, 
                        email = %s,
                        phone = %s
                        WHERE id = %s
                        """,(fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contact update Succesfully')
        return redirect(url_for('Index'))
    
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact remove succesfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
    
