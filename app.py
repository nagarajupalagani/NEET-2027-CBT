from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DB_NAME = "results.db"
DURATION = 60


# =========================================================
# QUESTIONS
# =========================================================

QUESTIONS = [
    # UNITS AND MEASUREMENTS

    ["Units & Measurements",
     "The measured values of mass and speed are (2.00 ± 0.02) kg and (10.0 ± 0.2) m/s. The maximum percentage error in kinetic energy is:",
     ["2%", "3%", "4%", "5%"], 2],

    ["Dimensions",
     "The dimensional formula of Planck's constant is:",
     ["[M L T^-1]", "[M L^2 T^-1]", "[M L^2 T^-2]", "[M L^-1 T^-2]"], 1],

    ["Dimensional Analysis",
     "The speed of a wave on a stretched string depends on tension F and linear mass density μ as v = k F^a μ^b. The values of a and b are:",
     ["a = 1/2, b = -1/2", "a = -1/2, b = 1/2", "a = 1, b = -1", "a = 1/2, b = 1/2"], 0],

    ["Units & Measurements",
     "A quantity X = a^2 b^3 / sqrt(c). The percentage errors in a, b and c are 1%, 2% and 4%, respectively. The maximum percentage error in X is:",
     ["6%", "8%", "10%", "12%"], 3],

    ["Dimensions",
     "Which pair has the same dimensions?",
     ["Impulse and force", "Torque and energy", "Pressure and force", "Power and momentum"], 1],

    ["Units & Measurements",
     "A length is measured using an instrument whose least count is 0.01 cm. Which reading is consistent with this precision?",
     ["2.745 cm", "2.75 cm", "2.7 cm", "2.7450 cm"], 1],

    ["Dimensions",
     "If force F, velocity v and time t are chosen as fundamental quantities, the dimensional formula of mass is:",
     ["[F v^-1 t]", "[F v^-1 t^-1]", "[F v t^-1]", "[F v^-2 t]"], 1],

    ["Dimensional Analysis",
     "The frequency f of a stretched string depends on its length L, tension T and linear mass density μ. Which relation is dimensionally possible?",
     ["f = kL sqrt(T/μ)", "f = (k/L) sqrt(T/μ)", "f = k sqrt(Tμ)/L", "f = kL/sqrt(Tμ)"], 1],

    ["Dimensions",
     "The dimensional formula of surface tension is:",
     ["[M T^-2]", "[M L T^-2]", "[M L^-1 T^-2]", "[M L^2 T^-2]"], 0],

    ["Units & Measurements",
     "Evaluate (3.42 × 1.5)/2.0 and express the result with the correct number of significant figures:",
     ["2.565", "2.57", "2.6", "2.56"], 2],

    ["Dimensions",
     "The dimensional formula of the universal gravitational constant G is:",
     ["[M^-1 L^3 T^-2]", "[M L^3 T^-2]", "[M^-1 L T^-2]", "[M L^-2 T^-1]"], 0],

    ["Units & Measurements",
     "If x = (5.0 ± 0.1) m and y = (2.0 ± 0.1) m, the maximum percentage error in x/y is approximately:",
     ["2%", "5%", "7%", "10%"], 2],

    ["Dimensional Analysis",
     "Dimensional analysis shows that v^2 = u^2 + 2as is dimensionally consistent. Which conclusion is correct?",
     ["The equation is necessarily physically correct",
      "The equation may be dimensionally correct without being physically correct",
      "The equation is incorrect because velocity is squared",
      "The equation is valid only when acceleration is zero"], 1],

    ["Dimensions",
     "The product of pressure and volume has the dimensions of:",
     ["Power", "Momentum", "Energy", "Force"], 2],

    ["Units & Measurements",
     "The side of a cube is measured as (2.00 ± 0.01) cm. The maximum percentage error in its volume is approximately:",
     ["0.5%", "1.0%", "1.5%", "3.0%"], 3],

    # MOTION IN A STRAIGHT LINE

    ["Motion in a Straight Line",
     "The position of a particle is x = 4t^2 - 2t^3, where x is in metres and t in seconds. After t = 0, when does its velocity next become zero?",
     ["1 s", "4/3 s", "2 s", "8/3 s"], 2],

    ["Motion in a Straight Line",
     "A body starts from rest and moves with constant acceleration. The ratio of the distances covered in the 4th and 2nd seconds is:",
     ["2", "3", "4", "7/3"], 1],

    ["Motion in a Straight Line",
     "A car moving at 20 m/s is uniformly retarded to rest in 5 s. The distance covered during the last second is:",
     ["1 m", "2 m", "4 m", "6 m"], 1],

    ["Motion in a Straight Line",
     "A particle covers 24 m in the first 2 s and 64 m in the next 2 s under uniform acceleration. Its initial velocity is:",
     ["2 m/s", "4 m/s", "6 m/s", "8 m/s"], 1],

    ["Motion in a Straight Line",
     "The position of a particle is x = t^3 - 6t^2 + 9t. At which times is its instantaneous velocity zero?",
     ["1 s and 3 s", "2 s and 3 s", "1 s and 2 s", "0 s and 3 s"], 0],

    ["Motion in a Straight Line",
     "A particle has velocity v = 12 - 3t in SI units. Its displacement from t = 0 to t = 6 s is:",
     ["18 m", "36 m", "24 m", "54 m"], 1],

    ["Motion in a Straight Line",
     "A ball is thrown vertically upward at 30 m/s. Taking g = 10 m/s^2, the total distance travelled in the first 5 s is:",
     ["25 m", "45 m", "65 m", "70 m"], 2],

    ["Motion in a Straight Line",
     "A train moving at 72 km/h is brought to rest uniformly in 200 m. The magnitude of its retardation is:",
     ["0.5 m/s^2", "1 m/s^2", "2 m/s^2", "4 m/s^2"], 1],

    ["Motion in a Straight Line",
     "Car A passes a point at 10 m/s. Five seconds later, car B passes the same point at 15 m/s in the same direction. How long after B passes the point does it catch A?",
     ["5 s", "10 s", "15 s", "20 s"], 1],

    ["Motion in a Straight Line",
     "A particle travels half its total distance at speed v and the remaining half at speed 3v. Its average speed is:",
     ["4v/3", "3v/2", "2v", "2v/3"], 0],

    ["Motion in a Straight Line",
     "A velocity-time graph is a straight line from (0 s, 5 m/s) to (4 s, -3 m/s). The displacement during these 4 s is:",
     ["0 m", "4 m", "8 m", "16 m"], 1],

    ["Motion in a Straight Line",
     "A particle starts with velocity 5 m/s and acceleration 2 m/s^2. Its displacement during the 5th second is:",
     ["12 m", "13 m", "14 m", "15 m"], 2],

    ["Motion in a Straight Line",
     "The position of a particle is x = 2t^3 - 9t^2 + 12t. Its acceleration becomes zero at:",
     ["1 s", "1.5 s", "2 s", "3 s"], 1],

    ["Motion in a Straight Line",
     "A stone is dropped from rest. It covers 35 m during the last second of its fall. Taking g = 10 m/s^2, the total time of fall is:",
     ["3.5 s", "4 s", "4.5 s", "5 s"], 1],

    ["Motion in a Straight Line",
     "A particle moves 10 m east and then 6 m west in 4 s. The magnitude of its average velocity is:",
     ["1 m/s", "2 m/s", "4 m/s", "4 m/s"], 1],

    ["Motion in a Straight Line",
     "A particle has initial velocity 8 m/s and acceleration -2 m/s^2. The total distance travelled in the first 6 s is:",
     ["12 m", "16 m", "20 m", "24 m"], 2],

    ["Motion in a Straight Line",
     "A body moving with constant acceleration changes its speed from 10 m/s to 30 m/s while covering 100 m. The time taken is:",
     ["2.5 s", "4 s", "5 s", "10 s"], 2],

    ["Motion in a Straight Line",
     "The position of a particle is x = 6t - t^2. The total distance travelled from t = 0 to t = 8 s is:",
     ["16 m", "18 m", "20 m", "25 m"], 2],

    ["Motion in a Straight Line",
     "Two particles start simultaneously from the same point in opposite directions with speeds 6 m/s and 8 m/s. Their separation after 12 s is:",
     ["24 m", "72 m", "96 m", "168 m"], 3],

    ["Motion in a Straight Line",
     "A bus moves initially at 15 m/s, accelerates at 1 m/s^2 for 10 s, and then continues at constant speed for 20 s. Its total distance is:",
     ["350 m", "400 m", "450 m", "500 m"], 2],

    ["Motion in a Straight Line",
     "The position of a particle is x = 10 + 8t - 2t^2. Its maximum position is:",
     ["16 m", "18 m", "20 m", "26 m"], 1],

    ["Motion in a Straight Line",
     "A particle covers 20 m in the first 2 s and 40 m in the next 2 s under constant acceleration. Its acceleration is:",
     ["2.5 m/s^2", "5 m/s^2", "7.5 m/s^2", "10 m/s^2"], 1],

    ["Motion in a Straight Line",
     "A vehicle moving at 25 m/s is brought to rest uniformly in 5 s. Its displacement during the first 3 s is:",
     ["15 m", "22.5 m", "30 m", "37.5 m"], 2],

    ["Motion in a Straight Line",
     "A particle starts from rest and accelerates at 2 m/s^2 for 5 s. It then decelerates at 1 m/s^2 until it stops. The total distance travelled is:",
     ["50 m", "75 m", "100 m", "125 m"], 2],

    ["Motion in a Straight Line",
     "A particle has velocity v = 4t - 12. The total distance travelled from t = 0 to t = 5 s is:",
     ["10 m", "13 m", "17 m", "25 m"], 2],

    ["Motion in a Straight Line",
     "A particle has velocity v = 3t^2 - 12t + 9. During which interval is its velocity negative?",
     ["0 < t < 1", "1 < t < 3", "t > 3", "It is never negative"], 1],

    ["Motion in a Straight Line",
     "A car travels one-third of a journey at 30 km/h and the remaining two-thirds at 60 km/h. Its average speed is:",
     ["40 km/h", "45 km/h", "48 km/h", "50 km/h"], 2],

    ["Motion in a Straight Line",
     "A particle moves from x = -4 m to x = 8 m and then to x = 2 m in 6 s. Its average speed is:",
     ["1 m/s", "2 m/s", "3 m/s", "4 m/s"], 2],

    ["Motion in a Straight Line",
     "A ball is thrown vertically upward from the ground at 40 m/s. Taking g = 10 m/s^2, its displacement during the 6th second is:",
     ["-5 m", "0 m", "5 m", "10 m"], 0],

    ["Motion in a Straight Line",
     "A particle starts from rest and moves with acceleration a = 4t in SI units. Its velocity at t = 3 s is:",
     ["6 m/s", "18 m/s", "12 m/s", "36 m/s"], 1],
]
# =========================================================
# DATABASE
# =========================================================

