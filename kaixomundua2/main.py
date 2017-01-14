#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# REG_FORM=''' ................. JS + HTML ...................'''
#
#registroHandler (.......)
#
#def get (self);
#	self.request.out.write (REG_FORM)
#
#def post (self)
#	self.request.get ('email')
#

import webapp2
from webapp2_extras import sessions
import session_module
import re
import json
from google.appengine.ext import ndb
from google.appengine.ext.webapp \
	import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers	
import urllib
	

class Image(ndb.Model):
    user = ndb.StringProperty()
    public = ndb.BooleanProperty()
    blob_key = ndb.BlobKeyProperty()
	
	
	
class Registro (ndb.Model):
	user = ndb.StringProperty(required = True)
	password = ndb.StringProperty(required = True) 
	correo = ndb.StringProperty(required = True)
	when = ndb.TimeProperty (auto_now_add = True)
	


USUARIO_RE = re.compile(r"^[a-zA-Z0-9]{1,30}")
CLAVE_RE = re.compile(r"^.{6,20}$")
EMAIL_RE = re.compile(r"^([a-zA-Z0-9_.])+\@(([a-zA-Z0-9])+\.)+([a-zA-Z0-9]{2,4})$")

def validar_usuario(usuario):
	return USUARIO_RE.match(usuario)

def validar_clave(clave):
	return CLAVE_RE.match(clave)

def validar_email(email):
	return EMAIL_RE.match(email)
	

class MainHandler(session_module.BaseSessionHandler, webapp2.RequestHandler):
    def get(self):
		self.response.write(template.render('main.html',{}))

    def post(self):
	
		USUARIO=self.request.get('usuario')
		CLAVE=self.request.get('clave')
		DOBLECLAVE=self.request.get('dobleclave')
		EMAIL=self.request.get('email')
		
		error = False
		error2 = False
		
		error_de_usuario=''
		error_de_clave=''
		error_de_email=''
		
		usuario_repetido=''
		email_repetido=''
		
		if not(validar_usuario(USUARIO)):
			error_de_usuario='Nombre incorrecto!!'
			error = True
		if not((validar_clave(CLAVE)) and (CLAVE==DOBLECLAVE)):	
			error_de_clave='Password incorrecto!!'
			error = True
		if not(validar_email(EMAIL)):
			error_de_email='Email incorrecto!!'			
			error = True
	
		When=''
		nusers = Registro.query(Registro.user==USUARIO).count()
		if (nusers>=1):
			usuario_repetido='Ese usuario ya esta registrado'
			error2 = True
		nemails = Registro.query(Registro.correo==EMAIL).count()
		if (nemails>=1):
			email_repetido='Ese e-mail ya esta registrado'
			error2 = True
	
		if (error or error2):		
			self.response.write(template.render('main.html',{}))
			if (error):
				self.response.write(error_de_usuario + ' ' + error_de_clave + ' ' + error_de_email)
			if (error2):		
				self.response.write(usuario_repetido + ' ' + email_repetido)
		if (error2 == False and error == False):
			registro = Registro()
			registro.user = USUARIO
			registro.password = CLAVE
			registro.correo = EMAIL		
			registro.put()
			self.response.write(template.render('main.html',{}))
			self.response.write('''<div><span class="label">'''+"Kaixo: "+self.request.get("usuario")+'''</span><br><span class="label">Se ha registrado correctamente. Ahora puede iniciar sesion</span></div>''')

class LogoutHandler(session_module.BaseSessionHandler):
	def get (self): 
		del self.session['UserSesion'] 
		self.redirect('/')

	
class ValidacionMainHandler ( webapp2.RequestHandler ) :
	def get (self) :
		error3 = False
		emailMal = ""
		email = self.request.get ('emailAjax')
		
		if not validar_email (email) :
			error3 = True
			emailMal = "No es un email valido"
		
		nemailsrep = Registro.query(Registro.correo==email).count()
		if (nemailsrep>=1):
			error3 = True
			emailMal="Ese e-mail ya esta registrado"
		
		self.response.write (emailMal)
		
class BasqueHandler(webapp2.RequestHandler):
    def get(self):
		self.response.write(template.render('main.html',{}))
		self.response.write('''<span class="label">'''+"Kaixo: "+self.request.get("usuario")+'''</span><br><span class="label">Tus datos son correctos</span>''')
		
