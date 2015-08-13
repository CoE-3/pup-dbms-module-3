import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class createthesis(ndb.Model):
    year = ndb.StringProperty(indexed=True)
    title1 = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section = ndb.StringProperty(indexed=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())

class ThesisEntryHandler(webapp2.RequestHandler):
 	def get(self):	
 		thesis1 = createthesis.query().order(-createthesis.section).fetch()
 		thesis_list = []

	 	for t in thesis1:
	 		thesis_list.append({
				'year': t.year,
 				'title1': t.title1,
 				'abstract': t.abstract,
 				'adviser': t.adviser,
 				'section': t.section
	 			})

	 	response = {
	 		'result': 'OK',
	 		'data': thesis_list
	 	}							
	 	self.response.headers['Content-Type'] = 'application/json'
	 	self.response.out.write(json.dumps(response))

 	def post(self):	
 		thesis1 = createthesis()								
 		thesis1.year = self.request.get('year')
 		thesis1.title1 = self.request.get('title1')
 		thesis1.abstract = self.request.get('abstract')
 		thesis1.adviser = self.request.get('adviser')
 		thesis1.section = self.request.get('section')
 		thesis1.put() #returns the key of the entity created
 		
 		self.response.headers['Content-Type'] = 'application/json'
 		response = {
 		'result': 'OK',
 		'data': {
 			'year': thesis1.year,
 			'title1': thesis1.title1,
 			'abstract': thesis1.abstract,
 			'adviser': thesis1.adviser,
 			'section': thesis1.section
 			}
 		}
 		self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
	('/api/thesis', ThesisEntryHandler),
    ('/home', MainPageHandler),
    ('/', MainPageHandler)
], debug=True)