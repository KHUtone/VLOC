import subprocess

def upload_files(uploadpath):
    print("Start uploading files")
    command = "gsutil -m mv {} gs://2019-khuthon-ddingdong/".format(uploadpath)
    subprocess.call(command, shell=True)
    print("Finished")
