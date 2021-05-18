# UWA Motorsports Department Quiz

<h2> Purpose of Application </h2>
<p>This web application is a formative assessment targeted for new and prospective members of the UWA Motorsports Team. The website aims to introduce new members
to each of the available departments in the team, discussing what their primary role is, as well as the relevance of the department to sustaining the 
club. The website offers 5 tutorial modules - one for each department (Finance, Marketing, Chassis, Vehicle Dynamics, Powertrain), which consists of content
followed by questions, the answers of which are dynamically evaluated by the client side. The website also provides a quiz at the end which asks questions related
to the content of the modules. The server collects the quiz and returns an approximation of which department it believes would suit the user (simply by finding the section with the most correct answers).</p>

<p>Users must register to access the quiz. Their progress is saved consistently by the server (on every form input change), allowing them to leave and return part-way through the quiz. The server also stores all submissions made by the user, allowing them to view past submissions and well as delete past submissions. The server  stores an aggregate department approximation based on all of the submitted quizzes to date.</p><br>

<h2> Architecture </h2>
<p>The project uses Flask as its web-framework (i.e., a model-view-controller), utilising a legacy-HTML-style web app structure (server-side rendering), where the server renders and serves entire webpages. Although AJAX is used, the received data (by the client-side) is typically not used to render html elements.</p>
<br>
<h2> How to launch app? </h2>
<ol>
    <li> Install virtual environment using the command $virtualenv venv </li>
    <li> Install dependencies using the command $pip install -r requirements.txt </li>
    <li> If the app is to be deployed, set the secret key by entering in .bashrc - export $SECRET_KEY=(some_secret_key) </li>
    <li> Initialise the database by calling $flask db init --> $flask db migrate --> $flask db upgrade </li>
    <li> Run the program using the commmand $flask run or by running tutorial.py </li>
</ol>
<br>
<h2> Unit tests </h2>
<p>The unit test for this application is ./tests/unit_test.py. This program tests all the functions, model methods, and other logic used in the application - this includes, model methods, the intial model state, helper functions stored in controller.py and logic used by routing functions (especially SQL queries). You can run the unit test by calling $python3 /tests/unit_test.py from the top level of the repository.</p>


