import numpy as np
import pandas as pd
import pickle

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import *
# ... (The rest of your existing imports)

# Load dataset
sym_des = pd.read_csv("datasets/symtoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv('datasets/medications.csv')
diets = pd.read_csv("datasets/diets.csv")

# Load model
svc = pickle.load(open('models/svc.pkl', 'rb'))

# Helper function
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']

    return desc, pre, med, die, wrkout

symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

# Model Prediction function
def get_predicted_value(patient_symptoms, svc_model, symptoms_dict, diseases_list):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        # Check if the key exists in the dictionary before accessing it
        if item in symptoms_dict:
            input_vector[symptoms_dict[item]] = 1
        else:
            # Handle the case where the key does not exist (you can log a warning or take appropriate action)
            print(f"Warning: Key '{item}' not found in symptoms_dict")
    # Make sure to handle the case where all elements of input_vector are zero
    if np.sum(input_vector) == 0:
        # Handle the case where no symptoms were found
        print("Warning: No valid symptoms found")
    return diseases_list[svc_model.predict([input_vector])[0]]

def index(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def predict_medicine(request):
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        print(symptoms)
        if symptoms == "Symptoms":
            message = "Please either write symptoms or you have written misspelled symptoms"
            return render(request, 'predict_medicine.html', {'message': message})
        else:
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
            predicted_disease = get_predicted_value(user_symptoms, svc, symptoms_dict, diseases_list)
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

            my_precautions = [i for i in precautions[0]]

            # Filter doctors based on a match with either predicted_disease or treat_cond
            doctor_list = Doctor.objects.filter(
                Q(specialization__iexact=symptoms) |
                Q(treat_cond__icontains=predicted_disease)
            )
            register = Registration.objects.get(user=request.user)
            Prediction.objects.create(
                register=register,
                symptoms=symptoms,
                predicted_disease=predicted_disease,
                dis_des=dis_des,
                my_precautions=my_precautions,
                medications=medications,
                my_diet=rec_diet,
                workout=workout,
            )
            
            messages.success(request, "Prediction and Result saved successfully")
            return render(request, 'predict_medicine.html', {
                'predicted_disease': predicted_disease,
                'dis_des': dis_des,
                'my_precautions': my_precautions,
                'medications': medications,
                'my_diet': rec_diet,
                'workout': workout,
                'doctor_list':doctor_list,
            })

    return render(request, 'predict_medicine.html')

def admin_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('/')
            else:
                messages.success(request, "Invalid User")
                return redirect('admin_login')
        except:
            messages.success(request, "Invalid User")
            return redirect('admin_login')
    return render(request, 'admin_login.html')

def logout_admin(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('/')

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['password']
        user = authenticate(username=email, password=pwd)
        if user:
            if user.is_staff:
                messages.success(request, "Invalid User")
                return redirect('user_login')
            else:
                login(request, user)
                messages.success(request, "User Login Successful")
                return redirect('/')
        else:
            messages.success(request, "Invalid User")
            return redirect('user_login')
    return render(request, "user_login.html")

def user_register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        mobile = request.POST['mobile']

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email.')
            return redirect('user_register')

        # Create user and registration
        user = User.objects.create_user(first_name=first_name, username=email, password=password)
        Registration.objects.create(user=user, mobile=mobile)

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('user_login')
    return render(request, "user_register.html")

@login_required(login_url='/admin_login/')
def password_change(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        c = request.POST['pwd1']
        n = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('admin_login')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('admin_change_password')
    return render(request, 'admin_change.html')

@login_required(login_url='/admin_login/')
def reg_user(request):
    data = Registration.objects.all()
    d = {'data': data}
    return render(request, "reg_user.html", d)

@login_required(login_url='/admin_login/')
def feed_view(request):
    data = Feedback.objects.all()
    d = {'data': data}
    return render(request, "feed_view.html", d)

@login_required(login_url='/admin_login/')
def delete_feed(request, pid):
    data = Feedback.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('feed_view')

@login_required(login_url='/admin_login/')
def delete_reg(request, pid):
    data = User.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('reg_user')

@login_required(login_url='/user_login/')
def feed(request):
    if request.method == "POST":
        description = request.POST['description']

        reg = Registration.objects.get(user=request.user)
        Feedback.objects.create(description=description, register=reg)
        messages.success(request, "Feedback Send Successful")
        return redirect('feed')
    return render(request, "add_feed.html")

def profile(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        mobile = request.POST['mobile']

        user = User.objects.filter(id=request.user.id).update(first_name=firstname,)
        Registration.objects.filter(user=request.user).update(mobile=mobile)
        messages.success(request, "Updation Successful")
        return redirect('profile')
    data = Registration.objects.get(user=request.user)
    return render(request, "profile.html", locals())

@login_required(login_url='/user_login/')
def predict_history(request):
    register = Registration.objects.get(user=request.user)
    data = Prediction.objects.filter(register=register)
    d = {'data': data}
    return render(request, 'predict_history.html', d)

@login_required(login_url='/admin_login/')
def pre_history(request):
    data = Prediction.objects.all()
    d = {'data': data}
    return render(request, 'pre_history.html', d)

def detail_predict(request, pid):
    data = Prediction.objects.get(id=pid)

    if request.method == "POST":
        doc_id = request.POST.get('doc_name')  # Assuming 'doc_name' is the id of the selected doctor

        if doc_id:  # Make sure a valid doctor id is provided
            doctor = Doctor.objects.get(id=doc_id)
            data.doctor = doctor
            data.save()
            messages.success(request, "Update Doctor Successful")
        else:
            messages.error(request, "Invalid Doctor ID")

    # Get the predicted_disease from the data
    predicted_disease = data.predicted_disease

    # Filter doctors based on a match with either predicted_disease or treat_cond
    doctor_list = Doctor.objects.filter(
        Q(specialization__iexact=predicted_disease) |
        Q(treat_cond__icontains=predicted_disease)
    )

    # Extracting lists from comma-separated strings
    data.my_precautions_list = [precaution.strip("' ") for precaution in data.my_precautions.strip("[]").split(",")]
    data.medications = [medication.strip("' ") for medication in data.medications.strip("[]").split(",")]
    data.my_diet = [diet.strip("' ") for diet in data.my_diet.strip("[]").split(",")]

    context = {'data': data, 'doctor_list': doctor_list}
    if request.user.is_staff:
        return render(request, "detail_predict_admin.html", context)
    else:
        return render(request, "detail_predict_user.html", context)

@login_required(login_url='/admin_login/')
def user_predict_view(request, pid):
    register = Registration.objects.get(id=pid)
    data = Prediction.objects.filter(register__id=pid)
    d = {'data': data, "register":register}
    return render(request, "user_predict_view.html", d)

@login_required(login_url='/admin_login/')
def delete_pridict(request, pid):
    data = Prediction.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('reg_user')

@login_required(login_url='/admin_login/')
def delete_pridict_ma(request, pid):
    data = Prediction.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('pre_history')

@login_required(login_url='/user_login/')
def user_delete_pridict(request, pid):
    data = Prediction.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('predict_history')

@login_required(login_url='/user_login/')
def add_doctor(request):
    if request.method == "POST":
        doc_name = request.POST['doc_name']
        doc_email = request.POST['doc_email']
        doc_contact = request.POST['doc_contact']
        specialization = request.POST['specialization']
        hospital_name = request.POST['hospital_name']
        hospital_address = request.POST['hospital_address']
        city = request.POST['city']
        qualified = request.POST['qualified']
        experience = request.POST['experience']
        apt_fees = request.POST['apt_fees']
        abl_day = request.POST['abl_day']
        abl_time = request.POST['abl_time']
        treat_cond = request.POST['treat_cond']

        Doctor.objects.create(doc_name=doc_name, doc_email=doc_email, doc_contact=doc_contact,
                                specialization=specialization, hospital_name=hospital_name,
                                hospital_address=hospital_address, city=city, qualified=qualified,
                                experience=experience, apt_fees=apt_fees, abl_day=abl_day, abl_time=abl_time,
                                treat_cond=treat_cond)
        messages.success(request, "Doctor Added Successful")
        return redirect('manage_doctor')
    return render(request, "add_doctor.html")

@login_required(login_url='/user_login/')
def edit_doctor(request, pid):
    if request.method == "POST":
        doc_name = request.POST['doc_name']
        doc_email = request.POST['doc_email']
        doc_contact = request.POST['doc_contact']
        specialization = request.POST['specialization']
        hospital_name = request.POST['hospital_name']
        hospital_address = request.POST['hospital_address']
        city = request.POST['city']
        qualified = request.POST['qualified']
        experience = request.POST['experience']
        apt_fees = request.POST['apt_fees']
        abl_day = request.POST['abl_day']
        abl_time = request.POST['abl_time']
        treat_cond = request.POST['treat_cond']

        Doctor.objects.filter(id=pid).update(doc_name=doc_name, doc_email=doc_email, doc_contact=doc_contact,
                                specialization=specialization, hospital_name=hospital_name,
                                hospital_address=hospital_address, city=city, qualified=qualified,
                                experience=experience, apt_fees=apt_fees, abl_day=abl_day, abl_time=abl_time,
                                treat_cond=treat_cond)
        messages.success(request, "Doctor Update Successful")
        return redirect('manage_doctor')
    data = Doctor.objects.get(id=pid)
    d = {'data': data}
    return render(request, "edit_doctor.html", d)

@login_required(login_url='/admin_login/')
def manage_doctor(request):
    data = Doctor.objects.all()
    d = {'data': data}
    return render(request, 'manage_doctor.html', d)

@login_required(login_url='/admin_login/')
def delete_doctor(request, pid):
    data = Doctor.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('manage_doctor')

def doctor_detail(request, pid):
    data = Doctor.objects.get(id=pid)
    return render(request, 'doctor-details.html', locals())

