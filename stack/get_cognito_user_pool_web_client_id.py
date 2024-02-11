import sys

import boto3

from common import Component
from get_cognito_user_pool_id import get_cognito_user_pool_id


def get_cognito_user_pool_web_client_id(environment):
    user_pool_id = get_cognito_user_pool_id(environment)
    client = boto3.client('cognito-idp')
    user_pool_client = client.list_user_pool_clients(UserPoolId=user_pool_id)['UserPoolClients'][0]
    user_pool_client_id = user_pool_client['ClientId']
    return user_pool_client_id

if __name__ == '__main__':
    environment = sys.argv[1]
    print(get_cognito_user_pool_web_client_id(environment))
