import os
from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor


app = Flask(__name__)
app.secret_key = b'IT9_\x92\x06\xbdN\x03\xb8[\xf0\xe2\xab\xbf\x9fk0a\x1dS\xd0\x85\x85'
# app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations', methods=['POST', 'GET'])
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create', methods=['GET', 'POST'])
def create():
    # get requests land us at /create
    if request.method == 'GET':
        return render_template('create.jinja2')
    # post request should query db for the donor, add donation, redir to /all

    if request.method == 'POST':
        # want to make sure there is an acceptable value entered:
        try:
            value = int(request.form['amount'])

        except ValueError:
            render_template('create.jinja2')
        if value <= 0:
            render_template('create.jinja2')

        else:
            donor_name = request.form['name']
            if donor_name:
                try:
                    donor = Donor.select().where(Donor.name == donor_name).get()

                except Donor.DoesNotExist as e:
                    donor = Donor(name=donor_name)
                    donor.save()

                donation = Donation(value=value, donor=donor)
                donation.save()
                return redirect(url_for('all'))
            else:
                return render_template('create.jinja2')


    return render_template('create.jinja2', create=create)
   

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
