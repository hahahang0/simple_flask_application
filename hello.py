from flask import Flask,url_for
from markupsafe import escape


app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return "<p>Hello world !</p>"

# @app.route("/<name>")
# def hello(name):
#     # return f"Hello, {name}!"
#     return f"Hello,{escape(name)}!"


# @app.route("/index")
# def index():
#     return "This is index page"


# @app.route('/<param>')
# def show_param(param):
#     return f"This is param {param}!"


# @app.route('/user/<username>')
# def show_user_profile(username):
#     return f"This is user {escape(username)}"

# @app.route('/post/<int:post_id>')
# def this_is_post_id(post_id):
#     return f"this is post id{escape(post_id)}"

# @app.route('/path/<path:subpath>')
# def this_is_path_route(subpath):
#     return f"subpath {escape(subpath)}"


#redirection behavior
# @app.route('/products/')
# def redirectionFunction():
#     return "This is product page"

# @app.route('/about')
# def about_page():
#     return "This is about page !"

#url For()
@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

# HTTP METHOD
from flask import request 
# here, we have both the get and post method in the same route,  we can separate if we want , creating different routes and function for each
# @app.route('/login',methods=["GET","POST"]) 
# def login():
#     if request.method == "POST":
#         return do_the_login()
#     else:
#         return show_the_login_form()

#REQUEST OBJECT 
@app.route('/login',methods=["POST","GET"])
def login():
    error = None
    if request.method == "POST":
        if valid_login(request.form["username"],request.form["password"]):
            return log_the_user_in(request.form["username"])
        else:
            error = "Invalid Username/password"
    return render_template('login.html',error=error)


#File UPLOAD 
from werkzeug.utils import secure_filename
@app.route('/upload',methods=["GET","POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["the_file"]
        file.save(f"/var/www/uploads/{secure_filename(file.filename)}")



#COOKIES
#getting cookies
@app.route('/')
def index():
    username = request.cookies.get('username')

#storing cookies 
from flask import make_response
@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie("username","The username")
    return resp


#redirects and errors 

from flask import abort,redirect,url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("Page_not_found.html"),404



#APIS with json 
@app.route('/me')
def me_api():
    user = get_current_user()
    return {
        "username" : user.username,
        "theme" : user.theme,
        "image" : url_for("user_image",filename=user.image),
    }

@app.route("/users")
def users_api():
    users = get_all_users()
    return [users.to_json() for user in users]