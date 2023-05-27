from db import db
from classes.user import Teacher, Parent
import os
from flask import Flask, session, redirect, render_template, request, abort, jsonify, url_for
from algorithm import get_program, get_programm_as_string
from authlib.integrations.flask_client import OAuth
import firebase_admin
from firebase_admin import credentials, auth

GOOGLE_CLIENT_ID = "716115744911-j2flcrafmde0v6rujupbs36us82mugjt.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))
firebase_cred = credentials.Certificate('secrets/final-project-adhd-5607b9bcb602.json')
firebase_app = firebase_admin.initialize_app(firebase_cred)
oauth = OAuth(app)
current_user = None


@app.route("/")
def main_page():
    """
        Main page: welcome....
        Here login button

    :return:
    """
    return render_template("index.html")


@app.route("/login")
def login():
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/google/auth', methods=['GET', 'POST'])
def google_auth():
    """
    The function handles authorization request from frontend
    Request headers decoded in order to get user data
    and this data is used to fetch customer id from Customers DB

    """
    global current_user
    token = oauth.google.authorize_access_token()['userinfo']

    email = token['email']
    result = db.execute_query(f"SELECT * FROM users WHERE email='{email}'")[0]
    if 'permission' in result and result['permission'] == "TEACHER":
        teacher = Teacher(
            name=result['name'],
            personal_id=result['personal_id'],
            email=result['email'],
            permission=result['permission'],
            phone=result['phone_number']
        )
        session['current_user'] = teacher.json()
        current_user = teacher

    elif 'permission' in result and result['permission'] == "PARENT":
        parent = Parent(
            name=result['name'],
            personal_id=result['personal_id'],
            email=result['email'],
            permission=result['permission'],
            phone=result['phone_number']
        )
        session['current_user'] = parent.json()
        current_user = parent

    if current_user:
        return redirect(f"/workspace/{current_user.personal_id}")
    else:
        abort(404)


@app.route("/workspace/<personal_id>", methods=["GET", "POST"])
def workspace_page(personal_id):
    if isinstance(current_user, Teacher):
        query = f"SELECT * FROM pupils WHERE teacher_id={personal_id}"
        kind = 'Teacher'
    else:
        query = f"SELECT * FROM pupils WHERE parent_id={personal_id}"
        kind = 'Parent'

    result = db.execute_query(query)
    data = {'user': current_user.to_dict(),
            'pupils': result}
    return render_template("workspace.html", user=data, kind=kind)


@app.route("/workspace/<personal_id>/edit_personal_info", methods=["GET", "POST"])
def edit_personal_info(personal_id):
    global current_user

    if request.method == "GET":
        return render_template('edit_info.html', user_info=current_user.to_dict())
    if request.method == "POST":
        input_data = request.form
        if not current_user.name == input_data['name'] or not current_user.personal_id == input_data[
            'personal_id'] or not current_user.email == input_data['email'] or not current_user.phone == input_data[
            'phone']:
            query = f"""UPDATE users SET name='{input_data['name']}', email='{input_data['email']}', phone_number='{input_data['phone']}' WHERE personal_id='{personal_id}'"""
            db.execute_query(query)
            current_user.name = input_data['name']
            current_user.personal_id = input_data['personal_id']
            current_user.email = input_data['email']
            current_user.phone = input_data['phone']

        return redirect(f"/workspace/{personal_id}")


@app.route("/workspace/<personal_id>/programs/new_program", methods=["GET", "POST"])
def creating_new_program(personal_id):
    if request.method == "GET":
        return render_template("new_program.html")
    elif request.method == "POST":
        name = request.form['name']
        id = request.form['id']
        parent_name = request.form['parent_name']
        parent_email = request.form['parent_email']
        parent_phone = request.form['parent_phone']
        parent_id = request.form['parent_id']
        teacher_id = personal_id
        age = request.form['age']
        height = request.form['height']
        sex = request.form['sex']
        symptoms = request.form.getlist('symptoms')

        query = f"INSERT INTO users (personal_id, name, email, permission, phone_number)" \
                f"VALUES ('{parent_id}','{parent_name}','{parent_email}','PARENT','{parent_phone}')"

        db.execute_query(query)
        result = get_program(symptoms)
        program_string = get_programm_as_string(id, name, result)
        query = f"INSERT INTO pupils (id, parent_id, teacher_id, name, age, height, sex, symptom, programm)" \
                f"VALUES ('{id}', '{parent_id}', '{teacher_id}', '{name}', {age}, {height}, '{sex}', '{result['diagnosis']}', '{program_string}')"
        db.execute_query(query)
        return redirect(f"/workspace/{personal_id}/programs/{id}")


@app.route("/workspace/<personal_id>/programs/<child_id>", methods=["GET"])
def dispaly_program(personal_id, child_id):
    query = f"SELECT * FROM pupils WHERE id={child_id}"
    result = db.execute_query(query)
    return render_template("program_view.html", result=result[0])


@app.route("/logout")
def logout():
    """
    Clear the session (in future)
    """
    return "OK"


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
