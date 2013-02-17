# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import loader, Context
from django.http import HttpResponse
from adminmanager.models import *
from django.template.loader import get_template
import hashlib
import csv
from django.http import HttpResponse

def main(request):
	return render_to_response('index.html')
	
def registration(request):
	return render_to_response('registration.html')
	
def reg_test(request):
	return render_to_response('reg_test.html')
	
def register_response(request):
	you_sex = 0
	if 'first_name' in request.POST: # здесь нужно использовать django.forms
		if request.POST['sex'] == 'man':
			you_sex = 0
		else:
			you_sex = 1
		man = request.POST['first_name']
		t = get_template('register_response.html')
		message = t.render(Context({'first_name': man}))
		#hashpass = hashlib.sha224(request.POST['password']).hexdigest()
		savebase = Users(login=request.POST['login'],first_name=request.POST['first_name'],second_name=request.POST['second_name'],email=request.POST['email'], passwd=request.POST['password'], sex=you_sex,wishes=request.POST['wishes'])
		savebase.save()
	else:
		man = 'username'
		t = get_template('register_response.html')
		message = t.render(Context({'first_name': man}))
	return HttpResponse(message) # не понятно, почему не использовать shortcut?! 
	
def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    #response = HttpResponse(mimetype='text/csv')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ('First row', 'g1pn0z', 'test987', 'http://accounts.google.com'),
        ('Second row', 'rinat09', 'p9875431', 'http://mail.ru'),
    )

    t = loader.get_template('usermodule.html')
    html = t.render(Context({ 'data': csv_data, }))
    return HttpResponse(html)

def csv_view(request):
	csv_data = ''
	with open(request.POST['csv_file']) as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			csv_data = csv_data + ', '.join(row)
	
def addto(request):
	if 'title' in request.POST:
		man = request.POST['title']
		my_login = request.session['login']
		tester = Users.objects.filter(login=my_login).values('id')
		in_id = tester[0]['id']
		p0 = Users.objects.get(pk=in_id)
		t = get_template('usermodule.html')
		message = t.render(Context({'title': man}))
		savebase = CSVBox(title=request.POST['title'],login_base=request.POST['login1'],password=request.POST['pass'],url=request.POST['url'],users=p0)
		savebase.save()
	else:
		man = 'username'
		t = get_template('error.html')
		message = t.render(Context({'title': man}))
	return HttpResponse(message)
	
	
def output_csvbox(request):
	my_login = request.session['login']
	tester = Users.objects.filter(login=my_login).values('id')
	in_id = tester[0]['id']
	p0 = Users.objects.get(pk=in_id)
	now = CSVBox.objects.filter(users=p0)#nastroit vivod
	return render_to_response('usermodule.html', {'view_csvbox': now})	

#testing script
def usercenter(request): # в django принятно именовать представления с использованием нижнего подчёркивания между словами, вот так: user_center 
	try:
		m = Users.objects.get(login=request.POST['login'])
		if m.passwd == request.POST['pass']:
			request.session['member_id'] = m.id
			request.session['login'] = m.login
			#return HttpResponse("You login it - %s" % request.session['member_id'])
			#return render_to_response('usermodule.html')
			man = request.POST['login']
			t = get_template('usermodule.html')
			message = t.render(Context({'my_login': man}))
			return HttpResponse(message)
	except Users.DoesNotExist:
		return HttpResponse("Sorry, repeat please! <a href='http://127.0.0.1:8000/'>(back)</a>")

def delete_row(request):
	if 'del_index' in request.POST:
		now = CSVBox.objects.filter(pk=request.POST['del_index']).delete()
		return render_to_response('usermodule.html')
	if 'editor_index' in request.POST:
		now = CSVBox.objects.filter(pk=request.POST['editor_index'])
		t = get_template('base_editor.html')
		message = t.render(Context({'edit_this_row': now}))
		return HttpResponse(message)
	else:
		return render_to_response('error.html')

def update_row(request):
	if 'editor_index' in request.POST:
		now = CSVBox.objects.filter(pk=request.POST['editor_index']).update(title=request.POST['title'],login_base=request.POST['login_base'],password=request.POST['passwd'],url=request.POST['url'])
		return render_to_response('update.html')
	else:
		return render_to_response('index.html')

import base64, hmac, hashlib

def generate(request):
	if 'secret' in request.POST:
		gen_pas = base64.b64encode(hmac.new(str(request.POST['secret']),str(request.POST['gen_url']), hashlib.sha1).digest())
		new_pas = 'a'
		i = int(request.POST['max_len'])
		new_pas = gen_pas[:i]
		t = get_template('usermodule.html')
		message = t.render(Context({'generated_pas': new_pas }))
		return HttpResponse(message)

#testing script
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're out.<a href='http://127.0.0.1:8000/'> home page</a>")  # крайне не логично зашивать полный путь url, за некоторыми исклюениями (копирайт, интеграция с каким либо внешним сервисом ) можно было просто сделать: <a href='/'> home page</a>
