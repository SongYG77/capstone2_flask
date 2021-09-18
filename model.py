from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user_table"
    id_num = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    id = db.Column(db.String(32),unique=True)
    password = db.Column(db.String(32))
    name = db.Column(db.String(32))
    address = db.Column(db.String(100))
    sex = db.Column(db.String(10))
    start_date = db.Column(db.String(45))
    end_date = db.Column(db.String(45))
    enrollment = db.Column(db.String(45))
    gym = db.Column(db.String(45))


    def __init__(self,id,password,name,address,sex,start_date,end_date,enrollment, gym):
        self.id = id
        self.password = password
        self.name = name
        self.address = address
        self.sex = sex
        self.start_date = start_date
        self.end_date = end_date
        self.enrollment = enrollment
        self.gym = gym



class Bench(db.Model):
    __tablename__ = "bench"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.String(32))
    date = db.Column(db.String(32))
    start_time = db.Column(db.String(32))
    end_time = db.Column(db.String(32))

    def __init__(self,id,userid,date,start_time,end_time):
        self.id = id
        self.userid = userid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Reck(db.Model):
    __tablename__ = "reck"
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    userid = db.Column(db.String(32))
    date = db.Column(db.String(32))
    start_time = db.Column(db.String(32))
    end_time = db.Column(db.String(32))

    def __init__(self, userid, date, start_time, end_time):
        self.userid = userid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Aerobic(db.Model):
    __tablename__ = "aerobic"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.String(32))
    date = db.Column(db.String(32))
    start_time = db.Column(db.String(32))
    end_time = db.Column(db.String(32))

    def __init__(self, id, userid, date, start_time, end_time):
        self.id = id
        self.userid = userid
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

class Ptclass(db.Model):
    __tablename__ = "Ptclass"
    id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    userid = db.Column(db.String(32))
    date = db.Column(db.String(32))
    classinfo = db.Column(db.String(200))
    starttime = db.Column(db.String(32))
    teacher = db.Column(db.String(20))
    def __init__(self, id, userid, date, classinfo, starttime, teacher):
        self.id = id
        self.userid = userid
        self.date = date
        self.classinfo = classinfo
        self.starttime = starttime
        self.teacher = teacher


class Ptinfo(db.Model):
    __tablename__ = 'Ptinfo'
    id = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    equip = db.Column(db.String(32))
    set = db.Column(db.String(32))
    count = db.Column(db.String(32))
    Pt_key = db.Column(db.Integer, db.ForeignKey('Ptclass.id'))

    def __init__(self, id, equip, set, count, Pt_key):
        self.id = id
        self.equip = equip
        self.set = set
        self.count = count
        self.Pt_key = Pt_key

class Gym(db.Model) :
    __tablename__ = 'Gym'
    idGym = db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    name = db.Column(db.String(45))
    reck = db.Column(db.Integer)
    bench = db.Column(db.Integer)
    running = db.Column(db.Integer)
    leg_press = db.Column(db.Integer)
    long_pull = db.Column(db.Integer)

    def __init__(self, idGym, name, reck, bench, running, leg_press, long_pull):
        self.idGym = idGym
        self.name = name
        self.reck = reck
        self.bench = bench
        self.running = running
        self.leg_press = leg_press
        self.long_pull = long_pull


