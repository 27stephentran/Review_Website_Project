import database as db


import random
def seed_all_quiz_questions():
    quiz_data = {
        (10, 'Trigonometry'): [
            ("What is sin(90°)?", "1", "0", "-1", "0.5", "A"),
            ("Which is a basic trig ratio?", "sin", "log", "exp", "sqrt", "A"),
            ("What is cos(0°)?", "1", "0", "-1", "0.5", "A"),
            ("Which function is periodic?", "sin(x)", "x^2", "e^x", "ln(x)", "A"),
        ],
        (10, 'Algebra'): [
            ("What is the solution to x^2 = 4?", "x=2 or x=-2", "x=4", "x=0", "x=1", "A"),
            ("Which is a linear equation?", "x+2=5", "x^2+1=0", "x^3=8", "2^x=8", "A"),
            ("What is the value of x in 2x=10?", "5", "2", "10", "20", "A"),
            ("Which is a quadratic equation?", "x^2+3x+2=0", "x+1=0", "x^3-1=0", "2^x=8", "A"),
        ],
        (10, 'Physics'): [
            ("Who formulated the three laws of motion?", "Newton", "Einstein", "Tesla", "Curie", "A"),
            ("What is the SI unit of force?", "Newton", "Joule", "Watt", "Pascal", "A"),
            ("What is acceleration?", "Rate of change of velocity", "Speed", "Distance", "Force", "A"),
            ("What is gravity?", "Attractive force", "Repulsive force", "Friction", "Magnetism", "A"),
        ],
        (10, 'Chemistry'): [
            ("What is the charge of a proton?", "+1", "-1", "0", "+2", "A"),
            ("What is H2O?", "Water", "Oxygen", "Hydrogen", "Salt", "A"),
            ("What is NaCl?", "Salt", "Sugar", "Water", "Acid", "A"),
            ("What is the chemical symbol for gold?", "Au", "Ag", "Gd", "Go", "A"),
        ],
        (10, 'Computer Science'): [
            ("What is a variable?", "A storage for data", "A function", "A loop", "A constant", "A"),
            ("Which is a loop structure?", "for", "if", "def", "print", "A"),
            ("What is an algorithm?", "A set of steps", "A variable", "A loop", "A function", "A"),
            ("What is Python?", "A programming language", "A snake", "A car", "A fruit", "A"),
        ],
        (11, 'Trigonometry'): [
            ("What is sin^2(x) + cos^2(x)?", "1", "0", "x", "2", "A"),
            ("Which is a trig identity?", "tan(x)=sin(x)/cos(x)", "sin(x)=x", "cos(x)=1/x", "tan(x)=x", "A"),
            ("What is tan(45°)?", "1", "0", "-1", "√3", "A"),
            ("Which is an even function?", "cos(x)", "sin(x)", "tan(x)", "cot(x)", "A"),
        ],
        (11, 'Algebra'): [
            ("What is i^2?", "-1", "1", "0", "i", "A"),
            ("Which is a complex number?", "2+3i", "2", "3", "i", "A"),
            ("What is the sum of roots of x^2-5x+6=0?", "5", "6", "-5", "-6", "A"),
            ("Which is a polynomial?", "x^2+2x+1", "2^x", "log(x)", "sin(x)", "A"),
        ],
        (11, 'Physics'): [
            ("What is projectile motion?", "Motion under gravity", "Circular motion", "Random motion", "No motion", "A"),
            ("What is the acceleration due to gravity?", "9.8 m/s^2", "10 m/s^2", "1 m/s^2", "0 m/s^2", "A"),
            ("What is velocity?", "Speed with direction", "Speed", "Distance", "Force", "A"),
            ("What is energy?", "Ability to do work", "Force", "Mass", "Power", "A"),
        ],
        (11, 'Chemistry'): [
            ("What is a period in the periodic table?", "A row", "A column", "A group", "A block", "A"),
            ("What is ionic bonding?", "Transfer of electrons", "Sharing of electrons", "No electrons", "Protons only", "A"),
            ("What is HCl?", "Hydrochloric acid", "Water", "Salt", "Base", "A"),
            ("What is the pH of a neutral solution?", "7", "0", "14", "1", "A"),
        ],
        (11, 'Computer Science'): [
            ("What is a stack?", "LIFO structure", "FIFO structure", "Array", "Queue", "A"),
            ("What is a queue?", "FIFO structure", "LIFO structure", "Stack", "Tree", "A"),
            ("What is a function?", "Reusable block of code", "A variable", "A loop", "A class", "A"),
            ("What is an array?", "A collection of items", "A function", "A loop", "A variable", "A"),
        ],
        (12, 'Trigonometry'): [
            ("What is the inverse of sin(x)?", "arcsin(x)", "arccos(x)", "arctan(x)", "sin(x)", "A"),
            ("What is the range of arcsin(x)?", "[-π/2, π/2]", "[0, π]", "[0, 2π]", "[-π, π]", "A"),
            ("What is the period of sin(x)?", "2π", "π", "1", "0", "A"),
            ("Which is an odd function?", "sin(x)", "cos(x)", "tan(x)", "cot(x)", "A"),
        ],
        (12, 'Algebra'): [
            ("What is the derivative of x^2?", "2x", "x", "x^2", "1", "A"),
            ("What is the integral of 1/x?", "ln|x|", "x", "1/x", "x^2/2", "A"),
            ("What is the limit of (1+1/n)^n as n→∞?", "e", "1", "0", "∞", "A"),
            ("Which is a logarithmic function?", "log(x)", "x^2", "e^x", "sin(x)", "A"),
        ],
        (12, 'Physics'): [
            ("What is Faraday's law about?", "Electromagnetic induction", "Gravity", "Thermodynamics", "Optics", "A"),
            ("What is the unit of magnetic field?", "Tesla", "Newton", "Joule", "Watt", "A"),
            ("What is Ohm's law?", "V=IR", "F=ma", "E=mc^2", "P=IV", "A"),
            ("What is the speed of light?", "3x10^8 m/s", "3x10^6 m/s", "3x10^5 m/s", "3x10^7 m/s", "A"),
        ],
        (12, 'Chemistry'): [
            ("What is a hydrocarbon?", "Compound of H and C", "Compound of H and O", "Compound of C and O", "Compound of N and O", "A"),
            ("What is a polymer?", "Large molecule", "Small molecule", "Atom", "Ion", "A"),
            ("What is the chemical symbol for sodium?", "Na", "S", "So", "N", "A"),
            ("What is Avogadro's number?", "6.02x10^23", "6.02x10^22", "6.02x10^24", "6.02x10^21", "A"),
        ],
        (12, 'Computer Science'): [
            ("What is a class?", "Blueprint for objects", "A function", "A variable", "A loop", "A"),
            ("What is SQL used for?", "Databases", "Websites", "Games", "Graphics", "A"),
            ("What is inheritance?", "OOP concept", "A loop", "A variable", "A function", "A"),
            ("What is a constructor?", "Initializes objects", "Destroys objects", "Creates variables", "Runs loops", "A"),
        ],
    }

    for (grade, subject), questions in quiz_data.items():
        tasks = db.get_tasks_by_grade(grade)
        task_id = None
        for t in tasks:
            if t[3] == subject:
                task_id = t[0]
                break
        if task_id:
            for q in questions:
                qtext, a, b, c, d, correct = q
                options = [(a, 'A'), (b, 'B'), (c, 'C'), (d, 'D')]
                random.shuffle(options)
                shuffled_opts = [opt[0] for opt in options]
                correct_letter = [opt[1] for opt in options].index(correct)
                correct_option = ['A', 'B', 'C', 'D'][correct_letter]
                db.add_question(task_id, qtext, *shuffled_opts, correct_option)
            print(f"Added questions for {subject} grade {grade}")
        else:
            print(f"No task found for {subject} grade {grade}")

if __name__ == "__main__":
    seed_all_quiz_questions()
