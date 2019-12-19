# sudo pip install google-cloud-storage
# sudo pip install firebase

from google.cloud import storage
from firebase import firebase
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<add your credentials path>"
firebase = firebase.FirebaseApplication('<your firebase database path>')
client = storage.Client()
bucket = client.get_bucket('<your firebase storage path>')
# posting to firebase storage
imageBlob = bucket.blob("/")
# imagePath = [os.path.join(self.path,f) for f in os.listdir(self.path)]
imagePath = "<local_path>/image.png"
imageBlob = bucket.blob("<image_name>")
imageBlob.upload_from_filename(imagePath)
