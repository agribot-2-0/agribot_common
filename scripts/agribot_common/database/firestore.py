import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Firestore(object):
    def __init__(self, certificate_file):
        self.certificate_file = certificate_file
        self.database = None
        self.initialize()

    def initialize(self):
        if not firebase_admin._apps:  # pylint: disable=protected-access
            cred = credentials.Certificate(self.certificate_file)
            firebase_admin.initialize_app(cred, {
                'projectID': 'agribot-cd437',
            })
            self.database = firestore.client()
        return True

    def get_uids_for_rsn(self, rsn):
        uids = []
        users_ref = self.database.collection(u'users').stream()
        for user in users_ref:
            robots_ref = self.database.collection(u'users').document(
                user.id).collection('robots').stream()
            for robot in robots_ref:
                if robot.id == rsn:
                    uids.append(user.id)
        return uids

    def register_callback_on_collection_change(self, collection_path,
                                               on_collection_callback):
        self.database.collection(collection_path).on_snapshot(
            on_collection_callback)
