from pymongo import MongoClient
import pymongo
# from Resources import parser
# import urllib.parse
# import socket

class Database():

	def __init__(self):
		host = MongoClient("mongodb://127.0.0.1:27017")
		database = host['filled']
		self.collection = database['audio_files_record']

	def create(self, audiofiletype, audiometadata):
		if self.collection.find_one({'audio_file_type':audiofiletype}):
			data = self.collection.find({'audio_file_type':audiofiletype}).sort([('_id', pymongo.DESCENDING)]).limit(1)
			for i in data:
				if 'id' in i:
					id = int(i['id']) + 1
		else:
			id = 0
		self.collection.insert({'id':id,'audio_file_type':audiofiletype,'audiometadata':audiometadata})
		return True

	def update(self,audioFileType, audioFileID, dataaudioFileType, dataaudioFileMetadata):
		if self.collection.find_one({'audio_file_type':audioFileType, 'id':int(audioFileID)}):
			if self.collection.find_one({'audio_file_type':dataaudioFileType}):
				data = self.collection.find({'audio_file_type':dataaudioFileType}).sort([('_id', pymongo.DESCENDING)]).limit(1)
				for i in data:
					if 'id' in i:
						id = int(i['id']) + 1
			else:
				id = 0
			self.collection.update({'audio_file_type':audioFileType, 'id':int(audioFileID)},{'$set': {"id":id,"audio_file_type":dataaudioFileType,"audiometadata":dataaudioFileMetadata}})
			return True
		else:
			return False

	def delete(self,audioFileType, audioFileID):
		if self.collection.find_one({'audio_file_type':audioFileType, 'id':int(audioFileID)}):
			self.collection.delete_one({'audio_file_type':audioFileType, 'id':int(audioFileID)})
			return True
		else:
			return False

	def get_by_audiofile(self, audioFileType):
		data = []
		for i in self.collection.find({'audio_file_type':audioFileType},{"_id":0}):
			data.append(i)
		return data

	def get_by_audioID(self,audioFileType, audioFileID):
		return self.collection.find_one({'audio_file_type':audioFileType, 'id':int(audioFileID)},{"_id":0})