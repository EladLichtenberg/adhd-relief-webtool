from flask import Flask, redirect, abort, request, render_template, session, url_for
from db import db
from classes.user import Teacher, Parent
import os
from flask import Flask, session, redirect, render_template, request, abort, jsonify, url_for
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from google.oauth2 import id_token
# from google.auth.transport import requests
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
    headers = request.headers
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    redirect_uri = url_for('google_auth', _external=True) # ,
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth', methods=['GET', 'POST'])
def google_auth():
    """
    The function handles authorization request from frontend
    Request headers decoded in order to get user data
    and this data is used to fetch customer id from Customers DB

    """
    token = oauth.google.authorize_access_token()['userinfo']

    email = token['email']
    result = db.execute_query(f"SELECT * FROM users WHERE email='{email}'")[0]
    if 'permission' in result and result['permission'] == "TEACHER":
        teacher = Teacher(
            name=result['name'],
            personal_id=result['personal_id'],
            email=result['email'],
            permission=result['permission']
        )
        global current_user
        current_user = teacher

        return redirect(f"/teacher_workspace/{teacher.personal_id}")

    elif 'permission' in result and result['permission'] == "PARENT":
        parent = Parent(
            name=result['name'],
            personal_id=result['personal_id'],
            email=result['email'],
            permission=result['permission']
        )
        session['current_user'] = parent.json()
        return redirect(f"/parent_workspace/{parent.personal_id}")

    else:
        abort(404)




@app.route("/teacher_workspace/<personal_id>", methods=["GET", "POST"])
def teacher_page(personal_id):
    if request.method == "GET":
        query = f"SELECT * FROM pupils WHERE teacher_id={personal_id}"
        result = db.execute_query(query)

        data = {'user': current_user.to_dict(),
                'pupils': result}

        return render_template("workspace.html", user=data, kind="Teacher")
    if request.method == "POST":
        return personal_id


@app.route("/parent_workspace/<personal_id>", methods=["GET", "POST"])
def parent(personal_id):
    if request.method == "GET":
        user = session['current_user']
        query = f"SELECT * FROM pupils WHERE parent_id={personal_id}"
        result = db.execute_query(query)
        data = {'user': user,
                'pupils': result}
        return render_template("parent_view.html", data=data)
    if request.method == "POST":
        pass

    return personal_id


@app.route("/parent_workspace/<personal_id>/edit_personal_info", methods=["GET", "POST"])
def edit_personal_info(personal_id):
    if request.method == "GET":
        render_template('edit_info.html', parent=current_user)
    if request.method == "POST":
        input_data = request.form

        query = f"""UPDATE Users
                    SET name={input_data['name']}, email={input_data['email']} 
                    WHERE personal_id={personal_id} 
                """  # modify query with phone number etc....
        if db.execute_query(query):
            return redirect(f"/parent_workspace/{personal_id}")


@app.route("/teacher_workspace/<personal_id>/edit_personal_info", methods=["GET", "POST"])
def edit_teacher_personal_info(personal_id):
    if request.method == "GET":
        render_template('edit_info.html', parent=current_user)
    if request.method == "POST":
        input_data = request.form

        query = f"""UPDATE Users
                    SET name={input_data['name']}, email={input_data['email']} 
                    WHERE personal_id={personal_id} 
                """  # modify query with phone number etc....
        if db.execute_query(query):
            return redirect(f"/teacher_workspace/{personal_id}")
        else:
            abort(500)


@app.route("/teacher_workspace/<personal_id>/programs/new_program", methods=["POST"])
def creating_new_program(personal_id):
    pass


@app.route("/teacher_workspace/<personal_id>/programs/<child_id>", methods=["GET"])
def get_program(personal_id, child_id):
    query = f"SELECT * FROM Programs WHERE teacher_id={personal_id} AND child_id={child_id}"
    result = db.execute_query(query)
    return render_template("program_view.html", result=result)


@app.route("/logout")
def logout():
    """
    Clear the session (in future)
    """
    return "OK"


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
