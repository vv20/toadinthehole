import json
import os
import sys

from common import Domain
from get_cognito_user_pool_id import get_cognito_user_pool_id
from get_cognito_user_pool_web_client_id import \
    get_cognito_user_pool_web_client_id


def create_amplify_config(environment):
    region = os.getenv('AWS_REGION')
    domain_name = os.getenv('DEPLOYMENT_DOMAIN_NAME')

    with open('frontend/src/amplifyconfiguration.json.template', 'r') as template_file:
        template = json.load(template_file)
        template['Auth']['Cognito']['userPoolClientId'] = get_cognito_user_pool_web_client_id(environment)
        template['Auth']['Cognito']['userPoolId'] = get_cognito_user_pool_id(environment)
        template['API']['REST']['ToadInTheHoleAPI']['region'] = region
        template['API']['REST']['ToadInTheHoleAPI']['endpoint'] = 'https://' + Domain.API.get_domain_name(environment, domain_name) + '/prod'
        with open('frontend/src/amplifyconfiguration.json', 'w') as output_file:
            json.dump(fp=output_file, obj=template)

if __name__ == '__main__':
    environment = sys.argv[1]
    create_amplify_config(environment)
