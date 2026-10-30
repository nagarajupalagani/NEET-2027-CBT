from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DB_NAME = "results.db"
DURATION = 70


# =========================================================
# QUESTIONS
# =========================================================
QUESTIONS = [
    ['Units & Measurements', 'A car moves from P to T along the path shown: 8 km east, 4 km south, 4 km west, then 1 km north. Find its net displacement.', ['2 km, 60° south of west', '5 km, 37° south of east', '6 km, 53° east of south', '10 km, 45° east of south'], 1],
    ['Motion in a Straight Line', 'A body travels at 4 m/s during half the total time and at 6 m/s during the remaining half. Its average speed is', ['5 m/s', '4 m/s', '6 m/s', '1 m/s'], 0],
    ['Motion in a Straight Line', 'The coordinates of a particle are x = 2t² and y = 3t (SI units). Find the magnitudes of velocity and acceleration at t = 1 s.', ['5 m/s, 4 m/s²', '6 m/s, 2 m/s²', '11 m/s, 12 m/s²', '2 m/s, 14 m/s²'], 0],
    ['Motion in a Straight Line', 'A particle is projected vertically upward at 25 m/s. Taking g = 10 m/s², its displacement during the third second is', ['30 m', 'Distance covered is 30 m', 'Distance covered is 2.5 m', '2.5 m'], 2],
    ['Units & Measurements', 'The number of significant figures in 0.005 is', ['1', '4', '3', 'Infinite'], 0],
    ['Motion in a Straight Line', 'The position of a particle is s = 2t³ + 3t² + 2t + 8. At what time is its acceleration zero?', ['0.5 s', '2 s', '1 s', 'Acceleration can never be zero'], 3],
    ['Units & Measurements', 'If momentum P, area A and time T are fundamental quantities, the dimensional formula of energy is', ['[P A⁻¹ T]', '[P² A T]', '[P A⁻¹ᐟ² T]', '[P A¹ᐟ² T⁻¹]'], 3],
    ['Units & Measurements', 'For significant figures: (I) All non-zero digits are significant. (II) Zeros between two non-zero digits are significant. Choose the correct option.', ['Only I is correct', 'Only II is correct', 'Both I and II are correct', 'Both I and II are incorrect'], 2],
    ['Motion in a Straight Line', 'Velocity depends on displacement as v = Ks², where K is a positive constant. The acceleration-versus-displacement graph is', ['A straight line increasing from the origin', 'An increasing curve that gradually flattens', 'An increasing curve that becomes steeper', 'A decreasing curve'], 2],
    ['Motion in a Straight Line', "A ball is released from rest from a building and travels 25 m in the last second before impact. Taking g = 10 m/s², the building's height is", ['45 m', '60 m', '50 m', '25 m'], 0],
    ['Motion in a Straight Line', "A balloon starts from rest and accelerates upward at 4 m/s². A coin is dropped from it 5 s after the start. The coin's initial velocity at release is", ['Zero', '20 m/s upward', '30 m/s upward', '45 m/s upward'], 1],
    ['Motion in a Plane', 'The trajectory is y = √3 x − ½x². Taking g = 10 m/s², the angle of projection is', ['30°', '45°', '60°', '75°'], 2],
    ['Vectors', 'A = i + j + k and B = i + j + 2k. Find |A − 2B|.', ['√3', '√17', '√11', '√7'], 2],
    ['Units & Measurements', 'The units of length, mass and time are 1 cm, 100 g and 10 s. The unit of kinetic energy in this system is', ['0.1 erg', '10 erg', '1 erg', '20 erg'], 2],
    ['Units & Measurements', 'Distance s = (100 ± 0.1) m and time t = (10 ± 0.1) s. The average speed with maximum permissible error is', ['(10 ± 0.11) m/s', '(1000 ± 11) m/s', '(10 ± 1.1) m/s', '(100 ± 0.2) m/s'], 0],
    ['Units & Measurements', 'The number of significant zeroes in 2.0500 is', ['1', '5', '3', '6'], 2],
    ['Motion in a Straight Line', 'A particle starts from rest and v = √(αx), where α is a positive constant. The distance travelled in time t is', ['(1/3)αt²', '(1/4)αt²', '(3/8)αt²', 'αt/2'], 1],
    ['Motion in a Plane', 'A ground-to-ground projectile has time of flight 40 s and horizontal range 800 m. Its horizontal velocity component is', ['20 m/s', '10 m/s', '40 m/s', '20√3 m/s'], 0],
    ['Motion in a Straight Line', 'For an object falling from rest in a viscous medium, a = α − βv. Its initial acceleration is', ['β/α', 'βα', 'α/β', 'α'], 3],
    ['Motion in a Straight Line', 'A particle starts from rest. Its acceleration is +2 m/s² for 2 s and −2 m/s² for the next 4 s. Choose the correct speed-time description.', ['Speed rises to 4 m/s at 2 s, then falls linearly to zero at 6 s', 'Speed rises to 4 m/s at 2 s, falls to zero at 4 s, then rises to 4 m/s at 6 s', 'Speed increases curvilinearly throughout', 'Speed rises smoothly with an S-shaped curve'], 1],
    ['Units & Measurements', 'In vernier callipers, n VSD coincide with (n − 2) MSD. If 1 MSD = a mm, the least count is', ['a/n mm', '2a/n mm', '2a/(n − 2) mm', 'a/(n − 2) mm'], 1],
    ['Motion in a Straight Line', 'A particle starts from rest with constant acceleration 2 m/s². The distance travelled during the fifth second is', ['1.25 m', '2.25 m', '9 m', '12 m'], 2],
    ['Motion in a Plane', 'A projectile is launched with initial velocity (i + 2j) m/s. Taking g = 10 m/s², its trajectory is', ['y = 2x − 5x²', 'y = x − 5x²', '4y = 2x − 5x²', 'y = 2x − 25x²'], 0],
    ['Dimensions', 'Which physical quantity has the same dimensions as work?', ["Young's modulus", 'Torque', 'Angular momentum', 'Surface tension'], 1],
    ['Motion in a Plane', 'A ball is projected vertically upward at 12 m/s with constant-magnitude air drag. It takes 1 s to reach maximum height. The maximum height is (g = 10 m/s²).', ['7.2 m', '6 m', '8.3 m', '5 m'], 1],
    ['Motion in a Straight Line', 'The signed area under an acceleration-time graph gives', ['Velocity at any instant', 'Change in velocity', 'Distance travelled', 'Displacement travelled'], 1],
    ['Motion in a Straight Line', 'Which statement is true?', ['If displacement is zero, distance must be zero', 'If distance is zero, displacement must be zero', 'Speed can be positive, negative or zero', 'Magnitude of displacement is always greater than or equal to distance'], 1],
    ['Circular Motion', 'Which statement is incorrect for non-uniform circular motion?', ['Speed changes continuously', 'Velocity remains constant', 'Tangential acceleration is non-zero', 'Acceleration changes continuously'], 1],
    ['Relative Motion', 'The path of a projectile as seen by an observer moving with another projectile (both under gravity) is generally a', ['Straight line', 'Parabola', 'Ellipse', 'Circle'], 0],
    ['Motion in a Straight Line', 'On a velocity-position graph, velocity rises linearly from 10 m/s at x = 2 m to 20 m/s at x = 4 m. Find acceleration in this interval.', ['25 m/s²', '30 m/s²', '75 m/s²', '40 m/s²'], 2],
    ['Motion in a Straight Line', 'The acceleration of a moving body is equal to the', ['Slope of distance-time graph', 'Slope of acceleration-time graph', 'Slope of velocity-time graph', 'Area under velocity-time graph'], 2],
    ['Projectile Motion', 'A projectile has maximum horizontal range 500 m. Its maximum height when launched for maximum range is', ['200 m', '500 m', '125 m', '1000 m'], 2],
    ['Projectile Motion', "A projectile's horizontal range is n times its maximum height. The angle θ satisfies", ['θ = tan⁻¹(2/n)', 'θ = tan⁻¹(4/n)', 'θ = tan⁻¹(3n/2)', 'θ = tan⁻¹(5/n)'], 1],
    ['Projectile Motion', 'The trajectory is y = √3 x − 5x². Its time of flight is', ['√2/5 s', '√3/2 s', '√5/2 s', '√3/5 s'], 3],
    ['Circular Motion', 'Which statement is incorrect for uniform circular motion?', ['Velocity is not constant', 'Speed is constant', 'Kinetic energy is constant', 'Angular speed is not constant'], 3],
    ['Relative Motion', 'Three people at the vertices of an equilateral triangle of side a move at speed v, each always facing the next person. They meet after', ['2a/v', '3a/v', '2a/(3v)', '3a/(2v)'], 2],
    ['Units & Measurements', 'If Z = A³√B/(CD²), and percentage errors in A, B, C and D are 1%, 2%, 3% and 1%, respectively, the percentage error in Z is', ['2%', '9%', '12%', '5%'], 1],
    ['Relative Motion', "A river is 1 km wide and flows at 1 km/h. A swimmer's speed in still water is 2 km/h. For the shortest crossing path, the crossing time is", ['½ h', '1 h', '1/√3 h', '2/√3 h'], 2],
    ['Projectile Motion', 'A particle is projected from the ground with velocity (i + 3j) m/s. Its velocity when it returns to the ground is', ['(i + 3j) m/s', '2(i + 3j) m/s', '2(i − 3j) m/s', '(i − 3j) m/s'], 3],
    ['Vectors', 'The angle made by A = 3i + 4j + 5k with the z-axis is', ['cos⁻¹(3/(5√2))', 'cos⁻¹(4/(5√2))', '45°', '60°'], 2],
    ['SHM', 'For SHM, E = K mˣ nʸ Aᶻ, where K is dimensionless, m is mass, n frequency and A amplitude. Find 2x + y + z.', ['4', '22', '6', '9'], 2],
    ['Motion in a Straight Line', 'A particle has non-zero acceleration', ['Only if velocity direction changes', 'Only if velocity magnitude changes', 'If velocity direction or magnitude or both change', 'Only if neither direction nor magnitude changes'], 2],
    ['Units & Measurements', 'The dimensional formula of acceleration is', ['[M L T⁻¹]', '[M⁰ L T⁻²]', '[M⁰ L⁰ T⁻²]', '[M² L⁻² T³]'], 1],
    ['Motion in a Straight Line', 'A ball is thrown vertically upward from the ground at 40 m/s while another is thrown downward from a height of 45 m at 50 m/s. They collide after', ['2 s', '½ s', '¼ s', '4 s'], 1],
    ['Motion in a Straight Line', 'Acceleration is 5 m/s² from t = 0 to 2 s, then decreases linearly to zero at t = 6 s. If initial velocity is 3 m/s, velocity at 6 s is', ['23 m/s', '13 m/s', '20 m/s', '10 m/s'], 0],
    ['Free Fall', 'A stone falls freely. Distances covered in the first 2 s, the next 2 s and the following 2 s are in the ratio', ['1 : 2 : 3', '1 : 3 : 5', '1 : 1 : 1', '2 : 3 : 4'], 1],
    ['Motion in a Straight Line', 'Position x = 4t² − 3t + 5 (metres). Find speed at t = 2 s.', ['8 m/s', '2 m/s', '13 m/s', 'Zero'], 2],
    ['Free Fall', 'Two bodies of masses 5 kg and 10 kg are dropped from the same height. The ratio of their times to reach the ground is', ['1/2', '5/4', '12/5', '1'], 3],
    ['Vertical Motion', 'A particle is projected vertically upward at 57 m/s. Taking g = 10 m/s², its displacement during the sixth second is', ['2.9 m', '2 m', '1.2 m', '4.2 m'], 1],
    ['Vertical Motion', 'At the maximum height of a body thrown vertically upward', ['Velocity is non-zero but acceleration is zero', 'Acceleration is non-zero but velocity is zero', 'Both acceleration and velocity are zero', 'Both acceleration and velocity are non-zero'], 1],
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
<title>NEET 2027 Physics - AIATS</title>

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
<div>NEET 2027 PHYSICS • TEST 04</div>
<div class="timer" id="timer">70:00</div>
</header>

<div class="container">

<div id="intro" class="card">

<h1>AIATS-01</h1>

<p><b>50 Questions • 70 Minutes • 200 Marks</b></p>

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
<img id="questionImage"
     alt="Question diagram"
     style="display:none; max-width:100%; max-height:460px; margin:16px 0;">
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
const questionImages = {
    0: "/static/q01_displacement.png",
    8: "/static/q09_acceleration_displacement_graph.png",
    19: "/static/q20_acceleration_time_graph.png",
    29: "/static/q30_velocity_position_graph.png",
    44: "/static/q45_acceleration_time_graph.png"
};

const img = document.getElementById("questionImage");

if (questionImages[i]) {
    img.src = questionImages[i];
    img.style.display = "block";
} else {
    img.removeAttribute("src");
    img.style.display = "none";
}
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

<h2>NEET 2027 PHYSICS • TEST 04</h2>

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

<h2>NEET 2027 PHYSICS • TEST 04</h2>

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
