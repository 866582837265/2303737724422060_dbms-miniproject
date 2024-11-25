from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'varsha'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'eventt'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/event', methods=['GET', 'POST'])
def event():
    search_results = None
    if request.method == "POST":
        search_term = request.form['search_eventid']
        cur = mysql.connection.cursor()
        query = "SELECT * FROM event_details WHERE eventid LIKE %s"
        cur.execute(query, ('%' + search_term + '%',))
        search_results = cur.fetchall()
        cur.close()
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM event_details")
        search_results = cur.fetchall()
        cur.close()
    return render_template('event.html', event=search_results)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        eventid_data = request.form['eventid']
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        venue = request.form['venue']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO event_details (eventid, name, date, time, venue) VALUES (%s, %s, %s, %s, %s)",
                    (eventid_data, name, date, time, venue))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('event'))
    return render_template('add.html')

@app.route('/delete/<string:eventid_data>', methods=['GET'])
def delete(eventid_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM event_details WHERE eventid = %s", (eventid_data,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('event'))

@app.route('/edit/<string:eventid_data>', methods=['GET', 'POST'])
def edit(eventid_data):
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM event_details WHERE eventid = %s", (eventid_data,))
        event_data = cur.fetchone()
        cur.close()
        return render_template('edit.html', event=event_data)

    if request.method == 'POST':
        eventid_data = request.form['eventid']
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        venue = request.form['venue']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE event_details 
            SET name = %s, date = %s, time = %s, venue = %s 
            WHERE eventid = %s
        """, (name, date, time, venue, eventid_data))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('event'))

if __name__ == "__main__":
    app.run(debug=True)
