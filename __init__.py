from model import db, User, Bench, Reck, Aerobic
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import schedule
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# background 방식으로 사용해야 start 이후 중지되지 않음
sched = BackgroundScheduler()


# 지금은 테스트를 위해 매 분 갱신 이후에는('cron', hour='0', minute='10', id='update_db') 0시 10분에 갱신되도록 바꿀 예정
@sched.scheduled_job('cron', hour='0', minute='10', id='update_db')
def update_db():
    # Bench.query.filter(datetime.datetime.strptime(Bench.date, "%Y-%m-%d").date() < datetime.date.today()).delete()
    # Reck.query.filter(datetime.datetime.strptime(Reck.date, "%Y-%m-%d").date() < datetime.date.today()).delete()
    # Aerobic.query.filter(datetime.datetime.strptime(Aerobic.date, "%Y-%m-%d").date() < datetime.date.today()).delete()
    db.session.commit()


# 스캐쥴링 시작. 실행되고 있는 동안 스캐쥴에 의해 실행될 것.
sched.start()


# 예약 정보를 받고 보내는 부분(기구별로 나눔)
@app.route('/bench_reservation', methods=['GET', 'POST'])
def reserve_bench():
    if request.method == 'GET':
        b = []
        data = Bench.query.all()
        for i in data:
            a = {
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        id = params['id']
        userid = params['userid']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        bench = Bench(id, userid, date, start_time, end_time)
        db.session.add(bench)
        db.session.commit()
        return 'OK'


@app.route('/aerobic_reservation', methods=['GET', 'POST'])
def reserve_aerobic():
    if request.method == 'GET':
        b = []
        data = Aerobic.query.all()
        for i in data:
            a = {
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        id = params['id']
        userid = params['userid']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        aerobic = Aerobic(id, userid, date, start_time, end_time)
        db.session.add(aerobic)
        db.session.commit()
        return 'OK'


@app.route('/reck_reservation/<date>', methods=['GET', 'POST'])
def reserve_reck(date):
    if request.method == 'GET':
        start_lst = []
        end_lst = []
        b = []
        data = Reck.query.filter(Reck.date == date).all()
        for i in data:
            start_lst.append(i.start_time)
            end_lst.append(i.end_time)
        a = {
            "start_time": start_lst,
            "end_time": end_lst
        }
        b.append(a)
        return jsonify(b)
    elif request.method == 'POST':
        params = request.get_json()
        userid = params['userid']
        date = params['date']
        start_time = params['start_time']
        end_time = params["end_time"]

        temp = start_time.split(':')
        res_start_time = int(temp[0])*100 + int(temp[1])
        temp = end_time.split(':')
        res_end_time = int(temp[0]) * 100 + int(temp[1])
        return_data = 'OK'
        data = Reck.query.filter(Reck.date == date).all()
        maxid = 0
        for i in data :
            temp = i.start_time.split(':')
            data_stime = int(temp[0])*100 + int(temp[1])
            temp = i.end_time.split(':')
            data_etime = int(temp[0]) * 100 + int(temp[1])

            if maxid<i.id : maxid = i.id
            if res_start_time>=data_stime and res_start_time<=data_etime :
                return_data = 'overlap'
            elif res_end_time>=data_stime and res_end_time<=data_etime :
                return_data = 'overlap'
            elif res_start_time<=data_stime and data_stime<=res_end_time :
                return_data = 'overlap'


        if return_data == 'OK' :
            reck = Reck(maxid+1, userid, date, start_time, end_time)
            db.session.add(reck)
            db.session.commit()
        return return_data


# 유저 마이페이지 부분, 사용자의 예약 정보를 불러옴.
@app.route('/reservation_user/<userid>', methods=['GET', 'POST'])
def reservation_user(userid):
    if request.method == 'GET':

        reservelist = []

        benchdata = Bench.query.filter(Bench.userid == userid).all()
        reckdata = Reck.query.filter(Reck.userid == userid).all()
        aerobicdata = Aerobic.query.filter(Aerobic.userid == userid).all()

        for i in benchdata:
            temp = {
                "equipment": "bench",
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            reservelist.append(temp)
        for i in reckdata:
            temp = {
                "equipment": "reck",
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            reservelist.append(temp)
        for i in aerobicdata:
            temp = {
                "equipment": "aerobic",
                "date": i.date,
                "start_time": i.start_time,
                "end_time": i.end_time,
                "userid": i.userid
            }
            reservelist.append(temp)

        return jsonify(reservelist)


@app.route('/bench_reservation_user/<userid>', methods=['GET', 'POST'])
def benchreserve_user(userid):
    if request.method == 'GET':
        bench = []
        benchdata = Bench.query.filter(Bench.userid == userid).all()
        for i in benchdata:
            a = {"datetime": i.date + " " + i.time,
                 "userid": i.userid}
            bench.append(a)
        return jsonify(bench)


@app.route('/reck_reservation_user/<userid>', methods=['GET', 'POST'])
def reckreserve_user(userid):
    if request.method == 'GET':
        reck = []
        reckdata = Reck.query.filter(Reck.userid == userid).all()
        for i in reckdata:
            a = {"datetime": i.date + " " + i.time,
                 "userid": i.userid}
            reck.append(a)

        return jsonify(reck)


@app.route('/aerobic_reservation_user/<userid>', methods=['GET', 'POST'])
def aerobicreserve_user(userid):
    if request.method == 'GET':
        aerobic = []
        aerobicdata = Aerobic.query.filter(Aerobic.userid == userid).all()
        for i in aerobicdata:
            a = {"datetime": i.date + " " + i.time,
                 "userid": i.userid}
            aerobic.append(a)

        return jsonify(aerobic)


# 유저 정보를 불러오는 부분
@app.route('/userdata/<userid>', methods=['GET', 'POST'])
def getUserData(userid):
    if request.method == 'GET':
        data = User.query.filter(User.id == userid).all()
        temp = []
        for i in data:
            a = {'userid': i.id, 'user_name': i.name, 'start_date': i.start_date, 'end_date': i.end_date,
                 'enrollment': i.enrollment}
            temp.append(a)
        return jsonify(temp)


if __name__ == "__main__":
    migrate = Migrate()
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.app = app
    db.create_all()
    migrate.init_app(app, db)
    app.run(debug = False, host = '0.0.0.0')
#기구별로 나눠서 저장되게 바꾸기.
