from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hello123@localhost/aution'
db = SQLAlchemy(app)

helper_table_User = db.Table('helper_table_User',
                             db.Column('user_id', db.Integer, db.ForeignKey('User.user_id ')),
                             db.Column('item_id', db.Integer, db.ForeignKey('Item.item_id'))
                             #db.UniqueConstraint('user_id', 'item_id', name='UC_user_id_item_id')
                             )
helper_table_Bid = db.Table('helper_table_Bid',
                            db.Column('bid_id', db.Integer, db.ForeignKey('Bid.bid_id')),
                            db.Column('item_id', db.Integer, db.ForeignKey('Item.item_id '))
                            #db.UniqueConstraint('bid_id', 'item_id', name='UC_bid_id_item_id')
                            )
class Item(db.Model):
    __tablename__ = 'Item'
    item_id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    User_id_rel = db.Column(db.Integer, db.ForeignKey('User.user_id'),nullable=False)
class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(40),nullable=False)
    item_ = db.relationship('Item', backref='User', lazy=True)
    #item_rela = db.relationship('Item', backref='User', lazy='dynamic')
    relation_bid = db.relationship("Bid",
                    secondary=helper_table_Bid)
class Bid(db.Model):
    __tablename__ = 'Bid'
    bid_id = db.Column(db.Integer,primary_key = True)
    price = db.Column(db.Float,nullable = False)
    relation_bid = db.relationship("Item",
                    secondary=helper_table_User)
db.create_all()
user1 = User(username = 'Dong',password = '123123')
item1 = Item(itemname = 'car',description = 'like new',pub_date = '19-5-2010')

#db.session.add(user1)
db.session.add(item1)
db.session.commit()    