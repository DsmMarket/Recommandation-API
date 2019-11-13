from flaskext.mysql import MySQL
from createdata import Data
from createmodel import Model
from flask import Flask, request, make_response
import json
from collections import OrderedDict

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'planB'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_HOST'] = '13.209.76.210'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

data = Data(cursor)
model = Model(data)
rentitems = {v: k for k, v in data.lens_to_internal_rentitem_ids.items()}
dealitems = {v: k for k, v in data.lens_to_internal_dealitem_ids.items()}

rentrecommenditems = [model.recommend(i, 'rent') for i in range(data.n_users_rent)]
dealrecommenditems = [model.recommend(i, 'deal') for i in range(data.n_users_deal)]

@app.route('/recommend', methods=['GET'])
def recommend():
    userId = request.args.get('userId', type=int)
    Type = request.args.get('type', type=int)

    if Type == 0:
        recommenditems = list(map(lambda x: dealitems[x], dealrecommenditems[userId]))
    elif Type == 1:
        recommenditems = list(map(lambda x: rentitems[x], rentrecommenditems[userId]))
    else:
        raise ValueError
<<<<<<< HEAD
    data = list(map(str, recommenditems))
    return make_response(json.dumps(str(data)))
=======
    recommenditems = list(map(str, recommenditems))
    return make_response(dumps(recommenditems))
>>>>>>> 56f5ff385e979f3045c2cffe82f22aca59c7abac

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Exception: %s', (e))
    return 'Exception: ' + str(e)

<<<<<<< HEAD
app.run(host='0.0.0.0', port=1937)
=======
app.run(host='localhost', port=1937)
>>>>>>> 56f5ff385e979f3045c2cffe82f22aca59c7abac
