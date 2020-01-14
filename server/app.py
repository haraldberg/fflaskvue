import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

mydb = mysql.connector.connect(
    user = '6PdyBLpTRC',
    passwd = 'LGEkXVEtHS',
    host = 'remotemysql.com',
    database = '6PdyBLpTRC',
)


def getUsers():
    cur = mydb.cursor(dictionary=True)
    cur.execute('''SELECT * FROM users''')
    rv = list(cur.fetchall())
    return rv

def getOrders(user_id):
    cur = mydb.cursor(dictionary=True)
    cur.execute('SELECT * FROM orders WHERE user_id=%s' % (user_id))
    # cur.execute('SELECT * FROM orders WHERE user_id=1')
    rv = list(cur.fetchall())
    return rv

def getScenes(order_id):
    cur = mydb.cursor(dictionary=True)
    cur.execute('SELECT * FROM scenes WHERE order_id=%s' % (order_id))
    rv = list(cur.fetchall())
    return rv

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/', methods=['GET'])
def getdata():
    cur = mydb.cursor(dictionary=True)
    cur.execute('''SELECT * FROM users''')
    rv = cur.fetchall()
    return jsonify(rv)


@app.route('/users', methods=['GET', 'POST'])
def all_users():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        cur = mydb.cursor(dictionary=True)
        cur.execute('INSERT INTO users(first_name, last_name, email, active) VALUES(%s, %s, %s, %s)', (post_data.get('first_name'), post_data.get('last_name'), post_data.get('email'), post_data.get('active')))
        mydb.commit()
        response_object['message'] = 'User added!'
    else:
        response_object['users'] = getUsers()
    return jsonify(response_object)


@app.route('/users/<user_id>', methods=['PUT', 'DELETE'])
def single_user(user_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        cur = mydb.cursor(dictionary=True)
        cur.execute('UPDATE users SET first_name=%s, last_name=%s, email=%s, active=%s WHERE id=%s', (post_data.get('first_name'), post_data.get('last_name'), post_data.get('email'), post_data.get('active'), user_id))
        mydb.commit()
        response_object['message'] = 'User updated!'
    if request.method == 'DELETE':
        cur = mydb.cursor(dictionary=True)
        cur.execute('DELETE FROM users WHERE id=%s' % (user_id))
        mydb.commit()
        response_object['message'] = 'User removed!'
    return jsonify(response_object)



# ------------------------- Orders -------------------------------------

@app.route('/orders/<user_id>', methods=['GET', 'POST'])
def all_orders(user_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        cur = mydb.cursor(dictionary=True)
        cur.execute('INSERT INTO orders(user_id, status) VALUES(%s, %s)', (user_id, post_data.get('status')))
        mydb.commit()
        response_object['message'] = 'Order added!'
    else:
        response_object['orders'] = getOrders(user_id)
    return jsonify(response_object)


@app.route('/orders/<order_id>', methods=['PUT', 'DELETE'])
def single_order(order_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        cur = mydb.cursor(dictionary=True)
        cur.execute('UPDATE orders SET status=%s WHERE id=%s', (post_data.get('status'), order_id))
        mydb.commit()
        response_object['message'] = 'Order updated!'
    if request.method == 'DELETE':
        cur = mydb.cursor(dictionary=True)
        cur.execute('DELETE FROM orders WHERE id=%s' % (order_id))
        mydb.commit()
        response_object['message'] = 'Order removed!'
    return jsonify(response_object)

#----------------------------- Scenes ------------------------------------------------

@app.route('/scenes/<order_id>', methods=['GET', 'POST'])
def all_scenes(order_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        cur = mydb.cursor(dictionary=True)
        cur.execute('INSERT INTO scenes(order_id, name, status, sensor) VALUES(%s, %s, %s, %s)', (order_id, post_data.get('name'), post_data.get('status'), post_data.get('sensor')))
        mydb.commit()
        response_object['message'] = 'Scene added!'
    else:
        response_object['scenes'] = getScenes(order_id)
    return jsonify(response_object)


@app.route('/scenes/<scene_id>', methods=['PUT', 'DELETE'])
def single_scene(scene_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        cur = mydb.cursor(dictionary=True)
        cur.execute('UPDATE scenes SET name=%s, status=%s, sensor=%s WHERE id=%s', (post_data.get('name'), post_data.get('status'), post_data.get('sensor'), scene_id))
        mydb.commit()
        response_object['message'] = 'Scene updated!'
    if request.method == 'DELETE':
        cur = mydb.cursor(dictionary=True)
        cur.execute('DELETE FROM scenes WHERE id=%s' % (scene_id))
        mydb.commit()
        response_object['message'] = 'Scene removed!'
    return jsonify(response_object)

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run()