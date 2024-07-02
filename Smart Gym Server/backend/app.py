from flask import Flask, request, jsonify
from db_handler import DBHandler

app = Flask(__name__)
db = DBHandler()

@app.route('/api/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    uuid = data.get('uuid')

    if not uuid:
        return jsonify({"error": "UUID is required"}), 400

    user = db.get_user_by_uuid(uuid)

    if user:
        user_data = {
            "id": user[0],
            "uuid": user[1],
            "name": user[2]
        }
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = data.get('user')
    
    if not user:
        return jsonify({"error": "User data is required"}), 400
    
    success = db.check_user_by_name(user)
    user_data = db.get_user_by_name(user)
    
    if success:
        return jsonify({"id": user_data[0], "uuid": user_data[1], "name": user_data[2], "success": True}), 200
    else:
        return jsonify({"error": "User not found", "success": False}), 404


@app.route('/api/workouts', methods=['GET'])
def get_workout():
    user = request.args.get('user')
    if not user:
        return jsonify({"error": "User is required"}), 400
    workout_data = db.get_workouts_by_user(user)
    response = []
    for workout in workout_data:
        response.append({
            "id": workout[0],
            "user_id": workout[1],
            "machine_id": workout[2],
            "date": workout[3],
            "repetitions": workout[4],
            "weight": workout[5],
            "duration": workout[6]
        })
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)