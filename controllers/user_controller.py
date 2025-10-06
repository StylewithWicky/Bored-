from flask import Blueprint, request ,jsonify
from flask_jwt_extended import create_access_token
from datetime import datetime ,timedelta
from Models.user import User,db

auth_bp =Blueprint('auth_bp',__name__)

#The signup bit
@auth_bp.route('/signup',method =['POST'])
def signup():
    data=request.get_json()
    username=data.get('username')
    email=data.get('email')
    password=data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'The Email already exists, please try another'}),400
    if User.query.filter_by(username=username).first():
        return jsonify({"The Username already exists"}),400
    
    user=User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit

    
    return jsonify({"message": "User created successfully!"})

# Login Bit 
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    
    user.last_login = datetime.utcnow()
    db.session.commit()

    
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": access_token, "user": user.to_dict()})


