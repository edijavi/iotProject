import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('/home/pi/AppPyCharm/iotmotionsensor-e737c-firebase-adminsdk-byfm4-2183495c4a.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_cloud_firestore(file_name, fileUrl):
    doc_ref = db.collection(u'images').document(u'%s' % file_name)
    data = {
        u'name': u'%s' % file_name,
        u'filepath': u'%s' % fileUrl
    }
    doc_ref.set(data)

def delete_cloud_firestore(file_name):
    doc_ref = db.collection(u'images').document(u'%s' % file_name)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.dedoc_ref.delete()
        print("Doc deleted.")

    else:
        print("Doc Not Found.")


