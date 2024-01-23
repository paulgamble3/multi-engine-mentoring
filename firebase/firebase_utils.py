import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("./firebase/iso-eval-firebase-adminsdk-zs022-968af88ead.json")

if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app(cred, {
        'databaseURL':"https://iso-eval-default-rtdb.firebaseio.com/"
        })

def write_task_item(item, task_name):
    ref = db.reference(task_name)
    ref.push(item)