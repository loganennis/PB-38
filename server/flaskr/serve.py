import click
import functools

from flask import Flask, Blueprint, flash, request, render_template
from flask.cli import with_appcontext

# For forms
from flask_wtf import Form
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import NumberRange, InputRequired
import requests
import json

# Add blueprint
app_blueprint = Blueprint('app', __name__, url_prefix='')

class TraitsForm(Form):
	''' Event parameters form '''
	speciality_types = ['Neurology', 'Pulmonology', 'Family Medicine', 'Clinical Genetics and Genomics', 'Clinical Counselling', 'Plastic Surgery', 'Anesthesiology', 'Pediatrics', 'Allergy and Immunology', 'Aerospace Medicine', 'Dermatology', 'Cardiology', 'None']
	event_types = ['Video', 'Report', 'Voice']
	visit_types = ['Counseling Video', 'Consulatation Video', 'Consulatation Report', 'Consultation Email', 'Conseling Email', 'Conseling Voice', 'Consultation Voice', 'Conseling Report']
	
	specialities = []
	events = []
	visits = []
	for i in range(0, len(speciality_types)):
		specialities.append((i + 1, speciality_types[i]))

	for i in range(0, len(event_types)):
		events.append((i + 1, event_types[i]))

	for i in range (0, len(visit_types)):
		visits.append((i + 1, visit_types[i]))

	duration 	= IntegerField('Duration', validators=[InputRequired(),NumberRange(min=1)])				# Must be greater than 0
	speciality 	= SelectField('Speciality',coerce=int, choices=specialities)	
	event_type 	= SelectField('Event Type',coerce=int, choices=events)
	visit_type 	= SelectField('Visit Type',coerce=int, choices=visits)
	submit		= SubmitField('Get Price')

"""
FRONT-END ENDPOINTS
"""
@app_blueprint.route('/', methods=('GET', 'POST'))
def getPrice():
	form=TraitsForm(csrf_enabled=False)
	if request.method == 'GET':
		'''Render form to input visit details'''
		return render_template('entertraits.html', form=form)
	
	if request.method == 'POST':
		'''Request price for given details'''
		form_data = request.form
		if form.validate_on_submit() == False:
			flash("Invalid Input")
			return render_template('entertraits.html', form=form)
		data = {'duration': form_data['duration'], 'speciality' : form_data['speciality'], 'eventType' : form_data['event_type'], 'type': form_data['visit_type']}
		r = requests.get(request.base_url + 'api/calculate', params=data)
		price = json.loads(r.text)['price']
		return render_template('showprice.html', price=price)