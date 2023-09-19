# CSS StyleSheet Maker

#### Description:
My project is a CSS StyleSheet Maker in the form of a web-based application. The purpose of this
application is to enable users to make and visualize simple stylesheets more effieciently with ease. The stylesheet contains CSS to change background color, text color, font family
, height, and width for a main header, a div header, a div body, As well as the background color of the whole page. 
**This application was inplemented in the CS50 IDE using the following...**
- Python
- HTML
- CSS
- Flask
- JavaScript
- SQl
- Werkzeug

### Overview
How the application works is at first it lets the user login or make an account. Once an account is made the username, hash of their password, and 
their user id is inserted into a table named **users** **(See /register below)**. The User is then brought to the homepage where they can click a link 
that will bring them editing page. once the link is clicked a session id is created and a bunch of default values for CSS propeties are loaded into a table named **Sessions** and those default values are then used in the webpage**(/edit GET)**.
The editing page is is set up like a basic webpage. There is a main header at the top of the page and a div below it whith a sub header and some text. When any of these are clicked 
on a form will open in which their are several fields that the user can fill in that will change the CSS of the element and update **Sessions** with those new values. The user can also click on a button in the top 
right that will open a sidebar that gives you option to change CSS properties for both headers at once, the background color of the webpage and also the div body**(/edit POST)**. Once the user is satisfied with the loook of their page they can finish by clicking on the save button located at the bottom of the side bar.
Clicking on the button will bring the user to a page that will have a stylesheet with all their inputed values and default ones if they didn't change it. they will able to copy and paste the code into their own stylesheet for use.

### application.py
Application.py contains 6 main functions which are discussed in further detail below.

#### register()
In the function register there are two methods available, GET and POST. When request method GET is used register simply return render template.html. when request method POST is used register makes sure that the inputs where submitted 
properly and then takes the inputs and makes sure that the username doesn't already exist in the table **users**. If it hasn't already been taken the username and a hash of the password is inputted into users as well as a user id that has been assigned to them. The user is then redirected to the homepage.

#### login()
In the function login if the request method is POST, it takes the username and password the user submitted and checks to see if the username exists in the table **users** and if the password is correct by matching the hash of it. If the username doesn't exists and/or the password is 
incorrect then a login.html is returned except with an invalid input message. If the inputs were correct then a session id will be created and the user will be redirected to the homepage. If the request method was GET the function would return login.html

#### home()
The function home first checks if the user is logged in. If the user is not logged in they are redirected to /login, but if the user is found to be logged in then home.html is returned.

#### preset1()
The function preset1 first checks if the user is logged in. If the user is not logged in they are redirected to /login. Otherwise if the user is logged in they are then redirected to /edit.

#### edit()
The function edit first checks if the user is logged in. If they are not they are redirected to /login. If the request method is GET first a session id is created.Then some default values are inserted in the table **sessions**. The CSS propeties are then pulled from the table **sessions** and render_template /editpres1.html is returned with those values t=so they can be used directly into the CSS of the website..If the request method is POST then the function takes all the inputs the user submitted and updates the default values for the element they submitted it in for that also has theit session id in the table **sessions**. The values from the table **sessions** are then selected and loaded as variables and return render template returns editpres1.html with those values as variables so they can be used directly into the CSS of the website.

#### save()
The function save first checks if the user is logged in. If they are not they are redirected to /login. If they are then the CSS properties from the table **sessions** are loaded into variables. Save.html is then returned with render_template along with the CSS values so they can be used in the stylesheet for the user to copy.


### template.db
template.db has two tables **users** and **sessions** that store all the data required for the operation of the application. The tables are discussed in further detail below.

#### users 
The table users has 3 columns. id, username, and hash. the id column is a unique constraint and primary key of the table. the username and hash columns are used for logging in.

### sessions
The table sessions has 10 columns. id, user\_id, session\_id, element, color, font, fontsize, height, width, textcolor. the id column is the primary key. user\_id is a foreign key used to link the users table, session\_id is used to keep a users session data seperate from past sessions. element is used to specify what element the CSS property is for.
the columns color, font, fontsize, height, width, and textcolor are all for CSS properties.



