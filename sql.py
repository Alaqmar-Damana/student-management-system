import sqlite3

class DBObject:
    tables = ["students", "subjects", "departments", "marks", "activities", "participation", "total_count"]
    schemas = {"departments" : "departments(DEPT_ID VARCHAR(10) PRIMARY KEY,DEPT_NAME VARCHAR(10))",
    "students":"students(USN VARCHAR(15) PRIMARY KEY, NAME VARCHAR(20), DEPT_ID VARCHAR(10) REFERENCES departments(DEPT_ID), PHONE_NO INTEGER(10), SECTION CHAR(10))",
    "subjects" : "subjects(SUBCODE VARCHAR(10) PRIMARY KEY,SUBNAME VARCHAR(25),SEM INTEGER(1))",
    "marks" : "marks(USN VARCHAR(15),SUBCODE VARCHAR(10),MARKS INTEGER(3),RESULT CHAR(6),FOREIGN KEY (USN) REFERENCES STUDENTS(USN),FOREIGN KEY (SUBCODE) REFERENCES SUBJECTS(SUBCODE),PRIMARY KEY(USN,SUBCODE))",
    "activities" : "activities(ACT_ID VARCHAR(10) PRIMARY KEY, GUIDE VARCHAR(100), TYPE VARCHAR(100), CATEGORY VARCHAR(100), ACT_NAME VARCHAR(100), MODE VARCHAR(100), PLACE VARCHAR(100), EXTGUIDE VARCHAR(100), COMMENCEMENT VARCHAR(100), COMPLETION VARCHAR(100), DAYS VARCHAR(100), CERTIFICATE VARCHAR(100), REPORT VARCHAR(100))",
    "participation" : "participation(ACT_ID VARCHAR(10),USN VARCHAR(10),FOREIGN KEY (ACT_ID) REFERENCES activities(ACT_ID),FOREIGN KEY (USN) REFERENCES STUDENTS(USN), PRIMARY KEY(ACT_ID, USN))",
    "total_count" : "total_count(ENTITY VARCHAR(20) PRIMARY KEY, TOTAL INTEGER)"}

    table_headings = {"students" : ["USN", "NAME", "DEPT_ID", "PHONE NO.", "SEC"],
    "subjects": ["SUB_CODE","SUB_NAME","SEM"],
    "departments": ["DEPT_ID","DEPT_NAME"],
    "marks": ["USN","SUB_CODE","MARKS","RESULT"],
    "activities":["ActID", "Guide", "Type", "Category", "ActName", "Mode", "Place", "ExtGuide", "Commencement","Completion", "Days", "Certification", "Report"],
    "participation": ["ACT_ID","USN"],
    "total_count": ["ENTITY", "COUNT"]}

    rows_for_total = ['Students', 'Subjects', 'Departments']

    #for creation of tables
    def __init__(self, fname):
        self.conn = sqlite3.connect(fname, check_same_thread=False)
        self.curr = self.conn.cursor()
        self.existing_tables = set(tname[0] for tname in self.curr.execute("SELECT name FROM sqlite_master WHERE TYPE='table'"))
        for table in self.tables:
            if table not in self.existing_tables:
                self.curr.execute(f"CREATE TABLE {self.schemas[table]}")
        self.conn.commit()
        for row in self.rows_for_total:
            self.curr.execute(f"INSERT OR IGNORE INTO total_count VALUES('{row}', 0)")
        self.conn.commit()
        self.make_triggers()
        self.conn.commit()
        

    def get_headings(self, table_name):
        return self.table_headings[table_name]

    def insert_students(self, obj):
        if obj["usn"] == "":
            return False
        try:
            self.curr.execute(f"INSERT INTO students VALUES ('{obj['usn']}', '{obj['name']}', '{obj['dept_id']}', '{obj['ph']}', '{obj['sec']}')")
            self.conn.commit()
            return True
        except:
            return False

    def get_students(self):
        return self.curr.execute("SELECT * FROM students").fetchall()
    
    def get_students_by_usn(self, usn):
        return self.curr.execute(f"SELECT * FROM students WHERE usn LIKE '%{usn.upper()}%'").fetchall()
    
    def del_students(self, usn):
        try:
            self.curr.execute(f"DELETE FROM students WHERE usn='{usn}'")
            # delete marks and participation records
            self.del_marks_by_usn(usn)
            self.del_participation_by_usn(usn)
            self.conn.commit()
            return True
        except:
            return False

    def insert_subjects(self, obj):
        if obj["code"] == "":
            return False
        try:
            self.curr.execute(f"INSERT INTO subjects VALUES ('{obj['code']}', '{obj['name']}', '{obj['sem']}')")
            self.conn.commit()
            return True
        except:
            return False

    def get_subjects(self):
        return self.curr.execute("SELECT * FROM subjects").fetchall()

    def del_subjects(self, code):
        try:
            self.curr.execute(f"DELETE FROM subjects WHERE subcode='{code}'")
            # delete marks records
            self.del_marks_by_subject(code)
            self.conn.commit()
            return True
        except:
            return False

    def insert_departments(self, obj):
        if obj["id"] == "":
            return False
        try:
            self.curr.execute(f"INSERT INTO departments VALUES ('{obj['id']}', '{obj['name']}')")
            self.conn.commit()
            return True
        except:
            return False

    def get_departments(self):
        return self.curr.execute("SELECT * FROM departments").fetchall()

    def del_departments(self, id):
        try:
            self.curr.execute(f"DELETE FROM departments WHERE dept_id='{id}'")
            # delete students under this department
            usns = self.curr.execute(f"SELECT usn FROM students WHERE dept_id='{id}'").fetchall()
            for usn in usns:
                self.del_students(usn[0])
            self.conn.commit()
            return True
        except:
            return False

    def insert_marks(self, obj):
        try:
            print(obj)
            self.curr.execute(f"INSERT INTO marks VALUES ('{obj['usn']}', '{obj['code']}', '{obj['marks']}', '{obj['result']}')")
            self.conn.commit()
            return True
        except:
            return False

    def get_marks(self):
        return self.curr.execute("SELECT * FROM marks").fetchall()
    
    def del_marks(self, str):
        try:
            usn, subcode = str.split()
            self.curr.execute(f"DELETE FROM marks WHERE usn='{usn}' AND subcode='{subcode}'")
            self.conn.commit()
            return True
        except:
            return False

    def del_marks_by_usn(self, usn):
        try:
            self.curr.execute(f"DELETE FROM marks WHERE usn='{usn}'")
            self.conn.commit()
            return True
        except:
            return False
    
    def del_marks_by_subject(self, subcode):
        try:
            self.curr.execute(f"DELETE FROM marks WHERE subcode='{subcode}'")
            self.conn.commit()
            return True
        except:
            return False

    def insert_activities(self, obj):
        try:
            self.curr.execute(f"INSERT INTO activities VALUES ('{obj['id']}', '{obj['guide']}', '{obj['type']}', '{obj['cat']}', '{obj['name']}', '{obj['mode']}', '{obj['place']}', '{obj['ext']}', '{obj['start']}', '{obj['end']}', '{obj['days']}', '{obj['cert']}', '{obj['report']}')")
            self.conn.commit()
            return True
        except:
            return False

    def get_activities(self):
        return self.curr.execute("SELECT * FROM activities").fetchall()

    def del_activity(self, id):
        try:
            self.curr.execute(f"DELETE FROM activities WHERE act_id='{id}'")
            # delete participation records
            self.del_participation_by_act_id(id)
            self.conn.commit()
            return True
        except:
            return False

    def insert_participation(self, obj):
        try:
            self.curr.execute(f"INSERT INTO participation VALUES ('{obj['id']}', '{obj['usn']}')")
            self.conn.commit()
            return True
        except:
            return False

    # def get_participation(self):
    #     return self.curr.execute("SELECT * FROM participation").fetchall()
    
    def get_participation_details(self):
        # part = self.get_participation()
        # details = list()
        # for i in range(len(part)):
        #     details.append([part[i][0], i+1])
        #     stu_details = self.curr.execute(f"select name from students where usn='{part[i][1]}'").fetchone()
        #     details[i] += [part[i][1], stu_details[0]]
        #     act_details = self.curr.execute(f"select * from activities where act_id='{part[i][0]}'").fetchone()
        #     details[i] += list(act_details[1:])
        # return details
        return self.curr.execute('SELECT p.usn, s.name, a.guide, a.type, a.category, a.act_name, a.mode, a.place, a.extguide, a.commencement, a.completion, a.days, a.certificate, a.report FROM participation p JOIN students s, activities a WHERE p.usn = s.usn AND p.act_id = a.act_id').fetchall()
    
    # def get_participation_by_usn(self, usn):
    #     return self.curr.execute(f"SELECT * FROM participation WHERE usn LIKE '%{usn.upper()}%'").fetchall()
    
    def get_participation_details_by_usn(self, usn):
        return self.curr.execute(f"SELECT p.usn, s.name, a.guide, a.type, a.category, a.act_name, a.mode, a.place, a.extguide, a.commencement, a.completion, a.days, a.certificate, a.report FROM participation p JOIN students s, activities a WHERE p.usn LIKE '%{usn.upper()}%' AND p.usn = s.usn AND p.act_id = a.act_id").fetchall()

    def get_participation_headings(self):
        return ["USN", "Name"]+self.get_headings('activities')[1:]

    def del_participation(self, str):
        try:
            id, usn = str.split()
            self.curr.execute(f"DELETE FROM participation WHERE act_id='{id}' AND usn='{usn}'")
            self.conn.commit()
            return True
        except:
            return False

    def del_participation_by_usn(self, usn):
        try:
            self.curr.execute(f"DELETE FROM participation WHERE usn='{usn}'")
            self.conn.commit()
            return True
        except:
            return False

    def del_participation_by_act_id(self, act_id):
        try:
            self.curr.execute(f"DELETE FROM participation WHERE act_id='{act_id}'")
            self.conn.commit()
            return True
        except:
            return False
    
    def get_count(self):
        return self.curr.execute('SELECT * from total_count').fetchall()
    
    trig_names = ['stui', 'stud', 'subi', 'subd', 'depi', 'depd']
    triggers = {'stui':'''CREATE TRIGGER stui
AFTER INSERT ON students
BEGIN
    UPDATE total_count SET total = total + 1 WHERE entity = 'Students';
END;''',
    'stud':'''CREATE TRIGGER stud
AFTER DELETE ON students
BEGIN
    UPDATE total_count SET total = total - 1 WHERE entity = 'Students';
END;''',
    'subi':'''CREATE TRIGGER subi
AFTER INSERT ON subjects
BEGIN
    UPDATE total_count SET total = total + 1 WHERE entity = 'Subjects';
END;''',
    'subd':'''CREATE TRIGGER subd
AFTER DELETE ON subjects
BEGIN
    UPDATE total_count SET total = total - 1 WHERE entity = 'Subjects';
END;''',
    'depi':'''CREATE TRIGGER depi
AFTER INSERT ON departments
BEGIN
    UPDATE total_count SET total = total + 1 WHERE entity = 'Departments';
END;''',
    'depd':'''CREATE TRIGGER depd
AFTER DELETE ON departments
BEGIN
    UPDATE total_count SET total = total - 1 WHERE entity = 'Departments';
END;'''}

    def make_triggers(self):
        existing_trigs = self.curr.execute("SELECT name from sqlite_master WHERE TYPE='trigger'").fetchall()
        existing_trigs = set([trig[0] for trig in existing_trigs])
        for trig in self.trig_names:
            if trig not in existing_trigs:
                self.curr.execute(self.triggers[trig])
        self.conn.commit()
    

