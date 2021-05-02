import flask
from flask import request, jsonify,make_response
from database import Database
import datetime
app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.errorhandler(500)
def page_not_found(e):
    return make_response({'status':500, 'messeage':'Internal Server Error'}, 500)

@app.route('/api/v1/create', methods=['POST'])
def create():
	if request.method == 'POST':
		data = request.json	
		type = data.get("audioFileType", None)
		if type is None:
			return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		audio_type = type
		metadata = data.get("audioFileMetadata")
		if not metadata:
			return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		
		if metadata["duration_time"] <= 0:
			metadata["duration_time"] = 0
		
		metadata["uploaded_time"] = datetime.datetime.now()
		if type == "song":
			if len(metadata["name"]) > 100:
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		elif type == "podcast":
			if len(metadata["name"]) > 100:
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
			participent = metadata.get("participents", None)
			if(participent is None or len(participent) > 10 or any(i for i in participent if len(i) > 100)):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
			hosts = metadata.get("host", None)
			
			if(hosts is None or len(hosts) > 100):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		elif type == "audiobook":
			title = metadata.get("title", None)
			if(title is None or len(title)> 100):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
			author = metadata.get("author", None)
			if(author is None or len(author)> 100):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
			narrator = metadata.get("narrator", None)
			if(narrator is None or len(narrator)> 100):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		Database().create(audio_type, metadata)
		return make_response({'status':'200 OK', 'messeage':'Action is sucessful'}, 200)
	else:
		return make_response({'status':400, 'messeage':'The request is invalid'}, 400)

@app.route('/api/v1/update/<audioFileType>/<audioFileID>', methods=['PUT'])
def update(audioFileType, audioFileID):
	if request.method == 'PUT':
		request_data = request.json
		metadata = request_data.get("audioFileMetadata")
		audio_type = request_data.get("audioFileType")
		if not metadata:
			return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		data = request.get_json()
		metadata["uploaded_time"] = datetime.datetime.now()
		if metadata["duration_time"] <= 0:
			metadata["duration_time"] = 0
		if type == "song":
			if len(metadata["name"]) > 100:
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		elif type == "podcast":
			if len(metadata["name"]) > 100:
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
			participent = metadata.get("participents", None)
			if(participent is None or len(participent) > 10 or any(i for i in participent if len(i) > 100)):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
			hosts = metadata.get("host", None)
			
			if(hosts is None or len(hosts) > 100):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		elif type == "audiobook":
			title = metadata.get("title", None)
			if(title is None or len(title)> 100):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
			author = metadata.get("author", None)
			if(author is None or len(author)> 100):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
			narrator = metadata.get("narrator", None)
			if(narrator is None or len(narrator)> 100):
				return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
		if 'audioFileType' and 'audioFileMetadata' in data.keys():
			Database().update(audioFileType, audioFileID, audio_type, metadata)
			return make_response({'status':'200 OK', 'messeage':'Action is sucessful'}, 200)
		else:
			return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
	else:
		return make_response({'status':400, 'messeage':'The request is invalid'}, 400)
@app.route('/api/v1/delete/<audioFileType>/<audioFileID>', methods=['DELETE'])
def delete(audioFileType, audioFileID):
	if request.method == 'DELETE':
		Database().delete(audioFileType, audioFileID)
		return make_response({'status':'200 OK', 'messeage':'Action is sucessful'}, 200)
	else:
		return make_response({'status':400, 'messeage':'The request is invalid'}, 400)

@app.route('/api/v1/get/<audioFileType>', methods=['GET'])
def get_by_audiofiletype(audioFileType):
	if request.method == 'GET':
		data = Database().get_by_audiofile(audioFileType)
		return make_response({"data":data}, 200)
	else:
		return make_response({'status':400, 'messeage':'The request is invalid'}, 400)

@app.route('/api/v1/get/<audioFileType>/<audioFileID>', methods=['GET'])
def get_by_audioID(audioFileType, audioFileID):
	if request.method == 'GET':
		data = Database().get_by_audioID(audioFileType, audioFileID)
		return make_response({"data":data}, 200)
	else:
		return make_response({'status':400, 'messeage':'The request is invalid'}, 400)

app.run()