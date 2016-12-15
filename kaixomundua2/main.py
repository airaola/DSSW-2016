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
import re
from google.appengine.ext.webapp \
	import template


USUARIO_RE = re.compile(r"^([a-zA-Z0-9_-])$")
CLAVE_RE = re.compile(r"^.{6,20}$")
EMAIL_RE = re.compile(r"^([a-zA-Z0-9_.])+\@(([a-zA-Z0-9])+\.)+([a-zA-Z0-9]{2,4})$")

def validar_usuario(usuario):
	return USUARIO_RE.match(usuario)

def validar_clave(clave):
	return CLAVE_RE.match(clave)

def validar_email(email):
	return EMAIL_RE.match(email)
	
		
class MainHandler(webapp2.RequestHandler):
    def get(self):
	    self.response.write(template.render('main.html',{}))

    def post(self):
		
		USUARIO=self.request.get("usuario")
		CLAVE=self.request.get("clave")
		DOBLECLAVE=self.request.get("dobleclave")
		EMAIL=self.request.get("email")
	
		error = False
		
		error_de_usuario=''
		error_de_clave=''
		error_de_email=''
		
		if not(validar_usuario(USUARIO)):
			error_de_usuario='Nombre incorrecto!!'
			error = True
		if not((validar_clave(CLAVE)) and (CLAVE==DOBLECLAVE)):	
			error_de_clave='Password incorrecto!!'
			error = True	
		if not(validar_email(EMAIL)):
			error_de_email='Email incorrecto!!'			
			error = True
		
		if (error):		
			self.response.write(template.render('main.html',{}))
			self.response.write(error_de_usuario + ' ' + error_de_clave + ' ' + error_de_email)
		else:
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

		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/eu', BasqueHandler),
	('/es', SpanishHandler),
	('/en', EnglishHandler)
], debug=True)













































#USER_RE= re.compile(r"^[a-zA-Z0-9](3,20)$")