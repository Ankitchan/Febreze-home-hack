from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


import argparse
import base64
import time
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from PIL import Image
from PIL import ImageDraw
from selenium import webdriver

import os
import json
import numpy as np
from pprint import pprint
import math
import operator


from threading import Thread
import time
import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import boto
import boto3



# def get_vision_service():
#     credentials = GoogleCredentials.get_application_default()
#     return discovery.build('vision', 'v1', credentials=credentials)



# def detect_face(face_file, max_results,output_filename):
#     image_content = face_file.read()
#     batch_request = [{
#         'image': {
#             'content': base64.b64encode(image_content).decode('utf-8')
#             },
#         'features': [{
#             'type': 'FACE_DETECTION',
#             'maxResults': max_results,
#             }]
#         }]

#     service = get_vision_service()
#     request = service.images().annotate(body={
#         'requests': batch_request,
#         })
#     response = request.execute()

#     # if response.equals("{u'responses': [\{\}]}"):
#     #     return Response({'Detail': "I checked no one is at the door, I have sent the snapshot on your email !"})

#     json_str = json.dumps(response)
#     data = json.loads(json_str)
#     file_name='live_datasets/'+output_filename[:13]+'.json'
#     #file_name='json_datasets/sparsh_family/live_feed30.json'

#     with open(file_name, 'w+') as f:
#         json.dump(data, f)

#     return response['responses'][0]['faceAnnotations']


# def highlight_faces(image, faces, output_filename):
#     im = Image.open(image)
#     draw = ImageDraw.Draw(im)

#     for face in faces:
#         box = [(v.get('x', 0.0), v.get('y', 0.0))
#                for v in face['fdBoundingPoly']['vertices']]
#         draw.line(box + [box[0]], width=5, fill='#00ff00')

#     im.save(output_filename)


# def main(input_filename, output_filename, max_results):

#     with open(input_filename, 'rb') as image:
 
#         faces = detect_face(image, max_results, output_filename)
#         print('Found {} face{}'.format(
#             len(faces), '' if len(faces) == 1 else 's'))

#         output_addr="output-images/"+output_filename

#         print('Writing to file {}'.format(output_addr))
#         # Reset the file pointer, so we can read the file again
#         image.seek(0)
#         highlight_faces(image, faces, output_addr)


# def lineCalc(x1,y1,z1,x2,y2,z2):
#     return math.sqrt((float(x2)-float(x1))**2+(float(y2)-float(y1))**2+(float(z2)-float(z1))**2)

# def delAB(upper,lower):
#     return upper-lower


# def diff():
#     for each in range(2,len(jsonstats['sparsh'])-1):
#         abs(jsonstats['sparsh'][each] - jsonstats['sparsh2'][each])



# Facejson = {}

# def facefoldertraversal():
#     for eachpersonname in os.listdir(os.getcwd()+"/json_datasets"):
#         if str(eachpersonname).startswith('.'):
#             continue
#         Facejson[eachpersonname]=[]
#         for eachjson in os.listdir(os.getcwd()+"/json_datasets/"+eachpersonname):
#             with open(os.getcwd()+"/json_datasets/"+eachpersonname+"/"+eachjson) as jsonfile:
#                 fullobj = json.load(jsonfile)
#             try:
#                 reqobject = fullobj['responses'][0]['faceAnnotations'][0]['landmarks']
#                 Facejson[eachpersonname].append(jsonarrayval(reqobject))
#             except Exception, e:
#                 print "Error in JSON"
        
            

# def facefoldertraveltest():
#     for eachpersonname in os.listdir(os.getcwd()+"/json_datasets"):
#         print eachpersonname


# def jsonarrayval(jsonobject):
#     jsoncalcuated = []
#     for i in range(0,len(jsonobject)-1):
#         x = lineCalc(jsonobject[i]['position']['x'],jsonobject[i]['position']['y'],jsonobject[i]['position']['z'],jsonobject[i+1]['position']['x'],jsonobject[i+1]['position']['y'],jsonobject[i+1]['position']['z'])
#         jsoncalcuated.append(x)          
#     return jsoncalcuated




def index(request):
	return render_to_response("secureApp/home.html", {})

    #return HttpResponse("Hello, world. You're at the polls index.")


