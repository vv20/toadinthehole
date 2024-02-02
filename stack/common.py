from enum import Enum

APPLICATION_NAME = 'ToadInTheHole'
COMPONENT_NAME_FORMAT = '{application_name}{component_name}{environment}'

class Component(Enum):
    ALIAS_RECORD                   = 'alias_record'
    API                            = 'api'
    API_CERTIFICATE                = 'api_certificate'
    API_EXPORT                     = 'api_export'
    API_ROLE                       = 'api_role'
    COLLECTION_HANDLER             = 'collection_handler'
    DISTRIBUTION                   = 'distribution'
    DOMAIN_NAME                    = 'domain_name'
    FRONTEND_BUCKET                = 'frontend_bucket'
    FRONTEND_BUCKET_EXPORT         = 'frontend_bucket_export'
    FRONTEND_CERTIFICATE           = 'frontend_certificate'
    FRONTEND_DEPLOYMENT            = 'frontend_deployment'
    ENVIRONMENT_CERTIFICATE        = 'environment_certificate'
    IMAGE_BUCKET                   = 'image_bucket'
    IMAGE_BUCKET_EXPORT            = 'image_bucket_export'
    IMAGE_BUCKET_READ_ONLY_POLICY  = 'image_bucket_read_only_policy'
    IMAGE_BUCKET_WRITE_ONLY_POLICY = 'image_bucket_write_only_policy'
    IMAGE_HANDLER                  = 'image_handler'
    LAMBDA_ROLE                    = 'lambda_role'
    ORIGIN_ACCESS_IDENTITY         = 'origin_access_identity'
    RECIPE_HANDLER                 = 'recipe_handler'
    RECIPE_TABLE                   = 'recipe_table'
    RECIPE_TABLE_READ_WRITE_POLICY = 'recipe_table_read_write_policy'
    USER_POOL                      = 'user_pool'
    USER_POOL_AUTHORIZER           = 'user_pool_authorizer'
    USER_POOL_CLIENT               = 'user_pool_client'

    def get_component_name(self, environment):
        return COMPONENT_NAME_FORMAT.format(
                application_name=APPLICATION_NAME,
                component_name=self.value.replace('-', '').replace('_', ''),
                environment=environment).lower()
