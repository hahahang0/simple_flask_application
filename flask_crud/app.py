from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
from config import Config
import MySQLdb

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/users',methods=["GET"])
def get_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        return jsonify({"users":users,"message" : "Users Fetched Successfully"})
    except Exception as e:
        return jsonify({'error' : str(e)}),500
    
@app.route("/users/<int:user_id>",methods=["GET"])
def get_user(user_id):
    try:
        curr = mysql.connection.cursor()
        curr.execute("Select * from users where id = %s",(user_id,))
        user = curr.fetchone()
        curr.close()
        if user: 
            return jsonify({'user' : user,'message' : "User fetched successfully."})
        return jsonify({"message" : "User not found"}),404
    except Exception as e:
        return jsonify({'error' : str(e)}),500
    
@app.route('/users',methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data["name"]
        email = data["email"]

        curr = mysql.connection.cursor()
        curr.execute(
            "INSERT INTO users(name,email) VALUES (%s,%s)",(name,email)
        )
        mysql.connection.commit()
        user_id = curr.lastrowid
        curr.close()

        return jsonify({
            'id' : user_id,
            'name' : name,
            'email' : email,
            'message' : "User created successfully"
        }),201
    except MySQLdb.IntegrityError:
        return jsonify({'error' : "Email already exists"}),400
    except Exception as e :
        return jsonify({'error':str(e)}),500

@app.route('/users/<int:user_id>',methods=["PUT"])
def update_user(user_id):
    try:
        print(f'user_id type: {type(user_id)}')

        data = request.get_json()
        name = data['name']
        email = data["email"]
        

        curr = mysql.connection.cursor()
        curr.execute("UPDATE users SET name = %s,email = %s WHERE id = %s",(name,email,(user_id)))
        mysql.connection.commit()
        affected_rows = curr.rowcount
        curr.close()

        if affected_rows == 0:
            return jsonify({"message" : "User not found"}),404
        return jsonify({
            "id" : user_id,
            "name" : name,
            "email" : email,
            "message" : "User updated successfully"
        })
    except MySQLdb.IntegrityError:
        return jsonify({"error" : "Email already exists"}),400
    except Exception as e:
        return jsonify({'error': str(e)}),500
    

@app.route('/users/<int:user_id>',methods=["DELETE"])
def delete_user(user_id):
    try:
        print(f'user_id type: {type(user_id)}')

        cur = mysql.connection.cursor()
        # cur.execute("DELETE FROM users WHERE id = %s",(user_id,))
        # mysql.connection.commit()
        # affected_rows = cur.rowcount
        # cur.close()
        print(f'user_id type: {type(user_id)}')

        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()   
        affected_rows = cur.rowcount
        cur.close()
        
        if affected_rows == 0:
            return jsonify({"message" : "User not found"}),404
        return jsonify({'message' : 'User deleted successfully'})
    
    except Exception as e:
        return jsonify({"error" : str(e)}),500
    

# @app.route('/users/<int:user_id>', methods=["DELETE"])
# def delete_user(user_id):
#     try:
#         # Verify database connection
#         if not mysql.connection:
#             return jsonify({"error": "Database connection failed"}), 500

#         cur = mysql.connection.cursor()
        
#         # Check if user exists first
#         cur.execute("SELECT id FROM users WHERE id = %s", (user_id,))
#         if not cur.fetchone():
#             cur.close()
#             return jsonify({"message": "User not found"}), 404
        
#         # Delete the user
#         cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
#         mysql.connection.commit()
#         affected_rows = cur.rowcount
#         cur.close()
        
#         return jsonify({'message': 'User deleted successfully'})
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)