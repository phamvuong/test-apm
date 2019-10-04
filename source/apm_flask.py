import sqlite3, requests, time, logging, random
from flask import Flask, jsonify
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import LoggingHandler

names = ['ruan', 'stefan', 'philip', 'norman', 'frank', 'pete', 'johnny', 'peter', 'adam']
cities = ['cape town', 'johannesburg', 'pretoria', 'dublin', 'kroonstad', 'bloemfontein', 'port elizabeth', 'auckland', 'sydney']
lastnames = ['smith', 'bekker', 'admams', 'phillips', 'james', 'adamson']

conn = sqlite3.connect('database.db')
conn.execute('CREATE TABLE IF NOT EXISTS people (name STRING, age INTEGER, surname STRING, city STRING)')
#sqlquery_write = conn.execute('INSERT INTO people VALUES("{}", "{}", "{}", "{}")'.format(random.choice(names), random.randint(18,40), random.choice(lastnames), random.choice(cities)))
seconds = [0.002, 0.003, 0.004, 0.01, 0.3, 0.2, 0.009, 0.015, 0.02, 0.225, 0.009, 0.001, 0.25, 0.030, 0.018]

app = Flask(__name__)
apm = ElasticAPM(app, server_url='http://localhost:8200', service_name='my-app-01', logging=False)

@app.route('/')
def index():
    return jsonify({"message": "response ok"})

@app.route('/delay')
def delay():
    time.sleep(random.choice(seconds))
    return jsonify({"message": "response delay"})

@app.route('/upstream')
def upstream():
    r = requests.get('http://localhost:5001').json()
    r.get('country')
    if r.get('country') == 'italy':
        return 'Italalia!', 200
    elif r.get('country') == 'canada':
        return 'Canada!', 502
    else:
        return 'Not Found', 404

@app.route('/5xx')
def fail_with_5xx():
    value = 'a' + 1
    return jsonify({"message": value})

@app.route('/sql-write')
def sqlw():
    conn = sqlite3.connect('database.db')
    conn.execute('INSERT INTO people VALUES("{}", "{}", "{}", "{}")'.format(random.choice(names), random.randint(18,40), random.choice(lastnames), random.choice(cities)))
    conn.execute('INSERT INTO people VALUES("{}", "{}", "{}", "{}")'.format(random.choice(names), random.randint(18,40), random.choice(lastnames), random.choice(cities)))
    conn.execute('INSERT INTO people VALUES("{}", "{}", "{}", "{}")'.format(random.choice(names), random.randint(18,40), random.choice(lastnames), random.choice(cities)))
    conn.execute('INSERT INTO people VALUES("{}", "{}", "{}", "{}")'.format(random.choice(names), random.randint(18,40), random.choice(lastnames), random.choice(cities)))
    conn.execute('INSERT INTO people VALUES("{}", "{}", "{}", "{}")'.format(random.choice(names), random.randint(18,40), random.choice(lastnames), random.choice(cities)))
    conn.commit()
    conn.close()
    return 'ok', 200

@app.route('/sql-read')
def sqlr():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('select * from people')
    rows = cur.fetchall()
    conn.close()
    return 'ok', 200

@app.route('/sql-group')
def slqg():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('select count(*) as num, city from people group by city')
    rows = cur.fetchall()
    conn.close()
    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
