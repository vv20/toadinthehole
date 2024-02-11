import json
import os
import sys

from get_cognito_user_pool_id import get_cognito_user_pool_id
from get_cognito_user_pool_web_client_id import \
    get_cognito_user_pool_web_client_id


def create_amplify_config(environment):
    with open('frontend/src/amplifyconfiguration.json.template', 'r') as template_file:
        template = json.load(template_file)
        template['aws_project_region'] = os.getenv('AWS_REGION')
        template['aws_cognito_region'] = os.getenv('AWS_REGION')
        template['aws_user_pools_id'] = get_cognito_user_pool_id(environment)
        template['aws_user_pools_web_client_id'] = get_cognito_user_pool_web_client_id(environment)
        with open('frontend/src/amplifyconfiguration.json', 'w') as output_file:
            json.dump(fp=output_file, obj=template)

if __name__ == '__main__':
    environment = sys.argv[1]
    create_amplify_config(environment)
