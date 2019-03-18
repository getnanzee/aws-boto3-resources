"""

**************************************************
					         *
Author = Abhishek Sharma <mail.abhi13@gmail.com> *
						 *
**************************************************

A simple script to bulk restore
"""

import threading
from s3mgr import s3mgr #run clone https://github.com/paliwalvimal/aws-s3mgr-python.git to import the py file from Git 

def store_to_notepad(bucket, keys):
    f = open(bucket + ".txt", "a+")
    f.write(bucket + " - " + keys + "\n")
    f.close()

if __name__ == "__main__":

    bucket_list = ["bucket_name"] #Enter the bucket name here!!
    for bucket in bucket_list:
        sm = s3mgr(profile='Default') #You can change the aws cli profile from here 
        result = sm.list_contents(bucket, "path") #Specify the folder in your s3 bucket
        for count in range(0, len(result["Files"])):
            key = result["Files"][count]["Key"]
            store_to_notepad(bucket, keys)
            t = (threading.Thread(target=sm.restore_from_glacier, args=(bucket,key,)))
            t.start()
            #t.join()
