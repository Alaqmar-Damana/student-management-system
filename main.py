from sql import DBObject
from flask import Flask, render_template, request, send_file, session, redirect, url_for, flash
import re
import json

app = Flask(__name__)

db_obj = DBObject('sample.db')

msg = "No data present yet!"
success_msg = "Item successfully inserted!"
fail_msg = "Unable to insert item, probable duplication of primary key."
del_msg = "Entry successfully deleted!"
del_fail = "Failed to delete entry."
invalid_usn = 'USN format is invalid!'
invalid_code = 'Subject code format is invalid!'

def validate_usn(usn):
    return re.match('\d[a-zA-Z]{2}(18|19|20|21|22)[a-zA-Z]{2}\d{3}', usn)

def validate_code(code):
    return re.match('\d{2}[A-Z]{2,3}\d{2}', code)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def students():
    usn = request.args.get('usn-search')
    if usn != None:
        return render_template('stud.html', data=db_obj.get_students_by_usn(usn), headings=db_obj.get_headings('students'), msg=msg)
    return render_template('stud.html', data=db_obj.get_students(), headings=db_obj.get_headings('students'), msg=msg)

@app.route('/students/<string:usn>', methods=['POST'])
def delete_stud(usn):
    try:
        if db_obj.del_students(usn):
            return render_template('stud.html', data=db_obj.get_students(), headings=db_obj.get_headings('students'), del_msg = del_msg)
        else:
            return render_template('stud.html', data=db_obj.get_students(), headings=db_obj.get_headings('students'), del_fail = del_fail)
    except:
        return redirect(url_for(students))

# @app route

@app.route('/subjects', methods=['GET', 'POST'])
def subjects():
    return render_template('sub.html', data=db_obj.get_subjects(), headings=db_obj.get_headings('subjects'), msg=msg)

@app.route('/subjects/<string:code>', methods=['POST'])
def delete_sub(code):
    try:
        if db_obj.del_subjects(code):
            return render_template('sub.html', data=db_obj.get_subjects(), headings=db_obj.get_headings('subjects'), del_msg = del_msg)
        else:
            return render_template('sub.html', data=db_obj.get_subjects(), headings=db_obj.get_headings('subjects'), del_fail = del_fail)
    except:
        return redirect(url_for(subjects))

@app.route('/departments', methods=['GET', 'POST'])
def departments():
    return render_template('dept.html', data=db_obj.get_departments(), headings=db_obj.get_headings('departments'), msg=msg)

@app.route('/departments/<string:id>', methods=['POST'])
def delete_dept(id):
    try:
        if db_obj.del_departments(id):
            return render_template('dept.html', data=db_obj.get_departments(), headings=db_obj.get_headings('departments'), del_msg = del_msg)
        else:
            return render_template('dept.html', data=db_obj.get_departments(), headings=db_obj.get_headings('departments'), del_fail = del_fail)
    except:
        return redirect(url_for(departments))

@app.route('/marks', methods=['GET', 'POST'])
def marks():
    return render_template('marks.html', data=db_obj.get_marks(), headings=db_obj.get_headings('marks'), msg=msg)

@app.route('/marks/<string:str>', methods=['POST'])
def delete_marks(str):
    try:
        if db_obj.del_marks(str):
            return render_template('marks.html', data=db_obj.get_marks(), headings=db_obj.get_headings('marks'), del_msg = del_msg)
        else:
            return render_template('marks.html', data=db_obj.get_marks(), headings=db_obj.get_headings('marks'), del_fail = del_fail)
    except:
        return redirect(url_for(marks))

@app.route('/activities', methods=['GET', 'POST'])
def activities():
    return render_template('act.html', data=db_obj.get_activities(), headings=db_obj.get_headings('activities'), msg=msg)

@app.route('/activities/<string:id>', methods=['POST'])
def delete_act(id):
    try:
        if db_obj.del_activity(id):
            return render_template('act.html', data=db_obj.get_activities(), headings=db_obj.get_headings('activities'), del_msg = del_msg)
        else:
            return render_template('act.html', data=db_obj.get_activities(), headings=db_obj.get_headings('activities'), del_fail = del_fail)
    except:
        return redirect(url_for(activities))

@app.route('/participation', methods=['GET', 'POST'])
def participation():
    usn = request.args.get('usn-search')
    if usn != None:
        return render_template('part.html', data=db_obj.get_participation_details_by_usn(usn), headings=db_obj.get_participation_headings(), msg=msg)
    return render_template('part.html', data=db_obj.get_participation_details(), headings=db_obj.get_participation_headings(), msg=msg)

@app.route('/participation/<string:str>', methods=['POST'])
def delete_part(str):
    try:
        if db_obj.del_participation(str):
            return render_template('part.html', data=db_obj.get_participation_details(), headings=db_obj.get_participation_headings(), del_msg = del_msg)
        else:
            return render_template('part.html', data=db_obj.get_participation_details(), headings=db_obj.get_participation_headings(), del_fail = del_fail)
    except:
        return redirect(url_for(participation))

