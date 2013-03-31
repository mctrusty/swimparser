from google.appengine.ext import ndb

class Workout(ndb.Model):
	user = ndb.UserProperty()
	date = ndb.DateTimeProperty()
	workout = ndb.JsonProperty()