from redis_sessions_fork.session import SessionStore
import pickle

__author__ = 'adarwazeh'


class SessionStore(SessionStore):
    def encode(self, session_dict):
        return pickle.dumps(session_dict)

    def decode(self, session_data):
        try:
            return pickle.loads(session_data)
        except:
            return {}