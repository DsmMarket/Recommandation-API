from flask import Flask
from flaskext.mysql import MySQL
from creatdata import CreateData

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'planB'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_HOST'] = '52.78.148.203'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

Model = CreateData(cursor)