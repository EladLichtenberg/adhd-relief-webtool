import json
from openAI import OpenAIModel
from db import db
from classes.user import User
import os
from flask import Flask, session, redirect, render_template, request, url_for, abort
from algorithm import get_program, get_programm_as_string
from authlib.integrations.flask_client import OAuth
from mail import send_mail_notification
import secrets
from oauthlib.oauth2 import OAuth2Error


HOST = 'localhost'
PORT = 5000
DEBUG = True

with open("secrets/oauth_creds.json") as file:
    creds = json.loads(file.read())

GOOGLE_CLIENT_ID = creds['web']['client_id']
GOOGLE_CLIENT_SECRET = creds['web']['client_secret']
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))

oauth = OAuth(app)
current_user = None

# Initialize OpenAI
url = 'https://api.openai.com/v1/chat/completions'
api_key = os.environ.get("ENV_API_KEY")
chat = OpenAIModel(api_key=api_key, url=url)


@app.route("/")
def main_page():
    """
        Main page: welcome....
        Here login button

    :return:
    """
    msg = None
    if current_user is not None:
        return redirect(f"/workspace/{current_user.personal_id}")
    if 'error' in session:
        msg = [session['error']]
    return render_template("index.html", msg=msg)


@app.route("/login")
def login():
    """
        Initiates the authentication process for logging in with a Google account using OAuth.

        This function registers the Google OAuth provider with the specified configuration,
        including the client ID, client secret, server metadata URL, and scope of authentication.
        It then redirects the user to the Google login page to authenticate.

        Returns:
            A redirect response to the Google login page.

        Raises:
            Any exceptions raised by the underlying OAuth library.
    """
    if 'current_user' in session:
        session.pop('current_user', None)
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        },

    )
    redirect_uri = url_for('google_auth', _external=True)

    return oauth.google.authorize_redirect(redirect_uri, prompt='consent')


@app.route('/google/auth', methods=['GET', 'POST'])
def google_auth():
    """
    The function handles authorization request from frontend
    Request headers decoded in order to get user data
    and this data is used to fetch customer id from Customers DB

    """
    if 'current_user' in session:
        return redirect("/login")
    global current_user

    try:
        token = oauth.google.authorize_access_token()['userinfo']
    except OAuth2Error:
        session['error'] = 'Notification: Mismatching state error'
        return redirect("/")

    session['logged_in'] = True
    email = token['email']
    result = db.execute_query(f"SELECT * FROM users WHERE email='{email}'")
    if result:
        result = result[0]
        user = User(name=result['name'],
                    personal_id=result['personal_id'],
                    email=result['email'],
                    permission=result['permission'],
                    phone=result['phone_number'])

        session['current_user'] = user.json()
        current_user = user

        return redirect(f"/workspace/{current_user.personal_id}")
    else:
        session['error'] = 'Notification: Login fault'
        return redirect("/")



@app.route("/workspace/<personal_id>", methods=["GET", "POST"])
def workspace_page(personal_id):
    """
        Renders the workspace page based on the provided personal ID.
        If the 'current_user' is not present in the session, the function redirects to the home page ("/").
        If the 'current_user' is an instance of the 'Teacher' class, a query is executed to retrieve pupils
        associated with the teacher's ID. Otherwise, a query is executed to retrieve pupils associated with
        the parent's ID.
        The retrieved data and the user information are passed to the 'workspace.html' template, along with
        the 'kind' parameter indicating whether the user is a teacher or parent.

        Args:
            personal_id (int): The personal ID of the user.

        Returns:
            The rendered 'workspace.html' template with the user data and the 'kind' parameter.
    """
    if 'current_user' not in session:
        return redirect("/")

    if current_user.permission == "TEACHER":
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
    """
    Handles the editing of personal information for a user.
    If the 'current_user' is not present in the session, the function redirects to the home page ("/").
    If the request method is GET, the function renders the 'edit_info.html' template with the current user's
    information retrieved from the 'current_user' object.
    If the request method is POST, the function retrieves the input data from the request form. If any of the
    edited fields (name, personal_id, email, or phone) are different from the current user's information, an
    SQL UPDATE query is executed to update the user's information in the database. Additionally, the 'current_user'
    object is updated with the new information.

    Args:
        personal_id (int): The personal ID of the user.

    Returns:
        A redirect response to the workspace page.
    """
    if 'current_user' not in session:
        return redirect("/")
    global current_user

    if request.method == "GET":
        return render_template('edit_info.html', user_info=current_user.to_dict())
    if request.method == "POST":
        input_data = request.form
        if not current_user.name == input_data['name'] or not current_user.personal_id == input_data[
            'personal_id'] or not current_user.email == input_data['email'] or not current_user.phone == input_data[
            'phone']:
            query = f"""UPDATE users SET name='{input_data['name']}', email='{input_data['email']}', phone_number='{input_data['phone']}' WHERE personal_id='{personal_id}'"""
            res = db.execute_query(query)
            if res is None:
                abort(505)
            current_user.name = input_data['name']
            current_user.personal_id = input_data['personal_id']
            current_user.email = input_data['email']
            current_user.phone = input_data['phone']

        return redirect(f"/workspace/{personal_id}")


