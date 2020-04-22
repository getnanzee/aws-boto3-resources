import boto3, json, csv

session = boto3.Session(profile_name='aws-profile', region_name='us-east-1')
cognito = session.client("cognito-idp")
user_pools = cognito.list_user_pools(MaxResults=20)                 # Change the MaxResult if the pool count exceeds 20 in your AWS Console

def backup():
    for pool in range(0, len(user_pools['UserPools'])):
        pool_id = user_pools['UserPools'][pool]['Id']
        user_list = cognito.list_users(UserPoolId=pool_id)
        data = user_list['Users']
        export_csv(pool_id, data, 'backup')

def getheaders():
    pool_id = user_pools['UserPools'][0]['Id']                      # Using index value as 0 because the header format is common for all the pools created in Cognito
    headers = cognito.get_csv_header(UserPoolId=pool_id)
    data = headers['CSVHeader']
    export_csv(pool_id, data, 'headers')

def export_csv(pool_id, data, func):
    csv_file = open(pool_id + '-' + func + '.csv', 'a+')
    csv_writer = csv.writer(csv_file)
    count = 0

    if func == 'headers':
        csv_writer.writerow(data)
        csv_file.close()

    else:
        for d in data:
            if count == 0:
                header = d.keys()
                csv_writer.writerow(header)
                count += 1

            csv_writer.writerow(d.values())
            
        csv_file.close()


if __name__ == "__main__":
    print("Choose your action: \n 1. Backup User to CSV \n 2. Get Headers to Import Users \n")
    i = input("Enter your action number: ")

    if i=='1':
        backup()
    
    elif i=='2':
        getheaders()
    else:
        print("Invalid Choice")
