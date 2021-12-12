from flask.wrappers import Request
from flask import Flask , render_template, request, redirect, url_for, session,Response
import re
import pickle
from flask_mysqldb import MySQL
import MySQLdb.cursors
from selenium import webdriver 
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from bs4 import BeautifulSoup
import base64
from PIL import Image
import io 
from keras.preprocessing.image import load_img
import numpy as np
from keras.preprocessing import image
from numpy import expand_dims
from matplotlib import pyplot
import pickle
from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from keras.utils.vis_utils import plot_model
from keras.preprocessing.image import img_to_array

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
from PIL import Image  
import PIL

from keras.models import load_model
alzheimer = load_model('alzheimer.h5')
brain_tumor = load_model('brain_tumor.h5')
breast_cancer = load_model('breast_cancer.h5')
chest_xray = load_model('chest_xray.h5')
malaria = load_model('malaria.h5')


ml_diabetes=pickle.load(open('ml_diabetes.pkl','rb'))
ml_liver=pickle.load(open('ml_liver.pkl','rb'))
ml_pcos=pickle.load(open('ml_pcos.pkl','rb'))
ml_cancer=pickle.load(open('ml_breastcancer.pkl','rb'))
ml_fetal_health=pickle.load(open('ml_fetal_health.pkl','rb'))
ml_heart=pickle.load(open('ml_heart.pkl','rb'))
ward = pickle.load(open('ward.pkl','rb'))
ward_genetic = pickle.load(open('ward_genetic.pkl','rb'))
 



app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hospital management'

# Intialize MySQL
mysql = MySQL(app)
app.secret_key = 'key12'

