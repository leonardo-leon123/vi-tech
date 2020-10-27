from flask import Flask, render_template, request, json, redirect, url_for,make_response,Blueprint
from flaskext.mysql import MySQL
from flask_login import login_user,logout_user,login_required
import os
import Modelo as Modelo
import pdfkit
import platform

app = Blueprint('app',__name__)

#config = pdfkit.configuration(wkhtmltopdf="./bin/wkhtmltopdf") 
#Config para heroku

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
    return render_template('inicio.html')


@app.route('/bodas',methods=["POST","GET"])
def bodas():
    if request.method == "POST":
        name = request.form["nm1"]
        name2 = request.form["nm2"]
        location = request.form["lc"]        
        return redirect(url_for("app.pdf_template", name=name , name2=name2 , location=location))
    else:
        return render_template('bodas.html')

        
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
    #pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku    
    pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=bodas.pdf'    
    return response

@app.route('/<name>/<name2>/<date>/<hour>')
@login_required #XV TEMPLATE
def pdf_template_xv(name,name2,date,hour):
    rendered = render_template('pdf_template-xv.html',name=name,name2=name2,date=date,hour=hour)
    #pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku
    pdf = pdfkit.from_string(rendered,False)    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=xv.pdf'    
    return response
@app.route('/<name>/<name2>/<date>/<location>/<school>')
@login_required #GRAD TEMPLATE
def pdf_template_grad(name,name2,date,location,school):
    rendered = render_template('pdf_template-grad.html',name=name,name2=name2,date=date,location=location,school=school)
    #pdf = pdfkit.from_string(rendered,False,configuration = config)
    #Config para heroku
    pdf = pdfkit.from_string(rendered,False)  
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=graduacion.pdf'    
    return response

@app.route('/<name>/<name2>/<date>/<location>/<company>/<price>')
@login_required #FIESTA OFICINA TEMPLATE
def pdf_template_fiesta(name,name2,date,location,company,price):
    rendered = render_template('pdf_template-fiesta.html',name=name,name2=name2,date=date,location=location,company=company,price=price)
    #pdf = pdfkit.from_string(rendered,False,configuration = config)    
    #Config para heroku
    pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=fiesta_godin.pdf'    
    return response



