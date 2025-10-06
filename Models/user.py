from datetime import datetime
from App import db,jwt
from werkzeug.security import generate_password_hash, check_password_hash

class User():
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password_hash =db.Column(db.String(120),unique=True,nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=None)
    is_verified = db.Column(db.Boolean, default=False)
    failed_logins = db.Column(db.Integer, default=0)


    def set_password(self,password):
        self.password_hash=generate_password_hash(password,method='pbkdf2:sha256',salt_length=20)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def to_dict(self):
        return{
            "id":self.id,
            "email":self.email,
            "password":self.password,
            "created_at":self.created_at.isoformat(),
            "last_login":self.last_login.isoformat() if self.last_login else None,
            "is_verified":self.is_verified

            
              }