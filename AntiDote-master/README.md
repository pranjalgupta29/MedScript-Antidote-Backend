# Software Engineering


Antidote is a ‘Disease Prediction and Patient Management System’ software. People are reluctant to visit the hospitals due to the fear of contracting COVID-19 while hospitals too have closed-out patient wards for treatment. Apart from this, health officials and the government have continuously been advising the general public to avoid visiting the hospitals except for emergencies, resulting in these fears being compounded.<br>
This portal provides an e-consultation facility to the patients. The patients can sign up at the portal. After logging in the patients would observe there are various sections that cater to their needs. A section for predicting the disease that they are likely to suffer from where they can fill a form by providing their details along with the symptoms witnessed. Based on the result of the prediction, the patients can search for the specialised doctors and share the prediction results with the selected doctor. The patients would also be provided with the section where they can upload their previous medical reports, thereby keeping a track of their medical history which often gets misplaced due to the conventional way of storing the reports in files.<br>
The doctors across the country can register themselves on our portal specifying the fields that they have been working in. Once logged in then each doctor will receive notifications regarding the patients who have approached them along with their details including their symptoms. After analysing the reports of the patient, the doctor can provide a confirmation of the appointment and if required they can even provide the patient with the prescription that needs to be followed till the appointment date. This will help overcome the challenge of increased drop rate in the regular patient visits and also help patients to consult the doctors in case of emergency situations by fixing an appointment without the need to visit the hospital regarding the same. 
<br>
# Product Features:<br>
Registration/Login<br>
Disease prediction and Doctor suggestion <br>
Uploading medical reports<br>
Appointment Confirmation<br>
Prescription<br>
Edit profile<br>
Question and Answer(QnA)<br>

# Usage:
Clone this repo
The inside the Hospital folder create an imp.py file having a class named secrets with the variables:
<li> SECRET_KEY 
<li> EMAIL_HOST_USER 
<li> EMAIL_HOST_PASSWORD 
 
 Structure of file should be
```python
 class secrets: 
    SECRET_KEY = 'your production key'
    EMAIL_HOST_USER = 'your email'
    EMAIL_HOST_PASSWORD = 'your password'
```
