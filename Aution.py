from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hello123@localhost/aution'
db = SQLAlchemy(app)
user_bid = db.Table('user_bid',
                    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id ')),
                    db.Column('bid_id', db.Integer, db.ForeignKey('bids.bid_id'))
)
bid_item = db.Table('bid_item',
                            db.Column('bid_id', db.Integer, db.ForeignKey('Bid.bid_id')),
                            db.Column('item_id', db.Integer, db.ForeignKey('Item.item_id '))
)

class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    Owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(40),nullable=False)
    items = db.relationship('Item', backref='Owner',lazy = 'dynamic')
    aution_item = db.relationship("Bid",secondary=user_bid,backref=db.backref('aution_for', lazy='dynamic'))
class Bid(db.Model):
    __tablename__ = 'bids'
    bid_id = db.Column(db.Integer,primary_key = True)
    price = db.Column(db.Float,nullable = False)
    aution_item = db.relationship("Item",secondary=bid_item,backref=db.backref('bid_for', lazy='dynamic'))
    
    
db.create_all()

user1 = User(username = 'Dong',password = '123123')
user2 = User(username = 'Khiet',password = '111111')
user3 = User(username = 'Hung',password = '222222')
item1 = Item(itemname = 'car',description = 'like new',pub_date = '19-5-2010',Owner = user1)
item2 = Item(itemname = 'cars',description = 'Toyota camry new',pub_date = '19-10-2010',Owner = user2)
item3 = Item(itemname = 'bike',description = 'sport bike',pub_date = '19-10-2010',Owner = user3)
item4 = Item(itemname = 'house',description = '100 m2 , with 5 rooms',pub_date = '19-10-2010',Owner = user1)
bid1 = Bid(price = 25000)

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.add(item1)
db.session.add(item2)
db.session.add(item3)
db.session.add(item4)
db.session.add(bid1)

bid1.aution_for.append(user1)

db.session.commit()    