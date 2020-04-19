import boto3
import json, codecs, os

session = boto3.Session(profile_name='aws-profile', region_name='ap-south-1')
client = session.client('apigateway')
apis = client.get_rest_apis()
docs = []

for i in range(0, len(apis['items'])):
    id = apis['items'][i]['id']
    name = apis['items'][i]['name']

    stages = client.get_stages(restApiId=id)

    for stage in range(0, len(stages['item'])):
        stageName = stages['item'][stage]['stageName']
        # stageList.append(sbody = obj['Body']tageName)
        export = client.get_export(restApiId=id, stageName=stageName, exportType='swagger', accepts='application/json')
        body = export['body']
        filename = stageName + '-' + name + '.json'
        
        docs.append({"url": filename, "name": stageName + '-' + name})
        
        file = codecs.getreader('utf-8')(body)
        for ln in codecs.getreader('utf-8')(body):
            file = open(os.path.join('./eks/', stageName + '-' + name + '.json'), "a+")
            file.write(ln)
            file.close


file = open(os.path.join('./eks/', 'docs-list.json'), 'a')
file.write(str(docs))
file.close()
