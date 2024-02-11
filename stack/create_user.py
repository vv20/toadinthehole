import sys

import boto3

from common import Component

from get_cognito_user_pool_id import get_cognito_user_pool_id


def create_user(environment, email, password):
    client = boto3.client('cognito-idp')
    user_pool_id = get_cognito_user_pool_id(environment)
    client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=email,
            TemporaryPassword=password,
            UserAttributes=[
                {
                    "Name": "email",
                    "Value": email
                },
                {
                    "Name": "email_verified",
                    "Value": "true"
                }])
    client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=email,
            Password=password,
            Permanent=True)

if __name__ == '__main__':
    environment = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    create_user(environment, email, password)
