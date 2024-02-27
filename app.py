from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []

@app.route("/")
def home_page():
    title = survey.title
    instructions = survey.instructions
    return render_template("survey_start.html", title = title, instructions = instructions )

@app.route("/start", methods=["POST"])
def start_survey():
    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def show_next_question():
    # get the response from the form
    choice = request.form['answer']

    # add the response to the list
    responses.append(choice)

    if(len(responses) == len(survey.questions)):
        return redirect("/answers")
    else:
        return redirect(f"questions/{len(responses)}")

@app.route('/questions/<int:qID>')
def show_question(qID):
    question = survey.questions[qID]
    if responses is None:
        return redirect("/")
    
    if(len(responses) == len(survey.questions)):
        return redirect("/answers")
    
    if(len(responses) != qID):
        flash(f"Invalid question ID: {qID}")
        return redirect(f"/questions/{len(responses)}")
    
    return render_template("question.html", question = question)

@app.route('/answers')
def show_answers_page():
    return render_template("answers.html", responses = responses)