def db():
    c = sqlite3.connect(DB_NAME)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    c = db()

    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            score INTEGER NOT NULL,
            correct INTEGER NOT NULL,
            wrong INTEGER NOT NULL,
            unattempted INTEGER NOT NULL,
            time_taken INTEGER NOT NULL,
            answers TEXT NOT NULL
        )
    """)

    c.commit()
    c.close()


init_db()


# =========================================================
# STUDENT TEST PAGE
# =========================================================

STUDENT_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NEET 2027 Physics - Units and Motion </title>

<style>
body{
    margin:0;
    font-family:Arial,sans-serif;
    background:#eef2f7;
    color:#182033;
}

header{
    background:#173f7a;
    color:white;
    padding:18px 25px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:22px;
    font-weight:bold;
}

.timer{
    font-size:28px;
}

.container{
    max-width:1400px;
    margin:25px auto;
    padding:15px;
}

.card{
    background:white;
    border-radius:14px;
    padding:25px;
    box-shadow:0 3px 12px rgba(0,0,0,.08);
}

input[type=text]{
    width:100%;
    box-sizing:border-box;
    padding:14px;
    margin:8px 0 15px;
    border:1px solid #ccc;
    border-radius:8px;
    font-size:17px;
}

button{
    border:0;
    border-radius:8px;
    padding:13px 20px;
    font-size:16px;
    cursor:pointer;
}

.primary{
    background:#173f7a;
    color:white;
}

.warning{
    background:#f5c542;
}

.danger{
    background:#d9534f;
    color:white;
}

.grid{
    display:grid;
    grid-template-columns:1fr 330px;
    gap:20px;
}

.option{
    display:block;
    padding:16px;
    margin:12px 0;
    border:1px solid #ddd;
    border-radius:10px;
    cursor:pointer;
}

.option:hover{
    background:#f4f7fb;
}

.palette{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:8px;
}

.pal{
    padding:12px 5px;
    background:#eee;
    text-align:center;
    border-radius:7px;
    cursor:pointer;
}

.pal.answered{
    background:#35a66f;
    color:white;
}

.pal.current{
    outline:3px solid #173f7a;
}

.pal.marked{
    background:#f5c542;
}

#exam{
    display:none;
}

.question{
    font-size:21px;
    line-height:1.5;
}

.topic{
    color:#555;
    font-weight:bold;
}

.controls{
    display:flex;
    gap:10px;
    margin-top:20px;
    flex-wrap:wrap;
}

@media(max-width:800px){
    .grid{
        grid-template-columns:1fr;
    }
}
</style>
</head>

<body>

<header>
<div>NEET 2027 PHYSICS • TEST 03</div>
<div class="timer" id="timer">60:00</div>
</header>

<div class="container">

<div id="intro" class="card">

<h1>Units, Motion in a line</h1>

<p><b>45 Questions • 60 Minutes • 180 Marks</b></p>

<p>Correct: +4 &nbsp;&nbsp; Wrong: −1 &nbsp;&nbsp; Unattempted: 0</p>

<label>Student Name</label>
<input id="name" type="text" placeholder="Enter your name">

<label>Roll Number</label>
<input id="roll" type="text" placeholder="Enter roll number">

<button class="primary" onclick="start()">Start Test</button>

</div>


<div id="exam">

<div class="grid">

<div class="card">

<div class="topic" id="topic"></div>

<h2 id="qno"></h2>

<div class="question" id="question"></div>

<div id="options"></div>

<div class="controls">
<button onclick="previous()">Previous</button>
<button class="warning" onclick="mark()">Mark for Review</button>
<button onclick="clearAnswer()">Clear</button>
<button class="primary" onclick="next()">Save & Next</button>
</div>

</div>


<div class="card">

<h2>Question Palette</h2>

<div class="palette" id="palette"></div>

<hr>

<button class="danger" onclick="submitTest()">Submit Test</button>

</div>

</div>

</div>

</div>


<script>

const Q = {{ questions|tojson }};

let i = 0;
let answers = Array(Q.length).fill(null);
let marked = Array(Q.length).fill(false);

let active = false;
let submitted = false;
let startTime = 0;
let remaining = 3600;


function start(){

    const name = document.getElementById("name").value.trim();
    const roll = document.getElementById("roll").value.trim();

    if(!name || !roll){
        alert("Please enter name and roll number.");
        return;
    }

    document.getElementById("intro").style.display="none";
    document.getElementById("exam").style.display="block";

    active = true;
    startTime = Date.now();

    render();
    palette();
    tick();
}


function render(){

    const q = Q[i];

    document.getElementById("topic").textContent = q[0];
    document.getElementById("qno").textContent =
        "Question " + (i+1) + " of " + Q.length;

    document.getElementById("question").textContent = q[1];

    let html="";

    q[2].forEach((x,j)=>{

        html += `
        <label class="option">
            <input
                type="radio"
                name="answer"
                ${answers[i]===j ? "checked" : ""}
                onchange="answers[i]=${j}; palette();"
            >
            ${String.fromCharCode(65+j)}. ${x}
        </label>
        `;

    });

    document.getElementById("options").innerHTML=html;

    palette();
}


function palette(){

    let html="";

    Q.forEach((_,j)=>{

        let cls="pal";

        if(answers[j]!==null) cls+=" answered";
        if(marked[j]) cls+=" marked";
        if(j===i) cls+=" current";

        html += `
        <div class="${cls}" onclick="go(${j})">
            ${j+1}
        </div>
        `;

    });

    document.getElementById("palette").innerHTML=html;
}


function go(n){

    i=n;
    render();

}


function next(){

    if(i < Q.length-1){
        i++;
        render();
    }else{
        alert("You are on the last question. You can submit the test.");
    }

}


function previous(){

    if(i>0){
        i--;
        render();
    }

}


function clearAnswer(){

    answers[i]=null;
    render();

}


function mark(){

    marked[i]=!marked[i];
    palette();

}


async function submitTest(){

    if(!active || submitted) return;

    if(!confirm("Submit test now?")) return;

    submitted=true;
    active=false;

    const elapsed = Math.floor((Date.now()-startTime)/1000);

    const payload={
        name:document.getElementById("name").value.trim(),
        roll:document.getElementById("roll").value.trim(),
        answers:answers,
        elapsed:elapsed
    };

    try{

        const res=await fetch("/submit",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(payload)
        });

        const data=await res.json();

        if(!res.ok){
            throw new Error(data.error || "Submission failed");
        }

        if(data.id){
            window.location.href="/response/"+data.id;
        }else{
            alert("Test submitted, but result could not be opened.");
        }

    }catch(err){

        submitted=false;
        active=true;

        alert("Submission error: " + err.message);

    }

}


function tick(){

    if(!active) return;

    remaining = Math.max(
        0,
        3600-Math.floor((Date.now()-startTime)/1000)
    );

    const min=String(Math.floor(remaining/60)).padStart(2,"0");
    const sec=String(remaining%60).padStart(2,"0");

    document.getElementById("timer").textContent=min+":"+sec;

    if(remaining<=0){
        submitTest();
        return;
    }

    setTimeout(tick,1000);
}

</script>

</body>
</html>
"""


