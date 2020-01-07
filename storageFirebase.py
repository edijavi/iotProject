import os
from google.cloud import storage
from firebase import firebase


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/AppPyCharm/iotmotionsensor-e737c-firebase-adminsdk-byfm4-2183495c4a.json"
firebase = firebase.FirebaseApplication('https://iotmotionsensor-e737c.firebaseio.com')
bucket_name = 'iotmotionsensor-e737c.appspot.com'


def upload_blob(destination_blob_name, source_file_name):
    """Uploads a file to the bucket."""
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("images/%s" % destination_blob_name)

    blob.upload_from_filename(source_file_name)
    blob.make_public()
    fileUrl = blob.public_url
    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        ),
        "Blob {} is publicly accessible at {}".format(
        blob.name, fileUrl)
    )
    return fileUrl


def list_blobs():
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"
    storage_client = storage.Client()
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    numFiles = 0
    for blob in blobs:
        numFiles += 1
    return numFiles

def delete_blob(blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("images/%s" % blob_name)
    blob.delete()

    print("Blob {} deleted.".format("images/%s" % blob_name))


