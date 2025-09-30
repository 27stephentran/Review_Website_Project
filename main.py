from flask import Flask, render_template, request, redirect, url_for, session, flash
import scripts.database as db 

app = Flask(__name__)

db.init_db()
db.seed_data()

app.secret_key = "verysecretkey"

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']

        if action == 'login':
            # Handle login
            user = db.login_user(username,password)
            if user:
                session['user'] = user
                flash(f"Welcome {user['name']} (Grade: {user['grade']})!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password", "danger")
        elif action == 'register':
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():    
    if request.method == "POST":
        action = request.form['action']
        if action == "register":
            username = request.form['username']
            password = request.form['password']
            grade  = request.form['grade']
            name = request.form['name']
            if db.register_user(username, password, name, int(grade)):
                flash(f"Registration successfully! You can now log in ", "success")
                return redirect(url_for('login'))
            else:
                flash("Username already exist try login!", 'danger')
        elif action == "login":
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if 'user' not in session:
        flash("Please log in first.", "danger")
        return redirect(url_for('login'))
    user = session['user']

    # Paging and filtering
    page = int(request.args.get('page', 1))
    per_page = 5
    selected_subject = request.args.get('subject', None)
    all_tasks = db.get_tasks_by_grade(user['grade'])
    # Get all subjects for filter dropdown
    subjects = sorted(list(set([t[3] for t in all_tasks])))
    if selected_subject:
        tasks = [t for t in all_tasks if t[3] == selected_subject]
    else:
        tasks = all_tasks
    total_task = len(tasks)
    start = (page-1)*per_page
    end = start+per_page
    paged_tasks = tasks[start:end]
    completed_task = db.get_completed_task_ids(user_id=user["user_id"])
    done_tasks = len([t for t in tasks if t[0] in completed_task])
    undone_tasks = total_task - done_tasks
    percent_done = done_tasks/total_task*100 if total_task > 0 else 0
    total_pages = (total_task + per_page - 1) // per_page

    if request.method == "POST":
        task_id = request.form.get("task_id")
        user['task_id'] = task_id
        flash(f"you have selected task ID: {task_id}", 'info')
        return redirect(url_for('quiz'))

    return render_template(
        "dashboard.html",
        user=user,
        tasks=paged_tasks,
        done_tasks=done_tasks,
        total_task=total_task,
        percent_done=percent_done,
        undone_tasks=undone_tasks,
        page=page,
        total_pages=total_pages,
        subjects=subjects,
        selected_subject=selected_subject
    )


# Helper to count questions for a task
def get_question_count(task_id):
    questions = db.get_questions_by_task(task_id)
    return len(questions)

@app.route('/quiz', methods =["GET", "POST"])
def quiz():
    if 'user' not in session or 'task_id' not in session['user']:
        flash("Please select a task from the dashboard first.", "danger")
        return redirect(url_for('dashboard'))
    task_id = session['user']['task_id']
    questions = db.get_questions_by_task(task_id)
    if request.method == "POST":
        # Collect answers and calculate statistics
        user_answers = {}
        for q in questions:
            ans = request.form.get(f"answer_{q[0]}")
            user_answers[q[0]] = ans
        total = len(questions)
        correct = 0
        for q in questions:
            if user_answers.get(q[0]) == q[6]:
                correct += 1
        percent = (correct / total * 100) if total > 0 else 0
        # Mark this quiz as completed for the user
        db.mark_task_completed(session['user']['user_id'], task_id)
        # No need to refresh user session; dashboard always queries latest completed tasks from DB
        return render_template("quiz_result.html", total=total, correct=correct, percent=percent)
    return render_template("quiz.html", questions=questions)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", 'info')
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)