@app.route('/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'email_id' in request.form and 'password' in request.form and 'Login-type' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email_id = request.form['email_id']
        type_of_user = request.form['Login-type']
        print("a")
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login_credentials WHERE username = %s AND password=%s', [username, password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            print("b")
    
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            print("c")
        elif not username or not password:
            msg = 'Please fill out the form!'
            print("d")
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO login_credentials VALUES(%s,%s,%s,%s)', [username,email_id, password,type_of_user])
            mysql.connection.commit()
            msg = 'Successfully registered! Please Sign-In'
            print("e")
            return render_template('login.html', msg=msg)
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("gg")
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login_credentials WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account['type_of_user'] == "Patient":
            return redirect(url_for('patient_home'))
        else:
             return redirect(url_for('hospital_home'))      
    return render_template('login.html')

@app.route('/hospital_home', methods = ['GET', 'POST'])
def hospital_home():
    return render_template('hospital_home.html')

@app.route('/patient_home', methods = ['GET', 'POST'])
def patient_home():
    return render_template('patient_home.html')

@app.route('/self_care', methods = ['GET', 'POST'])
def self_care():
    

    return render_template('self_care.html')

@app.route('/selfcare_results', methods = ['GET', 'POST'])
def selfcare_results():
    if request.method == 'POST':
        symptom = request.form['symptom']
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        glink1 = "home+remedies+for"
        glink2 = symptom
        query = glink1+glink2
        glinks=[]
        for page in range(1):
            url = "http://www.google.com/search?q=" + str(query) + "&start=" 
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # soup = BeautifulSoup(r.text, 'html.parser')

            search = soup.find_all('div', class_="yuRUbf")
            for h in search:
                glinks.append(h.a.get('href'))

        glinks = glinks[0:5]     

        base = "https://www.youtube.com/results?search_query="
        input1 = "home+remedies+for"
        input2 = symptom
        final_url = base+input1+input2
        driver.get(final_url)

        user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
        ytlinks = []
        for i in user_data:
                    ytlinks.append(i.get_attribute('href'))  
        ytlinks = ytlinks[0:5]            

    return render_template('selfcare_results.html', glinks=glinks,ytlinks=ytlinks)    

@app.route('/online_consultation', methods = ['GET', 'POST'])
def online_consultation():
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Cursor.execute('SELECT * FROM doctors')
    doctor_list = Cursor.fetchall()
    beds_list = list(doctor_list)
    Doctor_list = []


    for i in range(len(doctor_list)):
        x = doctor_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        Doctor_list.append(list_h)
    return render_template('online_consultation.html',Doctor_list=Doctor_list) 


@app.route('/patient_history', methods = ['GET', 'POST'])
def patient_history():
    if request.method == "POST":
        patientname = request.form['patientname']
        docname = request.form['docname']
        treatment = request.form['treatment']
        date = request.form['date']
        prescription = request.form['filename']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO patient_history VALUES(%s,%s,%s,%s,%s)', [patientname,docname, treatment,date,prescription])
        mysql.connection.commit()


    return render_template('patient_history.html')    

@app.route('/ward_classification', methods = ['GET', 'POST'])
def ward_classification():
    data = ''
    if request.method == 'POST':
        ChronicDisease = request.form['ChronicDisease']
        Respiratory = request.form['Respiratory']
        Gastrointestinal = request.form['Gastrointestinal']
        Nausea = request.form['Nausea']
        Cardiac = request.form['Cardiac']
        HighFever = request.form['HighFever']
        Kidney = request.form['Kidney']
        Diabetes = request.form['Diabetes']
        Neuro = request.form['Neuro']
        Hypertension = request.form['Hypertension']
        Cancer = request.form['Cancer']
        Ortho = request.form['Ortho']
        Blood = request.form['Blood']
        Thyroid = request.form['Thyroid']
        Prostate = request.form['Prostate']
        RespiratoryCD = request.form['RespiratoryCD']
        

        list1 = [ChronicDisease,Respiratory,Gastrointestinal,Nausea,Cardiac,HighFever,
        Kidney,Diabetes,Neuro,Hypertension,Cancer,Ortho,RespiratoryCD,Blood,Prostate,Thyroid]

        result = int(ward_genetic.predict([[list1[0],list1[3],list1[4],list1[6],list1[7],list1[9],list1[11],list1[12],list1[14],list1[15]]]))
        

        if result == 1:
            data = 'ICU'
        elif result == 0:
            data = 'General Ward'    

    return render_template('ward_classification.html', data=data)  

@app.route('/diagnosis', methods = ['GET', 'POST'])
def diagnosis():
    if request.method == "POST":
        symptom = request.form['symptom']
        if symptom == 'diabetes':
            return redirect(url_for('diabetes_diagnosis'))
        elif symptom == 'cancer':
            return redirect(url_for('cancer_diagnosis')) 
        elif symptom == 'fetal_health':
            return redirect(url_for('fetal_health_diagnosis'))   
        elif symptom == 'heart':
            return redirect(url_for('heart_diagnosis'))   
        elif symptom == 'liver':
            return redirect(url_for('liver_diagnosis')) 
        elif symptom == 'pcos':
            return redirect(url_for('pcos_diagnosis'))       

    return render_template('diagnosis.html')  

@app.route('/bed_availability', methods = ['GET', 'POST'])
def bed_availability():
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Cursor.execute('SELECT * FROM beds')
    beds_list = Cursor.fetchall()
    beds_list = list(beds_list)
    Bed_list = []


    for i in range(len(beds_list)):
        x = beds_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        Bed_list.append(list_h)
    return render_template('bed_availability.html',Bed_list=Bed_list)  

@app.route('/bed_availability_hospital', methods = ['GET', 'POST'])
def bed_availability_hospital():
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Cursor.execute('SELECT * FROM beds')
    beds_list = Cursor.fetchall()
    beds_list = list(beds_list)
    Bed_list = []


    for i in range(len(beds_list)):
        x = beds_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        Bed_list.append(list_h)

    if request.method == 'POST':
        wardtype = request.form['wardtype']
        bed = request.form['bed']
        print(wardtype,bed)
        Cursor.execute('UPDATE beds SET vacant_beds = %s  WHERE type_of_ward = %s', [bed, wardtype])
        mysql.connection.commit()
    return render_template('bed_availability_hospital.html', Bed_list=Bed_list)      

@app.route('/image_recognition', methods = ['GET', 'POST'])
def image_recognition():
    result = ''
    if request.method == "POST":
        symptom = request.form['symptom']
        uploaded_file = request.files['image']
        path = 'F:/Codes/Hospital Management/pred/'
        image1 = load_img('image.png', target_size=(224, 224))
        image1 = img_to_array(image1)
        # reshape data for the model
        image1 = image1.reshape((1, image1.shape[0], image1.shape[1], image1.shape[2]))

        # prepare the image for the VGG model
        image1 = preprocess_input(image1)
        if symptom == "Alzheimer":
            yhat = alzheimer.predict(image1, verbose=0)[0]
            if yhat[0] == yhat.max():
              result = "Mild demented"
            elif yhat[1] == yhat.max():
                result = "Moderate demented"
            elif yhat[2] == yhat.max():
                result = "Non demented"
            elif yhat[3] == yhat.max():
                result = "Very mild demented"
            print(result)

        elif symptom == "Brain Tumor":
            yhat = brain_tumor.predict(image1, verbose=0)[0]
            if yhat[0] == yhat.max():
              result = "No brain tumor"
            elif yhat[1] == yhat.max():
                result = "Brain tumor detected"
            print(result)
           
        elif symptom == "Breast Cancer":
            yhat = breast_cancer.predict(image1, verbose=0)[0]
            if yhat[0] == yhat.max():
              result = "No breast cancer"
            elif yhat[1] == yhat.max():
                result = "Breast cancer detected"
            print(result)
           
        elif symptom == "Chest X-Ray":
            yhat = chest_xray.predict(image1, verbose=0)[0]
            if yhat[0] == yhat.max():
              result = "COVID detected"
            elif yhat[1] == yhat.max():
                result = "Normal condition"
            elif yhat[2] == yhat.max():
                result = "Pneumonia detected"
            print(result)
            
        elif symptom == "Malaria":
            yhat = malaria.predict(image1, verbose=0)[0]
            if yhat[0] == yhat.max():
              result = "Malaria detected"
            elif yhat[1] == yhat.max():
                result = "Malaria not detected"
            print(result)
    return render_template('image_recognition.html', result=result)  


@app.route('/image_rec_result', methods = ['GET', 'POST'])
def image_rec_result():
    
                    
        return render_template('image_rec_result.html')    

            

@app.route('/patient_search', methods = ['GET', 'POST'])
def patient_search():
    if request.method == "POST":
        patientname = request.form['patientname']
        docname = request.form['docname']
        treatment = request.form['treatment']
        date = request.form['date']
        prescription = request.form['filename']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO patient_history_hospital VALUES(%s,%s,%s,%s,%s)', [patientname,docname, treatment,date,prescription])
        mysql.connection.commit()

    return render_template('patient_search.html')                  

@app.route('/patient_list_hospital', methods = ['GET', 'POST'])
def patient_list_hospital():
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Cursor.execute('SELECT * FROM patient_history_hospital')
    patient_list = Cursor.fetchall()
    patient_list = list(patient_list)
    Patient_list = []


    for i in range(len(patient_list)):
        x = patient_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        Patient_list.append(list_h)
    return render_template('patient_list_hospital.html',Patient_list=Patient_list)                  



@app.route('/patient_list', methods = ['GET', 'POST'])
def patient_list():
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Cursor.execute('SELECT * FROM patient_history')
    patient_list = Cursor.fetchall()
    patient_list = list(patient_list)
    Patient_list = []


    for i in range(len(patient_list)):
        x = patient_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        Patient_list.append(list_h)
    return render_template('patient_list.html',Patient_list=Patient_list)                  


@app.route('/diabetes_diagnosis', methods = ['GET', 'POST'])
def diabetes_diagnosis():
    data = ''
    if request.method == "POST":
        glucose = request.form['glucose']
        bloodpressure = request.form['bloodpressure']
        skinthickness = request.form['skinthickness']
        insulin = request.form['insulin']
        bmi = request.form['bmi']
        diabetespedigreefunction = request.form['diabetespedigreefunction']
        age = request.form['age']
        
        result = int(ml_diabetes.predict([[glucose,bloodpressure,skinthickness,insulin,bmi,diabetespedigreefunction,age]]))
        if result == 1:
            data = 'Diabetes Detected'
        elif result == 0 :
            data = 'Diabetes NOT Detected'

    return render_template('diabetes.html', data = data)  

@app.route('/cancer_diagnosis', methods = ['GET', 'POST'])
def cancer_diagnosis():
    data = ''
    if request.method == 'POST':
        Radiusmean = request.form['Radiusmean']
        Texturemean = request.form['Texturemean']
        Perimetermean = request.form['Perimetermean']
        Areamean = request.form['Areamean']
        Smoothnessmean = request.form['Smoothnessmean']
        Compactnessmean = request.form['Compactnessmean']
        Concavitymean = request.form['Concavitymean']
        Concave = request.form['Concave']
        Symmetrymean = request.form['Symmetrymean']
        Fractaldimensionmean = request.form['Fractaldimensionmean']
        Radiusse = request.form['Radiusse']
        Texturese = request.form['Texturese']
        Perimeterse = request.form['Perimeterse']
        Arease = request.form['Arease']
        Smoothnessse = request.form['Smoothnessse']
        Compactnessse = request.form['Compactnessse']
        Concavityse = request.form['Concavityse']
        Concavese = request.form['Concavese']
        Symmetryse = request.form['Symmetryse']
        Fractaldimensionse = request.form['Fractaldimensionse']
        Radiusworst = request.form['Radiusworst']
        Textureworst = request.form['Textureworst']
        Perimeterworst = request.form['Perimeterworst']
        Areaworst = request.form['Areaworst']
        Smoothnessworst = request.form['Smoothnessworst']
        Compactnessworst = request.form['Compactnessworst']
        Concavityworst = request.form['Concavityworst']
        Concaveworst = request.form['Concaveworst']
        Symmetryworst = request.form['Symmetryworst']
        Fractaldimensionworst = request.form['Fractaldimensionworst']
        
        result = int(ml_cancer.predict([[Radiusmean,Texturemean,Perimetermean,Areamean,Smoothnessmean,Compactnessmean,Concavitymean,
        Concave,Symmetrymean,Fractaldimensionmean,Radiusse,Texturese,Perimeterse,Arease,Smoothnessse,Compactnessse,Concavityse,
        Concavese,Symmetryse,Fractaldimensionse,Radiusworst,Textureworst,Perimeterworst,Areaworst,Smoothnessworst,Compactnessworst,
        Concavityworst,Concaveworst,Symmetryworst,Fractaldimensionworst]]))

        if result == 1:
            data = 'Breast Cancer Detected'
        elif result == 0:
            data = 'Breast Cancer NOT Detected'    

    return render_template('breast_cancer.html', data=data) 

@app.route('/liver_diagnosis', methods = ['GET', 'POST'])
def liver_diagnosis():
    data = ''
    if request.method == "POST":
        age = request.form['age']
        gender = request.form['gender']
        Total_Bilirubi = request.form['Total_Bilirubi']
        Direct_Bilirubin = request.form['Direct_Bilirubin']
        agAlkaline_Phosphotasee = request.form['Alkaline_Phosphotase']
        Alamine_Aminotransferase = request.form['Alamine_Aminotransferase']
        Aspartate_Aminotransferase = request.form['Aspartate_Aminotransferase']
        Total_Protiens = request.form['Total_Protiens']
        Albumin = request.form['Albumin']
        Albumin_and_Globulin_Ratio = request.form['Albumin_and_Globulin_Ratio']
        
        result = int(ml_liver.predict([[age,gender,Total_Bilirubi,Direct_Bilirubin,agAlkaline_Phosphotasee,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,Albumin_and_Globulin_Ratio]]))
        if result == 1:
            data = 'Cirrhosis Detected'
        elif result == 0 :
            data = 'Cirrhosis NOT Detected'



    return render_template('liver.html', data=data) 

@app.route('/heart_diagnosis', methods = ['GET', 'POST'])
def heart_diagnosis():
    data = ''
    if request.method == "POST":
        cp = request.form['cp']
        trestbps = request.form['trestbps']
        chol = request.form['chol']
        fbs = request.form['fbs']
        restecg = request.form['restecg']
        thalach = request.form['thalach']
        exang = request.form['exang']
        oldpeak = request.form['oldpeak']
        slope = request.form['slope']
        ca = request.form['ca']
        thal = request.form['thal']

        result = int(ml_heart.predict([[cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]]))
        if result == 1:
            data = 'Heart disease detected'
        elif result == 0:
            data = 'Heart disease detected'

        
    return render_template('heart.html', data=data) 

@app.route('/pcos_diagnosis', methods = ['GET', 'POST'])
def pcos_diagnosis():
    data = ''
    if request.method == 'POST':
        age = request.form['age']
        BMI = request.form['BMI']
        Blood_Group_Pulse = request.form['Blood_Group_Pulse']
        rate = request.form['rate']
        RR = request.form['RR']
        Hb = request.form['Hb']
        Cycle = request.form['Cycle']
        Cyclelength = request.form['Cyclelength']
        Pregnant = request.form['Pregnant']
        Noofaborptions = request.form['Noofaborptions']
        IbetaHCG = request.form['IbetaHCG']
        IIbetaHCG = request.form['IIbetaHCG']
        FSH = request.form['FSH']
        LH = request.form['LH']
        FSHLH = request.form['FSHLH']
        WaistHipRatio = request.form['WaistHipRatio']
        TSH = request.form['TSH']
        AMH = request.form['AMH']
        PRL = request.form['PRL']
        VitD3 = request.form['VitD3']
        PRG = request.form['PRG']
        RBS = request.form['RBS']
        Weightgain = request.form['Weightgain']
        hairgrowth = request.form['hairgrowth']
        Skindarkening = request.form['Skindarkening']
        Hairloss = request.form['Hairloss']
        Pimples = request.form['Pimples']
        RegExercise = request.form['RegExercise']
        BP_Systolic = request.form['BP_Systolic']
        BP_Diastolic = request.form['BP_Diastolic']
        FollicleNoL = request.form['FollicleNoL']
        FolliclenoR = request.form['FolliclenoR']
        AvgFsizeL = request.form['AvgFsizeL']
        AvgFsizeR = request.form['AvgFsizeR']
        Endometrium = request.form['Endometrium']

        result = int(ml_pcos.predict([[age,BMI,Blood_Group_Pulse,rate,RR,Hb,Cycle,Cyclelength,Pregnant,Noofaborptions,IbetaHCG,IIbetaHCG,
        FSH,LH,FSHLH,WaistHipRatio,TSH,AMH,PRL,VitD3,PRG,RBS,Weightgain,hairgrowth,Skindarkening,Hairloss,Pimples,RegExercise,BP_Systolic
        ,BP_Diastolic,FollicleNoL,FolliclenoR,AvgFsizeL,AvgFsizeR,Endometrium]]))

        if result == 1:
            data = 'PCOS Detected'
        elif result == 0:
            data = 'PCOS NOT Detected'    


    return render_template('pcos.html', data=data)     

@app.route('/fetal_health_diagnosis', methods = ['GET', 'POST'])
def fetal_health_diagnosis():
    data = ''
    if request.method == 'POST':
        baseline_value = request.form['baseline_value']
        accelerations = request.form['accelerations']
        fetal_movement = request.form['fetal_movement']
        uterine_contractions = request.form['uterine_contractions']
        light_decelerations = request.form['light_decelerations']
        severe_decelerations = request.form['severe_decelerations']
        prolongued_decelerations = request.form['prolongued_decelerations']
        abnormal_short_term_variability = request.form['abnormal_short_term_variability']
        mean_value_of_short_term_variability = request.form['mean_value_of_short_term_variability']
        percentage_of_time_with_abnormal_long_term_variability = request.form['percentage_of_time_with_abnormal_long_term_variability']
        mean_value_of_long_term_variability = request.form['mean_value_of_long_term_variability']
        histogram_width = request.form['histogram_width']
        histogram_min = request.form['histogram_min']
        histogram_max = request.form['histogram_max']
        histogram_number_of_peaks = request.form['histogram_number_of_peaks']
        histogram_number_of_zeroes = request.form['histogram_number_of_zeroes']
        histogram_mode = request.form['histogram_mode']
        histogram_mean = request.form['histogram_mean']
        histogram_median = request.form['histogram_median']
        histogram_variance = request.form['histogram_variance']
        histogram_tendency = request.form['histogram_tendency']

        result = int(ml_fetal_health.predict([[baseline_value,accelerations,fetal_movement,uterine_contractions,light_decelerations,
        severe_decelerations,prolongued_decelerations,abnormal_short_term_variability,mean_value_of_short_term_variability,
        percentage_of_time_with_abnormal_long_term_variability,mean_value_of_long_term_variability,histogram_width,histogram_min,
        histogram_max,histogram_number_of_peaks,histogram_number_of_zeroes,histogram_mode,histogram_mean,histogram_median,
        histogram_variance,histogram_tendency]]))

        if result == 1:
            data = 'Normal Condition'
        elif result == 2:
            data = 'Suspect Detected'
        elif result == 3:
            data = 'Pathological Condition Detected'        
    return render_template('fetal_health.html', data=data)             



if __name__=="__main__":
    app.run(debug=True)    

