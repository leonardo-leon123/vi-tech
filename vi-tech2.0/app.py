#Import Azure Libraries
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
#from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

#Import flask Libraries
from flask import Flask, render_template, request, json, redirect, url_for,make_response,Blueprint
from flaskext.mysql import MySQL
from flask_login import login_user,logout_user,login_required
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet
#Import Python / proyect libraries
import os
import Modelo as Modelo
import pdfkit
import platform
import requests
import time
from array import array
from PIL import Image
import sys
import time
from io import BytesIO

app = Blueprint('app',__name__)


subscription_key = "69432c0e60ea4cba9d3875f7edfefe44"
endpoint = "https://vi-tech-computer-vision.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

#Libreria para vision pip install azure-cognitiveservices-vision-computervision==0.5.0

config = pdfkit.configuration(wkhtmltopdf="./bin/wkhtmltopdf") 
#Config para heroku



class MyForm(FlaskForm):
    image = FileField('image')

images = UploadSet('images',IMAGES)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html',error=error)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicio')
@login_required
def inicio():
    return render_template('inicio-copy.html')

@app.route('/set_cookie')
@login_required
def set_cookie():

    cookie_contratos = '0'

    response = make_response(redirect(url_for('app.inicio')))

    response.set_cookie('documentos_generados',cookie_contratos)

    return response

@app.route('/delete_cookie')
def delete_cookie():

    response = make_response(redirect(url_for('app.index')))

    response.set_cookie('documentos_generados', '', expires=0)

    return response


@app.route('/cliente')
def clientes():
    return render_template('cliente.html')


@app.route('/badges')
@login_required
def badges():
    return render_template('badges.html')

@app.route('/template-select')
@login_required
def template_select():
    return render_template('template-select.html')

@app.route('/bodas',methods=["POST","GET"])
def bodas():
    badges = 0
    name = None
    name2 = None
    location = None
    if request.method == "POST":        
        name = request.form["nm1"]
        name2 = request.form["nm2"]
        location = request.form["lc"]
        return redirect(url_for("app.pdf_template", name=name , name2=name2 , location=location))

         
    else:
        return render_template('bodas.html',name=name , name2=name2 , location=location)



@app.route('/bodas-upload', methods=['GET','POST'])
def bodas_upload():    
    form = MyForm()
    name = "None"
    name2 = "None"
    location = "None"

    if form.validate_on_submit():
        print(form.image.data)
        filename = images.save(form.image.data)
        print(f'./uploads/images/{filename}')
        image = open(f'./uploads/images/{filename}','rb')
        #image = 'https://i.ibb.co/0rW9ZBv/20201122-182930.jpg'
        #recognize_handw_results = computervision_client.read(_url,language="es", raw=True)    
        recognize_handw_results = computervision_client.batch_read_file_in_stream(image,language="es",raw = True)
        image.close()
        operation_location_remote = recognize_handw_results.headers["Operation-Location"]
        operation_id = operation_location_remote.split("/")[-1]
        while True:            
            get_handw_text_results = computervision_client.get_read_operation_result(operation_id)
            if get_handw_text_results.status not in ['NotStarted', 'Running']:
                break
            time.sleep(1)
        if get_handw_text_results.status == TextOperationStatusCodes.succeeded:
            print("Success")
            for text_result in get_handw_text_results.recognition_results:
                l=[]
                for line in text_result.lines:
                    x = line.text
                    l.append(x)          
        name=l[0]
        name2=l[1]
        location=l[2]
        print(name)
        print(name2)
        print(location) 

        return redirect(url_for("app.pdf_template", name=name , name2=name2 , location=location))

    return render_template ('bodas-upload.html', form = form)

        
@app.route('/xv',methods=["POST","GET"])
@login_required
def xv():
    if request.method == "POST":
        name = request.form["nm"]
        name2 = request.form["nm2"]
        date = request.form["date"]
        hour = request.form["hour"]          
        return redirect(url_for("app.pdf_template_xv", name=name , name2=name2 , date=date,hour=hour ))
    else:
        return render_template('xv.html')


@app.route('/grad',methods=["POST","GET"])
@login_required
def grad():
    if request.method == "POST":
        name = request.form["nm"]
        name2 = request.form["nm2"]
        date = request.form["date"]
        location = request.form["lc"]   
        school = request.form["sc"]       
        return redirect(url_for("app.pdf_template_grad", name=name , name2=name2 , date=date,location=location,school=school))
    else:
        return render_template('grad.html')
@app.route('/fiesta',methods=["POST","GET"])
@login_required
def fiesta():
    if request.method == "POST":
        name = request.form["nm"]
        name2 = request.form["nm2"]
        date = request.form["date"]
        location = request.form["lc"]   
        company = request.form["comp"] 
        price = request.form["price"]      
        return redirect(url_for("app.pdf_template_fiesta", name=name , name2=name2 , date=date,location=location,company=company,price=price))
    else:
        return render_template('fiesta.html')
        

@app.route('/<name>/<name2>/<location>') #BODAS TEMPLATE
def pdf_template(name,name2,location):
    rendered = render_template('pdf_template-bodas.html',name=name,name2=name2,location=location)
    pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku    
    #pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=bodas.pdf'    
    return response

@app.route('/<name>/<name2>/<date>/<hour>')
@login_required #XV TEMPLATE
def pdf_template_xv(name,name2,date,hour):
    rendered = render_template('pdf_template-xv.html',name=name,name2=name2,date=date,hour=hour)
    pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku
    #pdf = pdfkit.from_string(rendered,False)    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=xv.pdf'    
    return response
@app.route('/<name>/<name2>/<date>/<location>/<school>')
@login_required #GRAD TEMPLATE
def pdf_template_grad(name,name2,date,location,school):
    rendered = render_template('pdf_template-grad.html',name=name,name2=name2,date=date,location=location,school=school)
    pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku
    #pdf = pdfkit.from_string(rendered,False)  
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=graduacion.pdf'    
    return response

@app.route('/<name>/<name2>/<date>/<location>/<company>/<price>')
@login_required #FIESTA OFICINA TEMPLATE
def pdf_template_fiesta(name,name2,date,location,company,price):
    rendered = render_template('pdf_template-fiesta.html',name=name,name2=name2,date=date,location=location,company=company,price=price)
    pdf = pdfkit.from_string(rendered,False,configuration = config)    
    #Config para heroku
    #pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=fiesta_godin.pdf'    
    return response


@app.route('/contratos')
@login_required
def contratos():
    try:
        consulta = Modelo.selectALLContratos()
        return render_template("contratos.html", contratos=consulta)
    except:
        print("error")


