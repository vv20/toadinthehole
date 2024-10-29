from enum import Enum
from subprocess import CalledProcessError, check_call

from aws_cdk import ILocalBundling
from jsii import implements

APPLICATION_NAME = 'ToadInTheHole'
COMPONENT_DOMAIN_NAME_FORMAT = '{component}.{environment}.{top_level_domain}'
COMPONENT_NAME_FORMAT = '{application_name}{component_name}{environment}'
ENVIRONMENT_DOMAIN_NAME_FORMAT = '{environment}.{top_level_domain}'

@implements(ILocalBundling)
class LocalBundler:

    def try_bundle(self, output_dir, bundling_opts):
        try:
            check_call('pip install -r backend/requirements.txt -t {}'.format(output_dir), shell=True)
            check_call('cp -a backend/* {}'.format(output_dir), shell=True)
            return True
        except CalledProcessError as e:
            print('Command {} returned non-zero exit status {}.'.format(e.cmd, e.returncode))
            return False


class Component(Enum):
    APEX_ALIAS_RECORD              = 'apex_alias_record'
    API                            = 'api'
    API_ALIAS_RECORD               = 'api_alias_record'
    API_CERTIFICATE                = 'api_certificate'
    API_ROLE                       = 'api_role'
    COLLECTION_HANDLER             = 'collection_handler'
    DISTRIBUTION                   = 'distribution'
    FRONTEND_ALIAS_RECORD          = 'frontend_alias_record'
    FRONTEND_BUCKET                = 'frontend_bucket'
    FRONTEND_BUCKET_EXPORT         = 'frontend_bucket_export'
    FRONTEND_CERTIFICATE           = 'frontend_certificate'
    FRONTEND_DEPLOYMENT            = 'frontend_deployment'
    ENVIRONMENT_CERTIFICATE        = 'environment_certificate'
    IDENTITY_POOL                  = 'identity_pool'
    IMAGE_BUCKET                   = 'image_bucket'
    IMAGE_BUCKET_READ_ONLY_POLICY  = 'image_bucket_read_only_policy'
    IMAGE_BUCKET_WRITE_ONLY_POLICY = 'image_bucket_write_only_policy'
    IMAGE_HANDLER                  = 'image_handler'
    LAMBDA_ROLE                    = 'lambda_role'
    LAMBDA_EXECUTION_POLICY        = 'lambda_execution_policy'
    LOG_GROUP                      = 'log_group'
    ORIGIN_ACCESS_IDENTITY         = 'origin_access_identity'
    RECIPE_HANDLER                 = 'recipe_handler'
    RECIPE_TABLE                   = 'recipe_table'
    RECIPE_TABLE_READ_WRITE_POLICY = 'recipe_table_read_write_policy'
    USER_POOL                      = 'user_pool'
    USER_POOL_AUTHORIZER           = 'user_pool_authorizer'
    USER_POOL_CLIENT               = 'user_pool_client'
    USER_ROLE                      = 'user_role'

    def get_component_name(self, environment):
        return COMPONENT_NAME_FORMAT.format(
                application_name=APPLICATION_NAME,
                component_name=self.value.replace('-', '').replace('_', ''),
                environment=environment).lower()

class Domain(Enum):
    API      = 'api'
    FRONTEND = 'www'

    def get_domain_name(self, environment, top_level_domain):
        return COMPONENT_DOMAIN_NAME_FORMAT.format(
                component=self.value,
                environment=environment,
                top_level_domain=top_level_domain)

def get_environment_domain(environment, top_level_domain):
    return ENVIRONMENT_DOMAIN_NAME_FORMAT.format(
            environment=environment,
            top_level_domain=top_level_domain)
