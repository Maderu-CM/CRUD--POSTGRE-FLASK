from flask import Flask, render_template, request, flash, redirect, url_for, get_flashed_messages
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "moyiaclivecode-backend"
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "AZiza@2812"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM students"
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('index.html', list_users=list_users)

@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        cur.execute("INSERT INTO students(fname, lname, email) VALUES (%s, %s, %s)", (fname, lname, email))
        conn.commit()
        flash('Student Added Successfully!')
        return redirect(url_for('Index'))
    

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_students(id):
    cur= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT *FROM students WHERE id=%s',(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html',student = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_student(id):
    
    if request.method == 'POST':
        fname= request.form['fname']
        lname= request.form['lname']
        email= request.form['email']

    cur= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        UPDATE students
        SET fname = %s,
            lname = %s,
            email = %s
                WHERE id= %s
                """,(fname,lname,email,id))
    flash ('Student Updated Successfully!')
    conn.commit()
    return redirect (url_for('Index')
 )

@app.route('/delete/<id>', methods=['DELETE'])
def delete_student(id):
    cur= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM students WHERE id = {0}'.format(id) )
    conn.commit()
    flash('Student Deleted Successfully!')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(debug=True)
