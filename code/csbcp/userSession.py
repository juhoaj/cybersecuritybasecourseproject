import django.contrib.sessions.backends.db as db
from csbcp.threadVariable import *

class SessionStore(db.SessionStore):

	def _get_new_session_key(self):
		while True:
			session_key = f"session-{getUser_id()}"
			if not self.exists(session_key):
				return session_key