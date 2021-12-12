# Evathon-2021

Link for Datasets and Static folder :
https://drive.google.com/drive/folders/1dJRLoP9Z4Am1MqTraQX0Xi1gokLtAyTS?usp=sharing

Steps to Run the code:

1. Create a project folder in VScode.

2. Open the folder and create virtual environment by running the command "python -m venv env" in the terminal.

3. Move app.py file, templates folder and static folder in the virtual environment created.

4. Run app.py


#Problem Statement: 
1. Classifying into ICU and general wards according to the patient's disorder.
2. Diagnosing several diseases, either by values from their medical reports or by the pictorial reports of the tests done(for e.g. X-Ray)


#Features

#Doctor Interface:

1. Classification of Ward: With this feature the doctor will be able to decide if the patient should go to “Mild Ward” or “ICU”. To predict this, we will be using powerful Machine Learning algorithms.

2. Diagnosis: On the basis of the input of the symptoms and other required data, an evolutionary model using genetic algorithm and  Machine Learning model will predict if the patient has the particular disease. 
Application includes diagnosis of: Breast Cancer, Cirrhosis, Diabetes, Fetal-Health, Heart, PCOS.

3. Image Recognition: In case if there is a situation where we need to draw conclusion about some test/condition of a patient from images, image can be uploaded and our Deep Learning Model will give proper result and conclusion about the same.
Application provides: Alzheimer, Pneumonia, Breast Cancer, Malaria, Brain Tumor.

4. Bed Availability: Another important feature demanded by many hospitals is to know the real time bed count. We plan to provide the exact details of distribution of beds in real time.

5. Patient History: In case for reference, doctor can also have the option to go through patient’s previous medical history for better knowledge of patient.

Patient Interface:

1. Interim Self-Care: In case if the patient is feeling uneasy and is unable to reach the doctor at the moment, the app will provide him suggestions of home remedies , basic do’s and don’ts until he seeks doctor.

2. Nearest Clinic/Hospital: The patient will be able to see the nearest clinics and hospitals to his location.

3. Patient History: For his own reference, the patient can also keep a track of his own medical history and present it to the required authorities whenever required.

4. Can see real time vacant bed availability of a particular hospital.


#Tech-Stack used :

1. Front-End - HTML/CSS/JavaScript
2. Back-End - Flask - Python
3. Database - MySQL
4. Machine Learning Models for diagnosis - 
    a. Naive Bayes
    b. Random Forest Classifier
    c. Logistic Regression
5. Deep Learning Model for Image Recognition : VGG16
6. Evolutionary Computation Method : Genetic Algorithm
7. Automation of Web Scraping -
    a. Beautiful Soup
    b. Selenium Bot