def emailme():
    fromaddr ="alexadoorhack@gmail.com"
    toaddr = "rich9005@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Knock Knock Check who's at the door"
    body = "Hello, I am your voice assistant who monitors your house, since you asked me who's at the door, I have sent you a facial picture of the person at your door. Please Find the attached. "
    msg.attach(MIMEText(body, 'plain'))
    filename = "person_at_door.jpg"
    location= os.getcwd()+"/captured-images/captured-from-door-1.png"
    attachment = open(location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "hacksterio")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()



import boto3


def compare_faces(bucket, key, bucket_target, key_target, threshold=80, region="us-west-2",profile="default"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.compare_faces(
        SourceImage={
            "S3Object": {
                "Bucket": bucket,
                "Name": key
            
            }
        },
        TargetImage={
            "S3Object": {
                "Bucket": bucket_target,
                "Name": key_target
            }
        },
        SimilarityThreshold=threshold,
    )
    return response['FaceMatches']


def search_faces_by_image(bucket, key, collection_id, threshold=75, region="us-west-2",profile="default"):
    rekognition = boto3.client("rekognition", region)
    response = rekognition.search_faces_by_image(
        Image={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        CollectionId=collection_id,
        FaceMatchThreshold=threshold,
    )
    return response['FaceMatches']




@api_view([ 'POST'])
def postImage(request):
    driver = webdriver.Firefox()
    #driver.get('http://ssjsparsh.local:8080/')
    driver.get('http://ssjsparsh.local:8080/')
    
    driver.maximize_window()
    time.sleep(1) # delays for 5 seconds
    driver.save_screenshot('captured-images/captured-from-door.png')

    driver.quit()
    s3 = boto.connect_s3()
    bucket = s3.get_bucket('owner-database-bucket')
    key = bucket.new_key('test.jpg')
    key.set_contents_from_filename('captured-images/captured-from-door.png')
    key.set_acl('public-read')
    try:
        check_similar=False
        meta_info_face=""
        for record in search_faces_by_image("owner-database-bucket", "test.jpg", "HomeOwner1-Collection"):
            check_similar=True
            face = record['Face']
            meta_info_face+=str(face['ExternalImageId'])

#Face inside the Collection
        if check_similar:
            print "Similar Face found..."
            print os.path.splitext(meta_info_face.split('_')[1])[0]

            if str(os.path.splitext(meta_info_face.split('_')[1])[0]) == "owner":
                out_str="Hi {} my lord, I know you are tired, I have turned on the Febreze for you. .".format(meta_info_face.split('_')[0])
                return Response({'Detail': out_str,"Key":"1"})
                # Handle Criminal and Family here
            else:
                if str(os.path.splitext(meta_info_face.split('_')[1])[0]) == "criminal":
                    out_str="Criminal {} is at your door, inform police department. Red Alert, Red Alert.".format(meta_info_face.split('_')[0])
                    return Response({'Detail': out_str,"Key":"3"})
                else:
                    out_str="{}, your {} is at the door.  ".format(meta_info_face.split('_')[0],os.path.splitext(meta_info_face.split('_')[1])[0])             
                    return Response({"Detail": out_str,"Key":"2"})

        else: #Face not inside the Collection
            print "He is a stranger..."
            return Response({'Detail': "You have a stranger at the door.","Key":"0"})



        # matches = compare_faces("owner-database-bucket", "image.jpg","imagestotest", "test.jpg" )
        # print len(matches)
        # return Response({'Detail': "I found a face on the door !"})


    except: #No Face Found
        return Response({'Detail': "I checked no one is at the door !","Key":"0"})



    




    



    # # #Comparing with Criminal Images
    # with open('captured-images/captured-from-door.png', 'rb') as source_image:
    #     source_bytes = source_image.read()

    # with open('criminal-images/image.png', 'rb') as target_image:
    #     target_bytes = target_image.read()

    # response = client.compare_faces(
    #                SourceImage={ 'Bytes': source_bytes },
    #                TargetImage={ 'Bytes': target_bytes },
    #                SimilarityThreshold=SIMILARITY_THRESHOLD
    # )
    # response_Data=response
    # print len(response_Data["FaceMatches"])
    # criminal_match_flag=len(response_Data["FaceMatches"])
    # if criminal_match_flag !=0:
    #     return Response({'Detail': "As per the comparision, the person at the door is a criminal, check your email for images, it is time to inform the Police."})



    #Comparing with Owner Images
    # with open('captured-images/captured-from-door.png', 'rb') as source_image:
    #     source_bytes = source_image.read()

    # with open('owner-images/image.png', 'rb') as target_image:
    #     target_bytes = target_image.read()

    # response = client.compare_faces(
    #                SourceImage={ 'Bytes': source_bytes },
    #                TargetImage={ 'Bytes': target_bytes },
    #                SimilarityThreshold=SIMILARITY_THRESHOLD
    # )
    # response_Data=response
    # print len(response_Data["FaceMatches"])
    # match_flag=len(response_Data["FaceMatches"])
    # if match_flag !=0:
        
    #     return Response({'Detail': "Welcome home Devashish, I have turned on the Febreze, I hope it smells good."})

    # if criminal_match_flag ==0 and match_flag==0:
    #     return Response({'Detail': "As per the comparision, the person at the door is a stranger, check your email for images. "})

    # return Response({'Detail': "I checked no one is at the door !"})







    # It doesnt match the face

    # s3 = boto.connect_s3()
    # bucket = s3.get_bucket('imagestotest')
    # key = bucket.new_key('test.jpg')
    # key.set_contents_from_filename('captured-images/captured-from-door-1.png')
    # key.set_acl('public-read')
    #driver.save_screenshot('captured-images/captured-from-door-2.png')
    


    # try:
    #     main('captured-images/captured-from-door-1.png', 'output_face_1.jpg', 2)
    #     main('captured-images/captured-from-door-2.png', 'output_face_2.jpg', 2)
    # except Exception, e:
    #     print str(e)
    #     if str(e) in "'faceAnnotations'":
    #         return Response({'Detail': "I checked no one is at the door !"})
    #     else:
    #         return Response({'Detail': "I couldnt find who is at the door, you should blame Google for that; They should have better cloud services like Amazon !"})
        
    
    # data=[]
    # with open("live_Datasets/output_face_1.json") as data_file:
    #     json_data = json.load(data_file)
    #     data = json_data['responses'][0]['faceAnnotations'][0]['landmarks']
    # with open("live_Datasets/output_face_2.json") as data_file:
    #     json_data = json.load(data_file)
    #     data1 = json_data['responses'][0]['faceAnnotations'][0]['landmarks']
   
    # livedataarrays = []
    # livedataarrays.append(jsonarrayval(data))
    # livedataarrays.append(jsonarrayval(data1))
    # resultcounter = {}
    # matchcounterlist={}
    # for eachlivearray in livedataarrays:
    #     for eachstoredarraylistkey in Facejson:
    #         resultcounter[eachstoredarraylistkey] = 0
    #         matchcounterlist[eachstoredarraylistkey] = []
    #         for eachstoredarray in Facejson[eachstoredarraylistkey]:
    #             counter =0
    #             lenoflist  = len(eachstoredarray)
    #             for i in range(0,lenoflist-1):
    #                 if abs(delAB(eachstoredarray[i],eachlivearray[i]))<20:
    #                     counter+=1
    #             matchcounterlist[eachstoredarraylistkey].append([float(counter)/float(lenoflist)])
    # print matchcounterlist
    # maxconfidence = 0.0
    # secondmax = 0.0
    # for key in matchcounterlist:
    #     print key
    #     print np.mean(matchcounterlist[key])
    #     if np.mean(matchcounterlist[key])>maxconfidence:
    #         secondmax = maxconfidence
    #         maxconfidence  = np.mean(matchcounterlist[key])

    # if maxconfidence > 0.71 and (maxconfidence-secondmax)<0.05:
    #     try:
    #         t = Thread(target=emailme)
    #         t.start()
    #     except Exception, e:
    #         print "Unable to start new thread"       
    #     return Response({'Detail':"I couldnt recognize the person, I think he is a stranger"})
    # key_chosen=max(matchcounterlist.iteritems(), key=operator.itemgetter(1))[0]
    # print key_chosen
    # strArr=key_chosen.split('_')
    # print strArr
    # try:
    #     t = Thread(target=emailme)
    #     t.start()
    # except Exception, e:

    #     print("Unable to start new thread")
    # str_resp="As per our comparision algorithm the person at the door is, "+strArr[0]+" and he is a "+strArr[1]+", check your email for his image !"
    # return Response({'Detail': str_resp})


