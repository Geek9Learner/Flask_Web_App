'''
About Flask
Flask is a lightweight Python framework for web applications that provides the basics for URL routing and page rendering.

What we did in below code.

First we imported the Flask class. An instance of this class will be our WSGI application.

Next we create an instance of this class. The first argument is the name of the application’s module or package. __name__ is a
convenient shortcut to get the current file, This is needed so that Flask knows where to look for resources such as
templates and static files.

We then use the route() decorator to tell Flask what URL should trigger our function. here it is '/'.

The function returns the message we want to display in the user’s browser. The default content type is HTML, so HTML in the string
will be rendered by the browser.
'''

'''
Routing:

Modern web applications use meaningful URLs to help users. Users are more likely to like a page and come back if the page uses a
meaningful URL they can remember and use to directly visit a page.
'''
from flask import Flask,render_template,request,redirect,session #sesion used to restrict user to perform functionality only after login.
from database import Database
import api
dbo = Database()


#rquest: receive data from html form.
app = Flask(__name__)  #making the flask object and passing __main__ (the current file name) through __name__ variable.
app.secret_key = "super secret key" # Passing the secret key, which enable user to login and redirect to login page if user is trying to access functionality through url without even logging inside.
#Routing
@app.route('/')
def index():
    return render_template("app_login.html")

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/perform_registration',methods=['post'])
def perform_registration():
    name = request.form.get('User_name')
    email = request.form.get('User_email')
    password = request.form.get('user_password')
    response = dbo.insert(name,email,password)
    if response:
        return render_template('app_login.html',message="Registration complete! Kindly login")
    else:
        return render_template('register.html',message = 'Email already exist')

@app.route('/perform_login',methods=['post'])
def perform_login():
    email = request.form.get('User_email')
    password = request.form.get('user_password')
    response = dbo.search(email,password)
    if response:
        session['logged_in'] = 1  #defining the session for logged in user, if user didn't login and then with help of session we can redirect them to login page.
        return redirect('/profile')
    else:
        return render_template('app_login.html',message="Incorrect email/password")

@app.route('/profile')
def profile():
    if session: #user can access profile only if they logged in. Otherwise they will be redirected to login page
        return render_template('profile.html')
    else:
        return redirect('/')

@app.route('/ner')
def ner():
    if session:  #user can access NER only if they logged in. Otherwise they will be redirected to login page
        return render_template('ner.html')
    else:
        return redirect('/')

@app.route('/perform_ner',methods=['post'])
def perform_ner():
    if session:   #user can perform ner operation only if they logged in. Otherwise they will be redirected to login page
        text = request.form.get('ner_text')
        response=api.ner(text)
        named_entity = response.json
        return render_template('ner.html',result=named_entity)
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True) #debug=True, it will provide ease of development, no need to run the file again and again, Just do the code changes and refresh the server, Changes will automatically render.

'''
APP Archeitecture:
    Host server(My desktop) ---> Client(Browser)
    User ----Intraction---> Browser ---Come to server(Desktop) ---> Run the functionality from server ---> Server renders in HTML form

    Data Flow:
    Login ---> user enter data ---> HTML Forms ---> Data receive by App.py ----> Data validation with Json file(Database)
    Register ---> Enter data in HTML form --> receive at app.py --> data transfer to Json file
'''