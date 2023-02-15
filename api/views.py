from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *
import cv2
import base64
from django.views.decorators.csrf import csrf_exempt
import mysql.connector as sql


#Define global variables
isClicked = False
isLogined = False
usr_name = ""

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        pass_wd = request.POST.get("passwd")
        
        #Save user info to database
        m = sql.connect(host="localhost", user="vu", passwd="maixuanvu", database="image_processing")
        cursor = m.cursor()
        cursor.execute("SELECT  * from users")
        rows = cursor.fetchall()
        m.commit()
        user_names = [name[0] for name in rows]

        if user_name in user_names:
            return render(request, 'signup.html', {'status': 'Available user name! Please choose other name!'})

        if (user_name != "" and pass_wd != ""):
            response = save_user(user_name, pass_wd)
            if response == "success":        
                return redirect('/login/') 
    return render(request, 'signup.html')
 

def save_user(user_name, pass_wd):
    try:
        m = sql.connect(host="localhost", user="vu", passwd="maixuanvu", database="image_processing")
        cursor = m.cursor()
        c = "insert into users Values('{}', '{}')" .format(user_name, pass_wd)
        cursor.execute(c)
        m.commit()
        return "success"
    except:
        return "fail"
        

def log_in(request):
    m = sql.connect(host="localhost", user="vu", passwd="maixuanvu", database="image_processing")
    cursor = m.cursor()
    cursor.execute("SELECT  * from users")
    rows = cursor.fetchall()
    m.commit()
    user_names = [name[0] for name in rows]
    passwd_s = [passw[1] for passw in rows]

    if request.method == "POST":
        user_name = request.POST.get('user_name')
        pass_wd = request.POST.get("passwd")

        global usr_name
        usr_name = user_name

        if user_name in user_names and pass_wd in passwd_s and user_names.index(user_name) == passwd_s.index(pass_wd):
            global isLogined
            isLogined = True
            return redirect('/upload/') 
        else:
            return render(request, 'login.html', {'status': 'Incorrect user name or password!'})

    return render(request, 'login.html')


def log_out(request):
    return render(request, 'login.html')

def upload_image(request):
    if isLogined == False:
         return redirect('/login/') 
    if request.method == 'POST':
        form = ImageForm(data = request.POST, files=request.FILES)
        if form.is_valid():
            form.save()       
            return redirect('/process_image/')
    else:
        form = ImageForm()
    return render(request, 'upload.html', {"form": form})


def image_processing(request):
    if isLogined == False:
        return redirect('/login/') 

    image = Image.objects.last()
    with open('my_image.jpeg', 'wb') as f:
        f.write(image.image.read())

    return render(request, 'process.html', {"image": image})

@csrf_exempt
def perform_process(request):  
    global isClicked
    isClicked = True

    img = cv2.imread('my_image.jpeg')
    _, encoded_image = cv2.imencode(".jpg", img)
    if request.method == "POST":
        try:
            mask_size = int(request.POST.get("mask_size"))
            if mask_size % 2 == 0:
                mask_size_tmp = mask_size - 1
            else:
                mask_size_tmp = mask_size

            #Do image blurring
            blur = cv2.GaussianBlur(img, sigmaX=5, sigmaY=5, ksize=(mask_size_tmp, mask_size_tmp))

            slider_value = request.POST.get("slider_value")    
            slider_value = float(slider_value)  

            #Save image params to model
            image_param_model = ImageProcessing(mask_size = mask_size, brightness = slider_value)
            image_param_model.save()

            #Do brightness change
            alpha = slider_value/255
            img = blur*alpha
            cv2.imwrite("a.jpg", img)

            # Encode the processed image as a JPEG
            _, encoded_image = cv2.imencode(".jpg", img)
        except:
            return JsonResponse({"status": "fail"})
    
    # Return the encoded image as a response
    return JsonResponse({"image": base64.b64encode(encoded_image.tobytes()).decode('utf-8'), "status": "succes"})


def save_infor(request):
    image_params_model = ImageProcessing.objects.last()
    masksize = image_params_model.mask_size
    brightness = image_params_model.brightness

    try:
        m = sql.connect(host="localhost", user="vu", passwd="maixuanvu", database="image_processing")
        cursor = m.cursor()
        c = "insert into IP_params Values('{}', '{}', '{}')" .format(masksize, brightness, usr_name)
        cursor.execute(c)
        m.commit()
        return JsonResponse({"status": "success"})
    except:
        return JsonResponse({"status": "fail"})


def history(request):
    return render(request, 'history.html')