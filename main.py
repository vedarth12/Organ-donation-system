from flask import Flask,render_template,session,request,redirect,url_for
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password='vedarth12',
  database = 'new_dbms'
)
mycursor = mydb.cursor(buffered=True)

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
@app.route("/home",methods = ['POST','GET'])
def home():
    if not session.get('login'):
        return render_template('login.html'),401
    else:
        if session.get('isAdmin') :
            return render_template('home.html',username=session.get('username'))
        else :
            return home()

@app.route("/login",methods = ['GET','POST'])
def login():
    if request.method=='POST' :
        query = """SELECT * FROM login WHERE username = '%s'""" %(request.form['username'])
        mycursor.execute(query)
        res = mycursor.fetchall()
        if mycursor.rowcount == 0:
            return home()
        if request.form['password'] != res[0][1]:
            return render_template('login.html')
        else:
            session['login'] = True
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            session['isAdmin'] = (request.form['username']=='admin')
            return home()
    return render_template('login.html')

#--------------Adding Information----------------------------

@app.route("/add_<id>_page",methods = ['POST','GET'])
def add_page(id):
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from " + id.capitalize()
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('add_page.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_<id>_page2",methods = ['POST','GET'])
def add_page2(id):
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from " + id.capitalize()
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('add_page2.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_Patient", methods=['POST','GET'])
def add_Patient():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Patient"
    mycursor.execute(qry)
    fields = mycursor.column_names
    
    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Patient_ID']:    
            if field not in ['Patient_ID','Doctor_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)

    qry = "INSERT INTO Patient(Name, Date_of_Birth, Medical_insurance, Medical_history, Street, City, State, organ_req, reason_of_procurement, Doctor_ID) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Patient', error=error,success=success))

@app.route("/add_patient_emergency_phone", methods=['POST','GET'])
def add_patient_emergency_phone():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from patient_emergency_phone"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Patient_ID','emergency_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO patient_emergency_phone Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : Patient not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page2', id='patient_emergency_phone', error=error,success=success))


@app.route("/add_Donor", methods=['POST','GET'])
def add_Donor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Donor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    val = ()
    for field in fields:
        temp = request.form.get(field)
        if field not in ['Donor_ID']:        
            if field not in ['Donor_ID','Organization_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)
    
    mycursor.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Donor(Name, Date_of_Birth, Medical_insurance, Medical_history, Street, City, State, organ_donated, date_of_death, Organization_ID) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
        
    mycursor.callproc('add_organ')

    mycursor.execute("COMMIT;")

    mydb.commit()

    
    return redirect(url_for('add_page', id='Donor', error=error,success=success))

@app.route("/add_donor_emergency_phone", methods=['POST','GET'])
def add_donor_emergency_phone():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from donor_emergency_phone"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Donor_ID','emergency_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO donor_emergency_phone Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : Donor not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page2', id='donor_emergency_phone', error=error,success=success))


@app.route("/add_Doctor", methods=['POST','GET'])
def add_Doctor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Doctor_ID']:
            if field not in ['Doctor_ID','organization_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)

    qry = "INSERT INTO Doctor(Doctor_Name, Department_Name, organization_ID) Values (%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Doctor', error=error,success=success))

@app.route("/add_Doctor_phone_no", methods=['POST','GET'])
def add_Doctor_phone_no():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor_phone_no"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Doctor_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Doctor_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page2', id='Doctor_phone_no', error=error,success=success))

@app.route("/add_Organization", methods=['POST','GET'])
def add_Organization():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Organization_ID']:
            if field not in ['Government_approved','Organization_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)

    qry = "INSERT INTO Organization(Organization_name, Location, Government_approved) Values (%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Organization', error=error,success=success))

@app.route("/add_Organization_phone_no", methods=['POST','GET'])
def add_Organization_phone_no():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization_phone_no"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Organization_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organization_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page2', id='Organization_phone_no', error=error,success=success))

@app.route("/add_Organization_head", methods=['POST','GET'])
def add_Organization_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization_head"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Employee_ID','Term_length','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organization_head Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page2', id='Organization_head', error=error,success=success))

@app.route("/add_Transaction", methods=['POST','GET'])
def add_Transaction_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Transaction"
    mycursor.execute(qry)
    fields = mycursor.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Patient_ID','Donor_ID','Status','Organ_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    mycursor.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Transaction Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False

    qry_insert = "delete from Organ_available where Organ_ID = %s "%val[1]

    mycursor.execute(qry_insert)

    mycursor.execute("COMMIT;")

    mydb.commit()

    return redirect(url_for('add_page2', id='Transaction', error=error,success=success))

#----------------------------Search-----------------------------------------

@app.route("/search_detail",methods = ['POST','GET'])
def search_detail():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('search_detail.html')

#----------------------------Update-----------------------------------------

    
@app.route("/update_patient_page",methods = ['POST','GET'])
def update_patient_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Patient"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_patient_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_patient_details",methods = ['GET','POST'])
def update_patient_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Patient")
    fields = mycursor.column_names
    qry = "UPDATE Patient SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Doctor_ID','Patient_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Patient_ID = %s and organ_req = \'%s\';" %(request.form['Patient_ID'],request.form['organ_req'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from Patient WHERE Patient_ID = %s and organ_req = \'%s\';" %(request.form['Patient_ID'],request.form['organ_req'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    print(res)
    print(qry2)
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_donor_page",methods = ['POST','GET'])
def update_donor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Donor"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_donor_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_donor_details",methods = ['GET','POST'])
def update_donor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Donor")
    fields = mycursor.column_names
    qry = "UPDATE Donor SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Organization_ID','Donor_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Donor_ID = %s and organ_donated = \"%s\";" %(request.form['Donor_ID'],request.form['organ_donated'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from Patient WHERE Donor_ID = %s and organ_donated = \"%s\";" %(request.form['Donor_ID'],request.form['organ_donated'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    print(res)
    print(qry2)
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_doctor_page",methods = ['POST','GET'])
def update_doctor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Doctor"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_doctor_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_doctor_details",methods = ['GET','POST'])
def update_doctor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Doctor")
    fields = mycursor.column_names
    qry = "UPDATE Doctor SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['Doctor_ID','Organization_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Doctor_ID = %s;" %(request.form['Doctor_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
        return render_template('error_page.html')
    mydb.commit()
    qry2 = "select * from Doctor WHERE Doctor_ID = %s;" %(request.form['Doctor_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_organization_page",methods = ['POST','GET'])
def update_organization_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry_upd = "Select * from Organization"
    mycursor.execute(qry_upd)
    fields_upd = mycursor.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_organization_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_organization_details",methods = ['GET','POST'])
def update_organization_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    mycursor.execute("SELECT * from Organization")
    fields = mycursor.column_names
    qry = "UPDATE Organization SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['Organization_ID','Government_approved']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Organization_ID = %s;" %(request.form['Organization_ID'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
        return render_template('error_page.html')
    mydb.commit()
    qry2 = "select * from Organization WHERE Organization_ID = %s;" %(request.form['Organization_ID'])
    mycursor.execute(qry2)
    res = mycursor.fetchone()
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

#----------------------------Remove-----------------------------------------

@app.route('/remove_patient',methods=['GET','POST'])
def remove_patient():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_patient.html')

@app.route('/remove_donor',methods=['GET','POST'])
def remove_donor():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_donor.html')

@app.route('/remove_doctor',methods=['GET','POST'])
def remove_doctor():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_doctor.html')

@app.route('/remove_organization',methods=['GET','POST'])
def remove_organization():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_organization.html')

@app.route('/remove_organization_head',methods=['GET','POST'])
def remove_organization_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/remove_organization_head.html')


#----------------Actual Deletion from database------------------------

@app.route('/del_patient',methods=['GET','POST'])
def del_patient():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Patient where Patient_ID="+str(request.form['Patient_ID'])+" and organ_req=\'%s\'"%(request.form['organ_req'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )

@app.route('/del_donor',methods=['GET','POST'])
def del_donor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Donor where Donor_ID="+str(request.form['Donor_ID'])+" and organ_donated=\'%s\'" %request.form['organ_donated']
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )


@app.route('/del_doctor',methods=['GET','POST'])
def del_doctor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Doctor where Doctor_ID="+str(request.form['Doctor_ID'])
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )


@app.route('/del_organization',methods=['GET','POST'])
def del_organization():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Organization where Organization_ID="+str(request.form['Organization_ID'])
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )


@app.route('/del_organization_head',methods=['GET','POST'])
def del_organization_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Organization_head where Organization_ID="+str(request.form['Organization_ID'])+" and Employee_ID="+str(request.form['Employee_ID'])
    try:
        mycursor.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('home') )

#----------------------------Logout-----------------------------------------
@app.route("/logout", methods=['POST','GET'])
def logout():
    session['login'] = False
    session['isAdmin'] = False
    return redirect("/login")

#-------------------generatecertificate---------------------------

@app.route('/get_id',methods=['GET','POST'])
def get_id():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/getid.html')

@app.route("/generate_document",methods=['GET','POST'])
def display_donor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "Select Name, DATE_FORMAT(FROM_DAYS(DATEDIFF(now(), Date_Of_Birth)), '%Y')+0 AS Age, organ_donated from Donor where Donor_ID="+str(request.form['Donor_ID'])
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/donationcert.html',res=res,fields=fields)

#-----------------------GenerateCard----------------------------------

@app.route('/get_id2',methods=['GET','POST'])
def get_id2():
    if not session.get('login'):
        return redirect( url_for('home') )
    return render_template('/getid2.html')

@app.route("/generate_card",methods=['GET','POST'])
def generate_card():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "Select Name, DATE_FORMAT(FROM_DAYS(DATEDIFF(now(), Date_Of_Birth)), '%Y')+0 AS Age, organ_donated, curdate() from Donor where Donor_ID="+str(request.form['Donor_ID'])
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/donationcard.html',res=res,fields=fields)

#-----------------------Searching Information------------------------------

@app.route("/search_Patient_details",methods=['GET','POST'])
def search_Patient_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Patient"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Donor_details",methods=['GET','POST'])
def search_Donor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Donor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Organ_details",methods=['GET','POST'])
def search_Organ_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organ_available"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Organization_details",methods=['GET','POST'])
def search_Organization_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Organization_head_details",methods=['GET','POST'])
def search_Organization_head_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Organization_head"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Doctor_details",methods=['GET','POST'])
def search_Doctor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Transaction",methods=['GET','POST'])
def search_Transaction_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Transaction"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_log",methods=['GET','POST'])
def search_log_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from log"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

if __name__ == "__main__":
    app.secret_key = 'sec key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
