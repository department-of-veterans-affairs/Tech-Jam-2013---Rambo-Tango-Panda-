import json
import datetime
import bottle
import pymongo
import urllib2
import string
import StringIO
import random
import qrcode
import base64
from django.utils import simplejson
from bottle import route, run, request, abort
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.documents

@route('/qrcode/:id', method = 'GET')
def get_qrcode(id):
    #get information for the id
    #create string for encoding using datetime, timetolive, requester_id, eoctype, random_value(opt)
    data=dict(request.query)
    rnd=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(25))
    qr_string= {'Datetime':str(datetime.datetime), 'timetolive':30, 'requester_id':id, 'eoctype':data['eoctype'], 'rnd':rnd}
    jstring = json.dumps(qr_string)
    #encrypt the string
    output=StringIO.StringIO()
    img=qrcode.make(qr_string)
    #convert encrypted string o qrcode
    #read sample qrcode file C:\Users\u93637\care\sample_qr_code.jpeg
    img.save(output,'JPEG')
    return output.getvalue()
    
@route('/eoc_event/:id', method = 'POST')
def put_document(id):
    #print request.tostring()
    data=dict(request.query)
    if not data:
        abort(400, 'No data received')
    # Decode base-64
    new_image=base64.standard_b64decode(request.body.read())
    # Decode the QR Code
    url = "http://www.esponce.com/api/v3/decode?format=jpg"
    req = urllib2.Request(url, new_image)
    response = urllib2.urlopen(req).read()
    # The response is now decoded, so store it in the DB.
    response_dict = json.loads(response)
    #Decrypt the text version of when encryption is installed  
    #Store the values extracted from the request
    #patient_id
    #provider_id
    #datetime
    #eoctype
    #submitter_role
    #Merge query and image  now	
    data['qr']=response_dict
    retval=db['eoc'].insert(data)
    return retval
    #need error handling

@route('/list_providers/', method='GET')
def get_provider_list(patient_id):
    #get a list of providers for the given patient_id
    #return the provider name, count of eocs, and last eoc
    return pr_list

@route('/register/', method = 'PUT')
def register_user():
    data=dict(request.query)
    if not data:
        abort(400, 'No data received')
    # we need to decode the data in the query for storage in the DB
    # not implemented yet: organization, email, phone, gender
    # in process: Role, firstname, lastname, dob, acct_nbr, staff_photo 
    retval=db['eoc'].insert(data)
    return retval


bottle.debug(True) 
run(host='192.168.43.160')
