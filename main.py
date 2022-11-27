from flask import Flask,render_template,session,request,redirect,url_for
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password='vedarth12',
  database = 'final_dbms'
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

@app.route("/add_Patient_page",methods = ['POST','GET'])
def add_Patient_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from PATIENT"
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('addPatient.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

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
            if field not in ['Patient_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)

    qry = "INSERT INTO Patient(Name, Date_of_Birth, Gender, Phone_no, Address, organ_req, reason_of_procurement, Doctor_Name) Values (%s,%s,%s,%s,%s,%s,%s,%s)"%val
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

    return redirect(url_for('add_Patient_page', id='Patient', error=error,success=success))

@app.route("/add_PatientMH_page",methods = ['POST','GET'])
def add_PatientMH_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Patient_Medical_History"
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('addPatientMH.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_PatientMH", methods=['POST','GET'])
def add_PatientMH():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Patient_Medical_History"
    mycursor.execute(qry)
    fields = mycursor.column_names
    
    val = ()

    for field in fields:
        temp = request.form.get(field)    
        if field not in ['Patient_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Patient_Medical_History(Patient_ID, Diabetes, High_Blood_Pressure, High_Cholesterol, Asthma, Hypothyroidism) Values (%s,%s,%s,%s,%s,%s)"%val
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

    return redirect(url_for('add_PatientMH_page', id='PatientMH', error=error,success=success))

@app.route("/add_Donor_page",methods = ['POST','GET'])
def add_Donor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from DONOR"
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('addDonor.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

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
            if field not in ['Donor_ID','Organization_ID','Relative_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)

    qry = "INSERT INTO Donor(Name, Date_Of_Birth, Gender, Phone_no, EnzymeTest, BloodTest, Address, organ_donate, Organization_ID, Relative_ID) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%val
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

    return redirect(url_for('add_Donor_page', id='Donor', error=error,success=success))


@app.route("/add_DonorMH_page",methods = ['POST','GET'])
def add_DonorMH_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Donor_Medical_History"
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('addDonorMH.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_DonorMH", methods=['POST','GET'])
def add_DonorMH():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Donor_Medical_History"
    mycursor.execute(qry)
    fields = mycursor.column_names
    
    val = ()

    for field in fields:
        temp = request.form.get(field)    
        if field not in ['Donor_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Donor_Medical_History(Donor_ID, Diabetes, High_Blood_Pressure, High_Cholesterol, Asthma, Hypothyroidism) Values (%s,%s,%s,%s,%s,%s)"%val
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

    return redirect(url_for('add_DonorMH_page', id='DonorMH', error=error,success=success))

@app.route("/add_Relative_page",methods = ['POST','GET'])
def add_Relative_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Relative"
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('addRelative.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_Relative", methods=['POST','GET'])
def add_Relative():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Relative"
    mycursor.execute(qry)
    fields = mycursor.column_names
    
    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Relative_ID']:    
            if field not in ['Relative_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)

    qry = "INSERT INTO Relative(Rel_Name, Gender, relation) Values (%s,%s,%s)"%val
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

    return redirect(url_for('add_Relative_page', id='Donor', error=error,success=success))

@app.route("/add_Doctor_page",methods = ['POST','GET'])
def add_Doctor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Doctor"
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('addDoctor.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

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
            if field not in ['Donor_ID','Organization_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)

    qry = "INSERT INTO Doctor(Doctor_Name, Gender, Phone_no, Department_Name, Organization_ID) Values (%s,%s,%s,%s,%s)"%val
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

    return redirect(url_for('add_Doctor_page', id='Doctor', error=error,success=success))

@app.route("/add_Transaction_page",methods = ['POST','GET'])
def add_Transaction_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Transaction"
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('addTransaction.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_Transaction", methods=['POST','GET'])
def add_Transaction_head():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Transaction"
    mycursor.execute(qry)

    mycursor.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Transaction(Patient_ID,Donor_ID,Organ_ID,Status,Date_of_Transaction) Values (%s,%s,%s,%s,\'%s\')"%(request.form['Patient_ID'],request.form['Donor_ID'],request.form['Organ_ID'],request.form['Status'],request.form['Date_of_Transaction'])
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False

    qry_insert = "delete from Organ_available where Organ_ID = %s "%request.form['Organ_ID']

    mycursor.execute(qry_insert)

    mycursor.execute("COMMIT;")

    mydb.commit()

    return redirect(url_for('add_Transaction_page', id='Transaction', error=error,success=success))

@app.route("/add_futuredonor_page",methods = ['POST','GET'])
def add_futuredonor_page():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Future_Donor"
    mycursor.execute(qry)
    fields = mycursor.column_names

    return render_template('addFutureDonor.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

@app.route("/add_futuredonor", methods=['POST','GET'])
def add_futuredonor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Future_Donor"
    mycursor.execute(qry)
    fields = mycursor.column_names
    val = ()
    for field in fields:
        temp = request.form.get(field)
        if field not in ['Future_Donor_ID']:        
            if field not in ['Future_Donor_ID'] and temp != '':
                temp = "\'"+temp+"\'"
            if temp == '':
                temp = 'NULL'
            val = val + (temp,)
    
    mycursor.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Future_Donor(Name, Gender, Date_of_Birth, Address, organ) Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycursor.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
        
    mycursor.execute("COMMIT;")

    mydb.commit()
    
    return redirect( url_for('home') )


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

@app.route("/search_Relative_details",methods=['GET','POST'])
def search_Relative_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Relative"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_Future_Donor_details",methods=['GET','POST'])
def search_Future_Donor_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from Future_Donor"
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
    qry = "Select Name, DATE_FORMAT(FROM_DAYS(DATEDIFF(now(), Date_Of_Birth)), '%Y')+0 AS Age, organ from Future_Donor where Future_Donor_ID="+str(request.form['Donor_ID'])
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
        return redirect( url_for('home'))
    qry = "Select Name, DATE_FORMAT(FROM_DAYS(DATEDIFF(now(), Date_Of_Birth)), '%Y')+0 AS Age, organ, curdate() from Future_Donor where Future_Donor_ID="+str(request.form['Donor_ID'])
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()

    return render_template('/donationcard.html',res=res,fields=fields)

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
        if field not in ['Patient_ID']:
            if request.form[field] not in ['None','']:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
            else:
                qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Name = \'%s\';" %(request.form['Name'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from Patient WHERE Name = \'%s\';" %(request.form['Name'])
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
            if field in ['Organization_ID','Donor_ID', 'Relative_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Name = %s;" %(request.form['Name'])
    print(qry)
    try:
        mycursor.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from Patient WHERE Donor_ID = %s;" %(request.form['Donor_ID'])
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
    qry = qry + "WHERE Doctor_Name = %s;" %(request.form['Doctor_Name'])
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


#----------------------------Remove-----------------------------------------

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


#----------------Actual Deletion from database------------------------


@app.route('/del_donor',methods=['GET','POST'])
def del_donor():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "delete from Donor where Donor_ID="+str(request.form['Donor_ID'])+" and organ_donate=\'%s\'" %request.form['organ_donate']
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

#----------------------------Logs------------------------------------------
@app.route("/search_patient_log",methods=['GET','POST'])
def search_patient_log_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from patient_log"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_donor_log",methods=['GET','POST'])
def search_donor_log_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from donor_log"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_organ_log",methods=['GET','POST'])
def search_organ_log_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from organ_log"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

@app.route("/search_transaction_log",methods=['GET','POST'])
def search_transaction_log_details():
    if not session.get('login'):
        return redirect( url_for('home') )
    qry = "SELECT * from transaction_log"
    mycursor.execute(qry)
    fields = mycursor.column_names
    res = mycursor.fetchall()
    return render_template('/search_and_show_list.html',res=res,fields=fields)

#----------------------------Logout-----------------------------------------
@app.route("/logout", methods=['POST','GET'])
def logout():
    session['login'] = False
    session['isAdmin'] = False
    return redirect("/login")


if __name__ == "__main__":
    app.secret_key = 'sec key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
