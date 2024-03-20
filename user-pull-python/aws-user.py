import boto3
from datetime import datetime
import pandas as pd

def get_last_activity(access_keys):
    if access_keys:
        return max((key['CreateDate'] for key in access_keys)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return "N/A"

def get_iam_users():
    iam = boto3.client('iam')
    users = iam.list_users()['Users']

    user_details = []
    for user in users:
        user_id = user['UserId']
        username = user['UserName']
        creation_time = user['CreateDate'].strftime("%Y-%m-%d %H:%M:%S")
        
        access_keys = iam.list_access_keys(UserName=username)['AccessKeyMetadata']
        last_activity = get_last_activity(access_keys)
        
        user_details.append({'User ID': user_id, 'Username': username, 'Creation Time': creation_time, 'Last Activity': last_activity})

    return user_details

def main():
    users = get_iam_users()
    
    if users:
        print("User ID\t\tUsername\tCreation Time\t\t\tLast Activity")
        for user in users:
            print(f"{user['User ID']}\t{user['Username']}\t{user['Creation Time']}\t{user['Last Activity']}")
        
        df = pd.DataFrame(users)
        df.to_excel("active_users_aws-test.xlsx", index=False)
        print("Output saved to active_users_aws.xlsx")
    else:
        print("No IAM users found.")

if __name__ == "__main__":
    main()
