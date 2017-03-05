

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


check_similar=False
meta_info_face=""

for record in search_faces_by_image("owner-database-bucket", "test.jpg", "HomeOwner1-Collection"):
	check_similar=True
	face = record['Face']
	# print len(face)
	# print "Matched Face ({}%)".format(record['Similarity'])
	# print "  FaceId : {}".format(face['FaceId'])
	# print "  ImageId : {}".format(face['ExternalImageId'])
	meta_info_face+=str(face['ExternalImageId'])

if check_similar:
	print "Similar Face found..."
	print meta_info_face
else:
	print "He is a stranger..."


"""
	Expected output:

	Matched Face (96.6647949219%)
	  FaceId : dc090f86-48a4-5f09-905f-44e97fb1d455
	  ImageId : test.jpg

"""