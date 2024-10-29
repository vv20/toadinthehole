
import sys

import boto3

from ..common import Component


def get_identity_pool_id(environment):
    client = boto3.client('cognito-identity')
    id_pools = client.list_identity_pools(MaxResults=10)['IdentityPools']
    id_pool = [idp for idp in id_pools if Component.IDENTITY_POOL.get_component_name(environment) in idp['IdentityPoolName']][0]
    return id_pool['IdentityPoolId']

if __name__ == '__main__':
    environment = sys.argv[1]
    print(get_identity_pool_id(environment))
