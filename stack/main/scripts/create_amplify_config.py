import json
import sys

from ..common import Domain
from .get_cognito_user_pool_id import get_cognito_user_pool_id
from .get_cognito_user_pool_web_client_id import \
    get_cognito_user_pool_web_client_id
from .get_identity_pool_id import get_identity_pool_id
from .get_image_bucket_name import get_image_bucket_name


def create_amplify_config(environment, region, domain_name):
    with open('frontend/src/amplifyconfiguration.json.template', 'r') as template_file:
        template = json.load(template_file)
        idp_id = get_identity_pool_id(environment)
        template['Auth']['Cognito']['userPoolClientId'] = get_cognito_user_pool_web_client_id(environment)
        template['Auth']['Cognito']['userPoolId'] = get_cognito_user_pool_id(environment)
        template['Auth']['Cognito']['identityPoolId'] = idp_id
        template['API']['REST']['ToadInTheHoleAPI']['region'] = region
        template['API']['REST']['ToadInTheHoleAPI']['endpoint'] = 'https://' + Domain.API.get_domain_name(environment, domain_name)
        template['Storage']['S3']['bucket'] = get_image_bucket_name(environment)
        template['Storage']['S3']['region'] = region
        template['Storage']['S3']['identityPoolId'] = idp_id
        with open('frontend/src/amplifyconfiguration.json', 'w') as output_file:
            print(json.dumps(template))
            json.dump(fp=output_file, obj=template)

if __name__ == '__main__':
    environment = sys.argv[1]
    region = sys.argv[2]
    domain_name = sys.argv[3]
    create_amplify_config(environment, region, domain_name)
