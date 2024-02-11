import sys

import boto3

from common import Component


def get_cognito_user_pool_id(environment):
    client = boto3.client('cognito-idp')
    user_pools = client.list_user_pools(MaxResults=10)['UserPools']
    user_pool = [up for up in user_pools if up['Name'] == Component.USER_POOL.get_component_name(environment)][0]
    return user_pool['Id']

if __name__ == '__main__':
    environment = sys.argv[1]
    print(get_cognito_user_pool_id(environment))
