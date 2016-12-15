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

class MainHandler(webapp2.RequestHandler):
    def get(self):

		self.response.write('<head><link type="text/css" href="/static/css/bootstrap.css"></head><h1>Kaixo Mundoa </h1> <img src=/images/irudia.gif>')
        
class SpanishHandler(webapp2.RequestHandler):
    def get(self):
		self.response.write('<head><link type="text/css" href="/static/css/bootstrap.css"></head><h1>Hola Mundo </h1> <img src=/images/irudia.gif>')
		
class EnglishHandler(webapp2.RequestHandler):
    def get(self):
		self.response.write('<head><link type="text/css" href="/static/css/bootstrap.css"></head><h1>Hello World </h1> <img src=/images/irudia.gif>')

app = webapp2.WSGIApplication([
<<<<<<< HEAD
    ('/', MainHandler),
=======
    ('/eu', MainHandler),
>>>>>>> 7a2bd714d7c99892fa473a327dc7df0aee45b35a
	('/es', SpanishHandler),
	('/en', EnglishHandler)
], debug=True)