# =========================================================
# RESPONSE SHEET
# =========================================================

RESPONSE_HTML = """
<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Response Sheet</title>

<style>

body{
    margin:0;
    font-family:Arial;
    background:#eef2f7;
    color:#182033;
}

.container{
    max-width:1000px;
    margin:30px auto;
    padding:15px;
}

.card{
    background:white;
    padding:25px;
    margin-bottom:18px;
    border-radius:14px;
    box-shadow:0 3px 12px rgba(0,0,0,.08);
}

.correct{
    border-left:6px solid #35a66f;
}

.wrong{
    border-left:6px solid #d9534f;
}

.unattempted{
    border-left:6px solid #999;
}

button{
    padding:13px 20px;
    border:0;
    border-radius:8px;
    background:#173f7a;
    color:white;
    font-size:16px;
}

@media print{
    .no-print{
        display:none;
    }
}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>Test Submitted Successfully</h1>

<h2>NEET 2027 PHYSICS • TEST 01</h2>

<p><b>Student:</b> {{ row["name"] }}</p>

<p><b>Roll Number:</b> {{ row["roll"] }}</p>

<h2>Score: {{ row["score"] }}/180</h2>

<p>
Correct: {{ row["correct"] }}
|
Wrong: {{ row["wrong"] }}
|
Unattempted: {{ row["unattempted"] }}
</p>

</div>


{% for n,q in enumerate(questions) %}

{% set student = answers[n] %}
{% set correct = q[3] %}

<div class="card
{% if student is none %}
unattempted
{% elif student == correct %}
correct
{% else %}
wrong
{% endif %}
">

<h3>Question {{ n+1 }}</h3>

<p><b>{{ q[1] }}</b></p>

{% if student is none %}

<p>Your Answer: <b>Not Attempted</b></p>

{% elif student == correct %}

<p>Your Answer:
<b>{{ "ABCD"[student] }}. {{ q[2][student] }}</b>
✓ Correct
</p>

{% else %}

<p>Your Answer:
<b>{{ "ABCD"[student] }}. {{ q[2][student] }}</b>
✗ Wrong
</p>

<p>
Correct Answer:
<b>{{ "ABCD"[correct] }}. {{ q[2][correct] }}</b>
</p>

{% endif %}

</div>

{% endfor %}


<div class="card no-print">

<button onclick="window.print()">Download / Save as PDF</button>

</div>

</div>

</body>
</html>
"""


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template_string(
        STUDENT_HTML,
        questions=QUESTIONS
    )


