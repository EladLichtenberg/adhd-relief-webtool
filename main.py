from flask import Flask, session, redirect, abort, request, render_template
from db import db
from user import Teacher, Parent
import os


app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))
RESULT_STUB = {
    'name': 'Nikita Matatov',
    'personal_id': '333879096',
    'permission': 'TEACHER',
    'email': 'docmat63@gmail.com'
}
current_user = None

@app.route("/")
def main_page():
    """
        Main page: welcome....
        Here login button

    :return:
    """
    return "<h1>Hello World<h1> <button><a href='/login'>LOGIN</button>"


@app.route("/login")
def login():
    """
        Login logic:
        after succesfull login check permissions
    
    """
    # TO_DO oAuth with firebase
    email = 'docmat63@gmail.com'
    result = db.execute_query(f"SELECT * FROM Users WHERE email='{email}'")[0]
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
        current_user = parent
        return redirect(f"/parent_workspace/{parent.personal_id}")

    else:
        abort(404)


@app.route("/teacher_workspace/<personal_id>", methods=["GET", "POST"])
def teacher_page(personal_id):
    if request.method == "GET":
        pass

    if request.method == "POST":
        pass

    return personal_id


@app.route("/parent_workspace/<personal_id>", methods=["GET", "POST"])
def parent(personal_id):
    if request.method == "GET":
        query = f"SELECT * FROM pupils WHERE parent_id={personal_id}"
        result = db.execute_query(query)
        return render_template("parent_view.html", args=result)
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
                """ # modify query with phone number etc....
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
                """ # modify query with phone number etc....
        if db.execute_query(query):
            return redirect(f"/teacher_workspace/{personal_id}")
        else:
            abort(500)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)