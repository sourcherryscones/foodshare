from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select


app = Flask(__name__)
app.secret_key = "secretos"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pgadmin@localhost:5432/crud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class newer_user_data(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    comp_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(14))
    address = db.Column(db.String(140))
    website = db.Column(db.String(200))

    def __init__(self, comp_name, email, phone, address, website):
        self.comp_name = comp_name
        self.email = email
        self.phone = phone
        self.address = address
        self.website = website


class shelter_data(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    comp_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(14))
    address = db.Column(db.String(140))
    website = db.Column(db.String(200))

    def __init__(self, comp_name, email, phone, address, website):
        self.comp_name = comp_name
        self.email = email
        self.phone = phone
        self.address = address
        self.website = website


class listing_data(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    mavail = db.Column(db.Integer)
    provider = db.Column(db.Integer)
    claimed = db.Column(db.Integer)
    desc = db.Column(db.String(500))

    def __init__(self, mavail, provider, claimed, desc):
        self.mavail = mavail
        self.provider = provider
        self.claimed = claimed
        self.desc = desc

@app.route('/')
def start():
    return render_template("index.html")


@app.route('/appstart')
def appstart():
    return render_template("signup.html")

@app.route('/aboutus')
def aboutus():
    return render_template("about.html")

@app.route('/contactus')
def contactus():
    return render_template("contact.html")

@app.route('/restfeed/<int:adder>', methods = ['GET'])
def restfeed(adder):
    stmt = select([listing_data, newer_user_data]).where(listing_data.provider == newer_user_data.id)
    engine = db.get_engine()
    datarr = []
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            datarr.append(row)

    return render_template("listings.html", listing_list=datarr, isRest=True, provider_id=adder)


@app.route('/sheltfeed/<int:sid>', methods = ['GET'])
def sheltfeed(sid):
    stmt = select([listing_data, newer_user_data]).where(listing_data.provider == newer_user_data.id)
    engine = db.get_engine()
    datarr = []
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            datarr.append(row)

    return render_template("listings.html", listing_list=datarr, isRest=False, shelter_id=sid)



@app.route('/addfeeditem/<int:uid>', methods = ['GET'])
def addfeeditem(uid):
    stmt = select([newer_user_data]).where(newer_user_data.id == uid)
    engine = db.get_engine()
    with engine.connect() as conn:
        row = conn.execute(stmt).first()
    return render_template("postnew.html", provider_name=row.comp_name, provider_id=uid)



@app.route('/postlisting', methods = ['POST'])
def postlisting():
    if request.method == 'POST':
        mavail = request.form.get('mavail')
        provider = request.form.get('uid')
        claimed = -1
        desc = request.form.get('desc')

        datacommit = listing_data(mavail, provider, claimed, desc)
        db.session.add(datacommit)
        db.session.commit()
        return redirect('/restfeed/' + provider)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form.get('bname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        website = request.form.get('website')

        datacommit = newer_user_data(name, email, phone, address, website)
        db.session.add(datacommit)

        db.session.commit()

        return redirect('/restfeed/'+str(2))

@app.route('/insertshelter', methods = ['POST'])
def insertshelter():
    if request.method == 'POST':
        name = request.form.get('sname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        website = request.form.get('website')

        datacommit = shelter_data(name, email, phone, address, website)
        db.session.add(datacommit)


        db.session.commit()

        #shelter = shelter_data.query.filter_by(shelter_data.comp_name == name).first()
        #idnumber = shelter.id

        return redirect('/sheltfeed/' + str(2))


@app.route('/connect', methods=['POST'])
def connect():
    sid = request.form.get('sid')
    lid = request.form.get('lid')
    listing = listing_data.query.filter_by(id=lid).first()
    listing.claimed = sid
    db.session.commit()

    return redirect('/sheltfeed/'+sid)

if __name__ == "__main__":
    app.run(debug=True)