# =========================================================
# SUBMIT
# =========================================================

@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json(force=True)

    name = str(data.get("name","")).strip()[:100]
    roll = str(data.get("roll","")).strip()[:50]
    answers = data.get("answers",[])
    elapsed = int(data.get("elapsed",0))

    if not name or not roll or not isinstance(answers,list):
        return jsonify({
            "error":"Name, roll number and answers are required."
        }),400

    answers = (answers + [None]*len(QUESTIONS))[:len(QUESTIONS)]

    correct = sum(
        1
        for a,q in zip(answers,QUESTIONS)
        if isinstance(a,int) and a == q[3]
    )

    wrong = sum(
        1
        for a,q in zip(answers,QUESTIONS)
        if a is not None and a != q[3]
    )

    unattempted = len(QUESTIONS) - correct - wrong

    score = correct*4 - wrong

    c = db()

    cur = c.execute("""
        INSERT INTO results
        (name,roll,score,correct,wrong,unattempted,time_taken,answers)
        VALUES (?,?,?,?,?,?,?,?)
    """,(
        name,
        roll,
        score,
        correct,
        wrong,
        unattempted,
        elapsed,
        json.dumps(answers)
    ))

    c.commit()

    # IMPORTANT:
    # lastrowid belongs to the CURSOR, not the CONNECTION.
    result_id = cur.lastrowid

    c.close()

    return jsonify({
        "id":result_id,
        "score":score,
        "correct":correct,
        "wrong":wrong,
        "unattempted":unattempted
    })


