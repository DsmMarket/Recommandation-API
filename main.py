from flaskext.mysql import MySQL
from createdata import Data
from createmodel import Model
from flask import Flask, request, make_response
from json import dumps

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'planB'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_HOST'] = '52.78.148.203'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

data = Data(cursor)
model = Model(data)

rentrecommenditems = [model.recommend(i, 'rent') for i in range(data.n_users_rent)]
dealrecommenditems = [model.recommend(i, 'deal') for i in range(data.n_users_deal)]

@app.route('/recommend', methods=['GET'])
def recommend():
    userId = request.args.get('userId', type=int)
    rentordeal = request.args.get('rentordeal', type=int)

    if rentordeal == 0:
        recommenditems = dealrecommenditems[userId]
    elif rentordeal == 1:
        recommenditems = rentrecommenditems[userId]
    else:
        raise ValueError

    return make_response(dumps(str(recommenditems)))

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Exception: %s', (e))
    return 'Exception: ' + str(e)

app.run(port=1937)