@app.route("/workspace/<personal_id>/programs/new_program", methods=["GET", "POST"])
def creating_new_program(personal_id):
    """
    Creates a new program for a user.

    If the 'current_user' is not present in the session, the function redirects to the home page ("/").

    If the request method is GET, the function retrieves a list of parents from the database and renders the
    'new_program.html' template with the parent data.

    If the request method is POST, the function retrieves input data from the request form. It performs various
    checks on the input data, such as validating symptoms and determining a diagnosis. If a diagnosis is not found,
    an appropriate error message is rendered in the 'new_program.html' template.

    If the 'parent_type' is not present in the request form, a new parent entry is inserted into the database.
    If yes, tha child is related with an existing parent

    The program and sports are generated based on the diagnosis. Chat recommendations are retrieved using the
    'chat.execute_query()' function. The program and sports data are stored in the session for further use.

    Args:
        personal_id (int): The personal ID of the user.

    Returns:
        A redirect response to the 'choose_days' page for the created program.

    """
    if 'current_user' not in session:
        return redirect("/")
    if request.method == "GET":
        query = f"SELECT * FROM users WHERE permission='PARENT'"

        session['parents'] = db.execute_query(query)
        if not query:
            abort(500)
        return render_template("new_program.html", msg=None, data=session['parents'])
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

        if not symptoms:
            return render_template("new_program.html", data=session['parents'], msg=["Please choose symptoms"])
        symptoms_string = '/'.join(symptoms)
        result = get_program(symptoms)
        if result == 'No diagnosis':
            return render_template("new_program.html", data=session['parents'],
                                   msg=["No diagnosis determined: Please check symptoms again"])

        if 'parent_type' not in request.form:
            query = f"INSERT INTO users (personal_id, name, email, permission, phone_number)" \
                    f"VALUES ('{parent_id}','{parent_name}','{parent_email}','PARENT','{parent_phone}')"
            res = db.execute_query(query)
        else:
            parent_id = request.form['parent_type']

        program_string, sports = get_programm_as_string(id, name, result)

        chat_recommendations = chat.execute_query(result['supplements'])

        session['initial_program'] = program_string
        session['initial_sports'] = ','.join(sports)

        query = f"INSERT INTO pupils (id, parent_id, teacher_id, name, age, height, sex, symptom, chat_recomendations, criteria)" \
                f"VALUES ('{id}', '{parent_id}', '{teacher_id}', '{name}', {age}, {height}, '{sex}', '{result['diagnosis']}', '{chat_recommendations}', '{symptoms_string}')"
        res = db.execute_query(query)
        send_mail_notification(receiver_email=parent_email, receiver_name=parent_name)
        return redirect(f"/workspace/{personal_id}/programs/{id}/choose_days")


@app.route("/workspace/<personal_id>/programs/<id>/choose_days", methods=["GET", "POST"])
def choose_days_sport_activities(personal_id, id):
    """
         Allows the user to choose sport activities and days for a program.

        If the request method is GET, the function retrieves the initial sports data from the session and renders
        the 'choose_sporsts.html' template with the sports data.

        If the request method is POST, the function retrieves the selected sports and days from the request form.
        It constructs a schedule based on the selected sports and days, and updates the program accordingly.

        The updated program is then stored in the database for the specified pupil ID.

        Finally, the function redirects to the program page for the pupil.

        Args:
            personal_id (int): The personal ID of the user.
            id (int): The ID of the pupil.

        Returns:
            A redirect response to the program page for the pupil.
    """
    if 'current_user' not in session:
        return redirect("/")
    if request.method == 'GET':
        result = session['initial_sports'].split(',')
        return render_template('choose_sporsts.html', data=result, msg=None)
    if request.method == 'POST':
        form = request.form
        if not form:
            result = session['initial_sports'].split(',')
            return render_template('choose_sporsts.html', data=result, msg=['Choose sport activities and days'])
        selected_sports = []
        for item in form:
            selected_sports.append(item)
        schedule = []
        for sport in selected_sports:
            schedule.append({'name': sport.replace('-week', ''), 'days': request.form.getlist(sport)})

        program = session['initial_program']
        for sport in schedule:
            program += ' ' + sport['name'] + '\n\t'
            program += 'On '
            for day in sport['days']:
                program += day + ', '
            program = program[:-2] + '\n'

        query = f"UPDATE pupils SET programm='{program}' WHERE id='{id}'"
        db.execute_query(query)
        return redirect(f"/workspace/{personal_id}/programs/{id}")