# =========================================================
# RESPONSE SHEET
# =========================================================

@app.route("/response/<int:result_id>")
def response_sheet(result_id):

    c = db()

    row = c.execute(
        "SELECT * FROM results WHERE id=?",
        (result_id,)
    ).fetchone()

    c.close()

    if not row:
        return "Response sheet not found",404

    answers = json.loads(row["answers"])

    return render_template_string(
        RESPONSE_HTML,
        row=row,
        answers=answers,
        questions=QUESTIONS,
        enumerate=enumerate
    )


# =========================================================
# TEACHER LOGIN
# =========================================================

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Teacher Login</title>
<style>
body{
    font-family:Arial;
    background:#eef2f7;
}
.card{
    max-width:400px;
    margin:80px auto;
    background:white;
    padding:30px;
    border-radius:14px;
}
input{
    width:100%;
    box-sizing:border-box;
    padding:14px;
    margin:10px 0;
}
button{
    padding:13px 20px;
    background:#173f7a;
    color:white;
    border:0;
    border-radius:8px;
}
</style>
</head>
<body>

<div class="card">

<h1>Teacher Login</h1>

<form method="POST">

<input
type="password"
name="password"
placeholder="Teacher password"
required
>

<button type="submit">Login</button>

</form>

{% if error %}
<p style="color:red">{{error}}</p>
{% endif %}

