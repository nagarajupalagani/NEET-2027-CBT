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
    ["Units & Measurements", "The dimensional formula of Planck's constant is:",
     ["[M L T^-1]", "[M L^2 T^-1]", "[M L^2 T^-2]", "[L^2 T^-1]"], 1],

    ["Units & Measurements", "Which of the following is dimensionless?",
     ["Force", "Pressure", "Strain", "Surface tension"], 2],

    ["Dimensional Analysis", "The time period T of a simple pendulum depends on its length l and acceleration due to gravity g. Using dimensional analysis, the relation is:",
     ["T proportional to sqrt(l/g)", "T proportional to l/g", "T proportional to sqrt(g/l)", "T proportional to l*g"], 0],

    ["Units & Measurements", "If the percentage errors in mass and velocity are 2% and 3%, respectively, the maximum percentage error in kinetic energy is:",
     ["3%", "5%", "8%", "10%"], 2],

    ["Units & Measurements", "For Q = A^2 sqrt(B) / C^3, the percentage errors in A, B, and C are 1%, 4%, and 2%, respectively. The maximum percentage error in Q is:",
     ["6%", "10%", "8%", "12%"], 1],

    ["Dimensions", "The dimensional formula of pressure is:",
     ["[M L^-1 T^-2]", "[M L T^-2]", "[M L^2 T^-2]", "[M L^-2 T^-1]"], 0],

    ["Dimensions", "The SI unit of the universal gravitational constant G is:",
     ["N m kg^-1", "N m^2 kg^-2", "N m^-2 kg^2", "kg m s^-1"], 1],

    ["Dimensions", "The dimensions of 1/(mu_0 epsilon_0), where mu_0 and epsilon_0 are the permeability and permittivity of free space, are:",
     ["[L T^-1]", "[L^2 T^-2]", "[M L T^-2]", "[L^-2 T^2]"], 1],

    ["Dimensions", "Which pair has the same dimensions?",
     ["Work and power", "Torque and work", "Force and pressure", "Momentum and energy"], 1],

    ["Units & Measurements", "The number of significant figures in 0.005060 is:",
     ["2", "3", "4", "5"], 2],

    ["Dimensions", "The dimensional formula of surface tension is:",
     ["[M T^-2]", "[M L T^-2]", "[M L^-1 T^-2]", "[M L^2 T^-2]"], 0],

    ["Units & Measurements", "If x = 2.50 m and y = 1.2 m, the value of x + y, expressed with appropriate precision, is:",
     ["3.70 m", "3.7 m", "3.700 m", "3.0 m"], 1],

    ["Units & Measurements", "A length is measured as (5.2 +/- 0.1) cm. Its approximate percentage error is:",
     ["0.52%", "1.9%", "5.2%", "10%"], 1],

    ["Dimensions", "The dimensional formula of coefficient of viscosity is:",
     ["[M L^-1 T^-1]", "[M L T^-2]", "[M^0 L^0 T^0]", "[M L^-2 T^-2]"], 0],

    ["Dimensions", "The dimensional formula of angular momentum is:",
     ["[M L^2 T^-1]", "[M L T^-1]", "[M L^2 T^-2]", "[M^0 L^0 T^0]"], 0],

    ["Dimensional Analysis", "Which of the following equations is dimensionally consistent?",
     ["s = ut + (1/2)at^2", "s = u + at", "v = u + at^2", "s = ut^2 + at"], 0],

    ["Units & Measurements", "The SI unit of impulse is:",
     ["N s", "N/s", "J/s", "kg m^2/s^2"], 0],

    ["Dimensional Analysis", "If P = a/(b+c), and b and c have the same dimensions, for the equation to be dimensionally consistent:",
     ["[P] = [a]/[b]", "[P] = [a][b]", "[P] = [b]/[a]", "[P] = [a]+[b]"], 0],

    ["Dimensions", "The dimensional formula of refractive index is:",
     ["[L T^-1]", "[M^0 L^0 T^0]", "[M L T^-1]", "[M L^-1 T^-2]"], 1],

    ["Dimensions", "The dimensional formula of the gravitational constant G is:",
     ["[M^-1 L^3 T^-2]", "[M L^3 T^-2]", "[M^-1 L T^-2]", "[M L^-2 T^-1]"], 0],

    ["Motion in a Straight Line", "A body starts from rest and moves with uniform acceleration 2 m/s^2. Its displacement in 5 s is:",
     ["10 m", "20 m", "25 m", "50 m"], 2],

    ["Motion in a Straight Line", "A body has an initial velocity of 10 m/s and acceleration -2 m/s^2. Its velocity after 8 s is:",
     ["-6 m/s", "-4 m/s", "4 m/s", "6 m/s"], 0],

    ["Motion in a Straight Line", "A particle travels 30 m in the first 2 s and 50 m in the next 2 s under uniform acceleration. Its acceleration is:",
     ["2 m/s^2", "5 m/s^2", "10 m/s^2", "20 m/s^2"], 1],

    ["Motion in a Straight Line", "The velocity of a particle is v = 6t - 2t^2, in SI units. Its displacement between t = 0 and t = 2 s is:",
     ["8 m", "10 m", "20/3 m", "12 m"], 2],

    ["Motion in a Straight Line", "A projectile is launched vertically upward with speed 20 m/s. Taking g = 10 m/s^2, the total time of flight is:",
     ["2 s", "3 s", "4 s", "5 s"], 2],

    ["Motion in a Straight Line", "A vehicle moving at 20 m/s comes to rest under uniform retardation of 4 m/s^2. Its stopping distance is:",
     ["25 m", "40 m", "50 m", "100 m"], 2],

    ["Motion in a Straight Line", "The position of a particle is x = 3t^2 - 2t + 1, in SI units. Its velocity at t = 2 s is:",
     ["6 m/s", "8 m/s", "10 m/s", "12 m/s"], 2],

    ["Motion in a Straight Line", "The position of a particle is x = t^3 - 6t^2 + 9t, in SI units. At which times is its instantaneous velocity zero?",
     ["1 s and 3 s", "2 s and 3 s", "1 s and 2 s", "0 s and 3 s"], 0],

    ["Motion in a Straight Line", "A car travels equal distances at speeds of 20 km/h and 30 km/h. Its average speed is:",
     ["20 km/h", "24 km/h", "25 km/h", "30 km/h"], 1],

    ["Motion in a Straight Line", "A car travels for equal time intervals at speeds of 20 km/h and 30 km/h. Its average speed is:",
     ["20 km/h", "25 km/h", "24 km/h", "30 km/h"], 1],

    ["Motion in a Straight Line", "A particle completes one full lap of a circular track and returns to its starting point. Its displacement is:",
     ["Equal to the circumference", "Equal to the diameter", "Zero", "Equal to half the circumference"], 2],

    ["Motion in a Straight Line", "The slope of a position-time graph represents:",
     ["Acceleration", "Velocity", "Displacement", "Speed multiplied by time"], 1],

    ["Motion in a Straight Line", "The area under a velocity-time graph represents:",
     ["Acceleration", "Force", "Displacement", "Momentum"], 2],

    ["Motion in a Straight Line", "The velocity of a particle changes uniformly from +4 m/s to -4 m/s in 4 s. Its displacement during this interval is:",
     ["16 m", "8 m", "0 m", "-16 m"], 2],

    ["Motion in a Straight Line", "A body starts from rest and accelerates uniformly at 4 m/s^2 for 3 s. It then moves at constant velocity for 2 s. The total displacement is:",
     ["18 m", "24 m", "42 m", "48 m"], 2],

    ["Motion in a Straight Line", "A stone is dropped from rest from a height of 45 m. Taking g = 10 m/s^2, the time taken to reach the ground is approximately:",
     ["2 s", "3 s", "4 s", "5 s"], 1],

    ["Motion in a Straight Line", "A car moving at 10 m/s is followed by another car moving at 15 m/s. If the second car is initially 50 m behind the first and both move in the same direction at constant speeds, the catch-up time is:",
     ["5 s", "10 s", "15 s", "20 s"], 1],

    ["Motion in a Straight Line", "Two particles move in opposite directions with speeds of 8 m/s and 12 m/s. Their separation after 5 s, if they start together, is:",
     ["20 m", "40 m", "80 m", "100 m"], 3],

    ["Motion in a Straight Line", "A particle starts with initial velocity 5 m/s and accelerates uniformly at 2 m/s^2. The distance travelled during the fourth second is:",
     ["9 m", "11 m", "12 m", "13 m"], 2],

    ["Motion in a Straight Line", "A ball is thrown vertically upward with speed 30 m/s. Taking g = 10 m/s^2, its displacement after 4 s is:",
     ["40 m", "60 m", "80 m", "120 m"], 0],

    ["Motion in a Straight Line", "A particle has velocity v = 10 - 4t, in SI units. The total distance travelled from t = 0 to t = 4 s is:",
     ["8 m", "10 m", "16 m", "17 m"], 3],

    ["Motion in a Straight Line", "A vehicle covers equal distances at speeds of 40 km/h and 60 km/h. Its average speed is:",
     ["48 km/h", "50 km/h", "52 km/h", "55 km/h"], 0],

    ["Motion in a Straight Line", "The position of a particle is x = 4t - t^2, in SI units. Its velocity becomes zero at:",
     ["1 s", "2 s", "3 s", "4 s"], 1],

    ["Motion in a Straight Line", "A particle moves from x = 2 m to x = 9 m in 3 s. Its average velocity is:",
     ["2 m/s", "7/3 m/s", "3 m/s", "7 m/s"], 1],

    ["Motion in a Straight Line", "A train moving at 72 km/h comes to rest uniformly in 10 s. Its stopping distance is:",
     ["50 m", "100 m", "150 m", "200 m"], 1],
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

<p><b>50 Questions • 60 Minutes • 180 Marks</b></p>

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

<h2>Score: {{ row["score"] }}/200</h2>

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
