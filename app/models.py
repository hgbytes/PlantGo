from app import db

class Disease(db.Model):
    """Model for plant disease information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    possible_steps = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Disease {self.name}>'

class Supplement(db.Model):
    """Model for supplement information related to plant diseases"""
    id = db.Column(db.Integer, primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    buy_link = db.Column(db.String(255), nullable=True)
    
    # Define relationship with Disease model
    disease = db.relationship('Disease', backref=db.backref('supplements', lazy=True))
    
    def __repr__(self):
        return f'<Supplement {self.name}>' 