@app.route('/studForm', methods=['GET', 'POST'])
def stud_form():
    if request.method == 'POST':
        usn, name, d_id, ph, sec = request.form['usn'], request.form['name'], request.form['dept_id'], request.form['number'], request.form['sec']
        if not validate_usn(usn):
            return render_template('studForm.html', depts=db_obj.get_departments(), fail_msg=invalid_usn)
        usn = usn.upper()
        insert_success = db_obj.insert_students({'usn': usn, 'name': name, 'dept_id': d_id, 'ph': ph, 'sec': sec})
        if insert_success:
            return render_template('studForm.html', depts=db_obj.get_departments(), msg=success_msg)
        else:
            return render_template('studForm.html', depts=db_obj.get_departments(), fail_msg=fail_msg)
    else:
        return render_template('studForm.html', depts=db_obj.get_departments())

@app.route('/deptForm', methods=['GET', 'POST'])
def dept_form():
    if request.method == 'POST':
        id, name = request.form['id'], request.form['name']
        insert_success = db_obj.insert_departments({'id': id, 'name': name})
        if insert_success:
            return render_template('deptForm.html', msg=success_msg)
        else:
            return render_template('deptForm.html', fail_msg=fail_msg)
    else:
        return render_template('deptForm.html')

@app.route('/subForm',methods = ['GET','POST'])
def sub_form():
    if request.method == 'POST':
        code, name, sem = request.form['subcode'],request.form['subname'],request.form['sem']
        code = code.upper()
        if not validate_code(code):
            return render_template('subForm.html', fail_msg=invalid_code)
        insert_success = db_obj.insert_subjects({'code': code, 'name': name, 'sem':sem})
        if insert_success:
            return render_template('subForm.html', msg=success_msg)
        else:
            return render_template('subForm.html', fail_msg=fail_msg)
    else:
        return render_template('subForm.html')

@app.route('/marksForm',methods = ['GET','POST'])
def marks_form():
    if request.method == 'POST':
        usn, code, marks, result = request.form['usn'],request.form['code'],request.form['marks'], request.form['result']
        insert_success = db_obj.insert_marks({'usn': usn, 'code': code, 'marks': marks, 'result': result})
        if insert_success:
            return render_template('marksForm.html', students=db_obj.get_students(), subjects=db_obj.get_subjects(), msg=success_msg)
        else:
            return render_template('marksForm.html', students=db_obj.get_students(), subjects=db_obj.get_subjects(), fail_msg=fail_msg)
    else:
        return render_template('marksForm.html', students=db_obj.get_students(), subjects=db_obj.get_subjects())

@app.route('/actForm', methods=['GET', 'POST'])
def act_form():
    if request.method == 'POST':
        id, guide, type, cat, name, mode, place, ext, start, end, days, cert, report = request.form['id'], request.form['guide'], request.form['type'], request.form['cat'], request.form['name'], request.form['mode'], request.form['place'], request.form['ext'], request.form['start'], request.form['end'], request.form['days'], request.form['cert'], request.form['report']
        if id=="":
            return render_template('actForm.html', fail_msg='Activity ID cannot be empty!')
        insert_success = db_obj.insert_activities({'id': id,'guide': guide,'type': type,'cat': cat,'name': name,'mode': mode,'place': place,'ext': ext,'start': start,'end': end,'days': days,'cert': cert,'report': report})
        if insert_success:
            return render_template('actForm.html', msg=success_msg)
        else:
            return render_template('actForm.html', fail_msg=fail_msg)
    else:
        return render_template('actForm.html')

@app.route('/partForm', methods=['GET', 'POST'])
def part_form():
    if request.method == 'POST':
        id, usn = request.form['id'], request.form['usn']
        insert_success = db_obj.insert_participation({'id': id, 'usn': usn})
        if insert_success:
            return render_template('partForm.html', activities=db_obj.get_activities(), students=db_obj.get_students(), msg=success_msg)
        else:
            return render_template('partForm.html', activities=db_obj.get_activities(), students=db_obj.get_students(), fail_msg=fail_msg)
    else:
        return render_template('partForm.html', activities=db_obj.get_activities(), students=db_obj.get_students())

@app.route('/bg', methods=['GET'])
def body_bg():
    filename = './assets/img/wallpaper.png'
    return send_file(filename, mimetype='image/png')

@app.route('/logo', methods=['GET'])
def logo_img():
    filename = './assets/img/logo.png'
    return send_file(filename, mimetype='image/png')

@app.route('/count', methods=['GET'])
def count():
    return render_template('count.html', headings=db_obj.get_headings('total_count'), content=db_obj.get_count())

@app.errorhandler(404)
def notfound(e):
    return render_template('404.html')

app.run(debug=True)