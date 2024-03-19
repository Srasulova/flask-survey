from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# key names will use to store some things in the session
# put here as constants so we are guaranteed to be consistent in 
# our spelling of these
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


# responses = []

@app.route("/")
def home_page():
    # title = survey.title
    # instructions = survey.instructions
    return render_template("survey_start.html", survey=survey )

@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the session of responses"""
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def show_next_question():
    # get the response from the form
    """Save response and redirect to the next question"""
    choice = request.form['answer']

    # add the response to the list
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(survey.questions)):
        return redirect("/answers")
    else:
        return redirect(f"questions/{len(responses)}")

@app.route('/questions/<int:qID>')
def show_question(qID):
    """Display current question"""
    responses = session.get(RESPONSES_KEY)
    question = survey.questions[qID]

    if responses is None:
        # tryint to access question page too soon
        return redirect("/")
    
    if(len(responses) == len(survey.questions)):
        # They have answered all the questions! Thank them
        return redirect("/answers")
    
    if(len(responses) != qID):
        # trying to access questions out of order
        flash(f"Invalid question ID: {qID}")
        return redirect(f"/questions/{len(responses)}")
    
    return render_template("question.html", question_num = qID, question = question)

@app.route('/answers')
def show_answers_page():
    """Survey is complete. Show Answers page"""
    responses = session.get(RESPONSES_KEY)
    return render_template("answers.html", responses = responses)