class BasqueHandler(webapp2.RequestHandler):
    def get(self):
		self.response.write('<head><link type="text/css" rel="stylesheet" href="/css/main.css"></head><h1>Kaixo Mundoa </h1> <img src=/images/irudia.gif>')
        
class SpanishHandler(webapp2.RequestHandler):
    def get(self):
		self.response.write('<head><link type="text/css" rel="stylesheet" href="/css/main.css"></head><h1>Hola Mundo </h1> <img src=/images/irudia.gif>')
		
class EnglishHandler(webapp2.RequestHandler):
    def get(self):
		self.response.write('<head><link type="text/css" rel="stylesheet" href="/css/main.css"></head><h1>Hello World </h1> <img src=/images/irudia.gif>')
		
class SesionHandler(session_module.BaseSessionHandler, webapp2.RequestHandler):
	def get(self):
		if not self.session.get('UserSesion'):
			EMAILSESION=self.request.get('emailInicio')
			CLAVESESION=self.request.get('claveInicio')
			if not(validar_email(EMAILSESION)):
				self.redirect('/')		
			if not(validar_clave(CLAVESESION)):	
				self.redirect('/')
			if (EMAILSESION=="" or CLAVESESION==""):
				self.redirect('/')

			matchRegister = Registro.query(ndb.AND(Registro.password == CLAVESESION, Registro.correo==EMAILSESION)).count()
			if (matchRegister == 1):		
				self.session['UserSesion'] = EMAILSESION
				self.response.write(template.render('pagina_sesion.html',{}))
			else:
				self.redirect('/')
		else:
			self.response.write(template.render('pagina_sesion.html',{}))

class SubidaHandler(session_module.BaseSessionHandler, blobstore_handlers.BlobstoreUploadHandler):
	def get (self):
		if not self.session.get('UserSesion'):
			self.redirect('/')
		else:
			upload_url = blobstore.create_upload_url('/upload_photo')
			# To upload files to the blobstore, the request method must be "POST"
			# and enctype must be set to "multipart/form-data".
			self.response.out.write("""
				<html> <head><link type="text/css" rel="stylesheet" href="/css/main.css"></head>
				<body>
				<form action="%(url)s" method="POST" enctype="multipart/form-data">
				<input type="file" name="file"><br>
				<input type="radio" name="access" value="public" checked="checked" />    Public
				<input type="radio" name="access" value="private" /> Private<p>
				<input type="submit" name="submit" value="Submit">
				</form><form method="get" action="/sesion">
				<input type="submit" name="atras" value="Atras">
				</form></body></html>""" % {'url':upload_url})	
	def post(self):
		upload_files = self.get_uploads('file')
		blob_info = upload_files[0] # guardo la imagen en el BlobStore
		img = Image(user=self.session.get('UserSesion'),public=self.request.get("access")=="public", blob_key=blob_info.key())
		img.put() #guardo el objeto Image
		self.redirect('/sesion')

			
			
class ViewHandler(session_module.BaseSessionHandler, blobstore_handlers.BlobstoreDownloadHandler):
	def get(self):
		if not self.session.get('UserSesion'):
			self.redirect('/')
		else:
			usuario = self.session.get('UserSesion')
			public_images = Image.query().filter(Image.public == True)
			private_images = Image.query().filter(Image.public == False).filter(Image.user == usuario)
			images_string='''<div style="position: absolute; height: 5000px; width:5000px;"><form method="get" action="/sesion"><input type="submit" value="Atras"></form>
			<head><link type="text/css" rel="stylesheet" href="/css/main.css"></head><h2>Las imagenes publicas:</h2>'''
			for i, picture in enumerate(public_images):
				images_string += '<img name="img{0}" src="/serve/{1}" height="240" width="240"alt="" />'.format(i,picture.blob_key)
			images_string += '''<h2>Las imagenes privadas:</h2>'''
			for i, picture in enumerate(private_images):
				images_string += '<img name="img{0}" src="/serve/{1}" height="240" width="240"alt="" />'.format(i,picture.blob_key)
			images_string += '''</div>'''
			self.response.out.write(images_string)
		


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
 	 def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)
		self.send_blob(blob_info)

	
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/eu', BasqueHandler),
	('/es', SpanishHandler),
	('/en', EnglishHandler),
	('/validacion', ValidacionMainHandler),
	('/sesion', SesionHandler),
	('/upload_photo', SubidaHandler),
	('/logout', LogoutHandler),
    ('/view_photos', ViewHandler),
    ('/serve/([^/]+)?', ServeHandler)]
	, config = session_module.myconfig, debug=True)
