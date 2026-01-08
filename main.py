from flask import Flask, render_template, request, redirect, flash, session, url_for
import db_utils  # מייבאים את הקובץ שיצרנו

app = Flask(__name__)
app.secret_key = 'flytau_secret'


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    uid = request.form.get('identifier')
    pwd = request.form.get('password')

    # שימוש בפונקציות מה-utils (בדיוק כמו בתרגול 7)
    manager = db_utils.is_manager(uid, pwd)
    if manager:
        session['user'] = manager['FirstName']
        session['role'] = 'manager'
        return f"שלום {session['user']}, התחברת כמנהל"

    customer = db_utils.is_customer(uid, pwd)
    if customer:
        session['user'] = customer['FirstName']
        session['role'] = 'customer'
        return f"שלום {session['user']}, התחברת כלקוח"

    flash("פרטים שגויים")
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            'id': request.form.get('id'),
            'f_name': request.form.get('first_name'),
            'l_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'pwd': request.form.get('password'),
            'address': request.form.get('address'),
            'passport': request.form.get('passport'),
            'dob': request.form.get('birth_date')
        }

        if db_utils.add_customer(user_data):
            flash("נרשמת בהצלחה!")
            return redirect(url_for('home'))
        else:
            flash("שגיאה ברישום")

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)