</div>

</body>
</html>
"""


@app.route("/teacher/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        password=request.form.get("password","")

        stored=os.environ.get("TEACHER_PASSWORD","teacher123")

        if password == stored:

            session["teacher"]=True

            return redirect(url_for("dashboard"))

        return render_template_string(
            LOGIN_HTML,
            error="Incorrect password."
        )

    return render_template_string(
        LOGIN_HTML,
        error=None
    )


# =========================================================
# TEACHER DASHBOARD
# =========================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Teacher Dashboard</title>

<style>

body{
    font-family:Arial;
    background:#eef2f7;
}

.container{
    max-width:1100px;
    margin:30px auto;
    padding:15px;
}

.card{
    background:white;
    padding:20px;
    margin-bottom:15px;
    border-radius:12px;
}

table{
    width:100%;
    border-collapse:collapse;
}

th,td{
    padding:12px;
    border-bottom:1px solid #ddd;
    text-align:left;
}

a{
    color:#173f7a;
}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>Teacher Dashboard</h1>

<h2>NEET 2027 PHYSICS • TEST 01</h2>

</div>

<div class="card">

<table>

<tr>
<th>Name</th>
<th>Roll</th>
<th>Score</th>
<th>Correct</th>
<th>Wrong</th>
<th>Unattempted</th>
<th>Response</th>
</tr>

{% for r in results %}

<tr>

<td>{{r["name"]}}</td>

<td>{{r["roll"]}}</td>

<td>{{r["score"]}}/200</td>

<td>{{r["correct"]}}</td>

<td>{{r["wrong"]}}</td>

<td>{{r["unattempted"]}}</td>

<td>
<a href="/response/{{r['id']}}" target="_blank">
View
</a>
</td>

</tr>

{% endfor %}

</table>

</div>

</div>

</body>
</html>
"""


@app.route("/teacher/dashboard")
def dashboard():

    if not session.get("teacher"):
        return redirect(url_for("login"))

    c=db()

    results=c.execute("""
        SELECT *
        FROM results
        ORDER BY id DESC
    """).fetchall()

    c.close()

    return render_template_string(
        DASHBOARD_HTML,
        results=results
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/teacher/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# RUN
# =========================================================

if __name__=="__main__":

    port=int(os.environ.get("PORT",5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