@app.route("/workspace/<personal_id>/programs/<child_id>/edit_program", methods=["GET", "POST"])
def edit_program(personal_id, child_id):
    """
    Edit the program and info for a child.

    Args:
        personal_id (str): The personal ID of the user.
        child_id (str): The ID of the child.

    Returns:
        If the request method is GET:
            Returns the edit program template with the child and parent information.
        If the request method is POST:
            Updates the child's information and program based on the form input, and redirects
            to the appropriate page.

    """
    if 'current_user' not in session:
        return redirect("/")
    if request.method == 'GET':
        query = f"SELECT * FROM pupils WHERE id={child_id}"
        child = db.execute_query(query)

        if not child:
            if child is None:
                abort(500)
            session['error'] = "Bad request: such child doesn't exists"
            return redirect("/")

        session['current_child'] = child[0]
        child[0]['criteria'] = child[0]['criteria'].split("/")
        session['current_symptoms'] = child[0]['criteria']
        query = f"SELECT * FROM users WHERE personal_id='{child[0]['parent_id']}'"
        parent = db.execute_query(query)
        if not parent:
            if parent is None:
                abort(500)
            session['error'] = "Bad request: such parent doesn't exists"
            return redirect("/")

        return render_template('edit_program.html', result=child[0], parent=parent[0],
                               personal_id=personal_id, child_id=child_id, msg=None)  # TODO
    elif request.method == "POST":

        name = request.form['name']
        id = request.form['id']
        age = request.form['age']
        height = request.form['height']

        parent_name = request.form['parent_name']
        parent_email = request.form['email']

        symptoms = request.form.getlist('symptoms')
        if not symptoms:
            return render_template("new_program.html", msg=["Please choose symptoms"])

        if name != session['current_child']['name']:
            query = f"UPDATE pupils SET name='{name}' WHERE id='{id}'"
            db.execute_query(query)
            session['current_child']['name'] = name
        if age != session['current_child']['age']:
            query = f"UPDATE pupils SET age='{age}' WHERE id='{id}'"
            db.execute_query(query)
            session['current_child']['age'] = age
        if height != session['current_child']['height']:
            query = f"UPDATE pupils SET height='{height}' WHERE id='{id}'"
            db.execute_query(query)
            session['current_child']['height'] = height

        if set(symptoms) == set(session['current_symptoms']):  # TODO
            return render_template("program_view.html", result=session['current_child'], personal_id=personal_id,
                                   child_id=child_id)

        symptoms_string = '/'.join(symptoms)
        result = get_program(symptoms)
        if result == 'No diagnosis':
            return render_template("new_program.html", msg=["No diagnosis determined: Please check symptoms again"])

        program_string, sports = get_programm_as_string(id, name, result)

        chat_recommendations = chat.execute_query(result['supplements'])

        session['initial_program'] = program_string
        session['initial_sports'] = ','.join(sports)

        query = f"UPDATE pupils SET symptom='{result['diagnosis']}', chat_recomendations='{chat_recommendations}', criteria='{symptoms_string}' WHERE id='{id}'"
        db.execute_query(query)

        send_mail_notification(receiver_email=parent_email, receiver_name=parent_name)
        return redirect(f"/workspace/{personal_id}/programs/{id}/choose_days")


@app.route("/workspace/<personal_id>/programs/<child_id>", methods=["GET"])
def dispaly_program(personal_id, child_id):
    """
        Displays the program for a child.

        If the 'current_user' is not present in the session, the function redirects to the home page ("/").

        A query is executed to retrieve the program information for the specified child ID from the database.

        The retrieved program information is passed to the 'program_view.html' template for rendering.

        Args:
            personal_id (int): The personal ID of the user.
            child_id (int): The ID of the child.

        Returns:
            The rendered 'program_view.html' template with the program information.
    """
    if 'current_user' not in session:
        return redirect("/")
    kind = current_user.permission
    query = f"SELECT * FROM pupils WHERE id='{child_id}'"
    result = db.execute_query(query)
    if not result:
        if result is None:
            abort(500)
        session['error'] = "Bad request: such child doesn't exists"
        return redirect("/")
    return render_template("program_view.html", result=result[0], personal_id=personal_id, child_id=child_id, kind=kind)


@app.route("/logout")
def logout():
    global current_user
    if 'current_user' not in session:
        return redirect("/")
    """
    Clear the session (in future)
    """

    session.clear()
    current_user = None
    print('Logged out')
    return redirect('/')


# if __name__ == '__main__':
#     app.run(host=HOST, port=PORT, debug=DEBUG)
