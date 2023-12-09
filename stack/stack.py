import subprocess

from aws_cdk import (
    aws_certificatemanager as acm,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    Duration,
    Stack
)
from constructs import Construct

class ToadInTheHoleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain_name = self.node.try_get_context('domain_name')
        frontend_bucket, image_bucket = self.create_s3_buckets(construct_id)
        recipe_table = self.create_dynamodb_table(construct_id)
        api_role, lambda_role = self.setup_iam(
                construct_id,
                frontend_bucket,
                image_bucket,
                recipe_table)
        user_pool = self.setup_cognito(construct_id)
        recipe_handler, collection_handler, image_handler = self.create_lambda_handlers(
                construct_id,
                lambda_role,
                recipe_table)
        zone = self.configure_dns(
                construct_id,
                domain_name,
                frontend_bucket)
        api_certificate = self.create_certificates(construct_id, domain_name, zone)
        api = self.create_api_gateway(
                construct_id,
                domain_name,
                api_role,
                user_pool,
                recipe_handler,
                collection_handler,
                image_handler,
                image_bucket,
                api_certificate)
        self.create_frontend_deployment(construct_id, frontend_bucket)

    def create_s3_buckets(self, environment):
        frontend_bucket = s3.Bucket(
                self,
                'toad-in-the-hole-frontend-' + environment,
                website_index_document='index.html')

        image_bucket = s3.Bucket(self, 'toad-in-the-hole-images-' + environment)

        return frontend_bucket, image_bucket

    def create_dynamodb_table(self, environment):
        recipe_table = dynamodb.TableV2(
                self,
                'toad-in-the-hole-recipes-' + environment,
                table_name='toad-in-the-hole-recipes-' + environment,
                partition_key=dynamodb.Attribute(name='slug', type=dynamodb.AttributeType.STRING),
                billing=dynamodb.Billing.on_demand())
        return recipe_table

    def setup_iam(
            self,
            environment,
            frontend_bucket,
            image_bucket,
            recipe_table):
        lambda_role = iam.Role(
                self,
                'lambda-role-' + environment,
                assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'))

        api_role = iam.Role(
                self,
                'api-role-' + environment,
                assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com'))

        frontend_bucket_read_only_policy = iam.Policy(
                self,
                'frontend-bucket-read-only-policy-' + environment,
                statements=[
                    iam.PolicyStatement(
                        actions=['s3-bucket:GetObject'],
                        resources=[frontend_bucket.bucket_arn]
                    )])
        frontend_bucket_read_only_policy.attach_to_role(api_role)

        image_bucket_read_only_policy = iam.Policy(
                self,
                'image-bucket-read-only-policy-' + environment,
                statements=[
                    iam.PolicyStatement(
                        actions=['s3-bucket:GetObject'],
                        resources=[image_bucket.bucket_arn]
                    )])
        image_bucket_read_only_policy.attach_to_role(api_role)

        image_bucket_write_only_policy = iam.Policy(
                self,
                'image-bucket-write-only-policy-' + environment,
                statements=[
                    iam.PolicyStatement(
                        actions=['s3-bucket:PutObject'],
                        resources=[image_bucket.bucket_arn]
                    )])
        image_bucket_write_only_policy.attach_to_role(lambda_role)

        recipe_table_read_write_policy = iam.Policy(
                self,
                'recipe-table-read-write-policy-' + environment,
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            'dynamodb-table:BatchGetItem',
                            'dynamodb-table:DeleteItem',
                            'dynamodb-table:GetItem',
                            'dynamodb-table:PutItem',
                            'dynamodb-table:Query',
                            'dynamodb-table:Scan',
                            'dynamodb-table:UpdateItem'],
                        resources=[recipe_table.table_arn]
                    )])
        recipe_table_read_write_policy.attach_to_role(lambda_role)
        return api_role, lambda_role

    def setup_cognito(self, environment):
        user_pool = cognito.UserPool(
                self,
                'toad-in-the-hole-user-pool-' + environment,
                user_pool_name='UserPool',
                self_sign_up_enabled=False,
                sign_in_case_sensitive=True,
                sign_in_aliases=cognito.SignInAliases(email=True),
                auto_verify=cognito.AutoVerifiedAttrs(email=True),
                user_verification=cognito.UserVerificationConfig(
                    email_subject='Welcome!',
                    email_body='Welcome to Toad in the Hole! The verification code is {####}.',
                    email_style=cognito.VerificationEmailStyle.CODE),
                standard_attributes=cognito.StandardAttributes(
                    fullname=cognito.StandardAttribute(
                        required=True,
                        mutable=True),
                    email=cognito.StandardAttribute(
                        required=True,
                        mutable=True)),
                password_policy=cognito.PasswordPolicy(
                    min_length=8,
                    require_lowercase=True,
                    require_digits=True,
                    require_symbols=True),
                account_recovery=cognito.AccountRecovery.EMAIL_ONLY)

        cognito_client = user_pool.add_client(
                'toad-in-the-hole-user-pool-client-' + environment,
                user_pool_client_name='toad-in-the-hole-user-pool-client-' + environment,
                o_auth=cognito.OAuthSettings(
                    flows=cognito.OAuthFlows(authorization_code_grant=True),
                    scopes=[cognito.OAuthScope.OPENID]),
                supported_identity_providers=[
                    cognito.UserPoolClientIdentityProvider.COGNITO],
                refresh_token_validity=Duration.hours(1),
                id_token_validity=Duration.minutes(30),
                access_token_validity=Duration.minutes(30))

        return user_pool

    def create_lambda_handlers(self, environment, lambda_role, recipe_table):
        lambda_kwargs = {
                'code'       : lambda_.Code.from_asset('backend'),
                'role'       : lambda_role,
                'runtime'    : lambda_.Runtime.PYTHON_3_9,
                'environment': {
                    'RECIPE_TABLE_NAME': recipe_table.table_name
                }
        }

        recipe_handler = lambda_.Function(
                self,
                'recipe-handler-' + environment,
                handler='recipe.handler',
                **lambda_kwargs)

        collection_handler = lambda_.Function(
                self,
                'recipe-collection-handler-' + environment,
                handler='recipe_collection.handler',
                **lambda_kwargs)

        image_handler = lambda_.Function(
                self,
                'image-handler-' + environment,
                handler='image.handler',
                **lambda_kwargs)

        return recipe_handler, collection_handler, image_handler

    def create_api_gateway(
            self,
            environment,
            domain_name,
            api_role,
            user_pool,
            recipe_handler,
            collection_handler,
            image_handler,
            image_bucket,
            certificate):
        authorizer = apigateway.CognitoUserPoolsAuthorizer(
                self,
                'cognito-user-pool-authorizer-' + environment,
                cognito_user_pools=[user_pool])

        api = apigateway.RestApi(
                self,
                'toad-in-the-hole-api-' + environment,
                rest_api_name='Toad in the Hole API',
                deploy=True)

        domain_name = apigateway.DomainName(
                self,
                'toad-in-the-hole-api-domain-name-' + environment,
                mapping=api,
                certificate=certificate,
                domain_name='api.' + environment + '.' + domain_name)

        recipe_resource     = api.root.add_resource('recipe')
        collection_resource = api.root.add_resource('collection')
        image_resource      = api.root.add_resource('image')

        recipe_resource.add_method(
                'GET',
                authorizer=authorizer,
                integration=apigateway.LambdaIntegration(
                    recipe_handler,
                    credentials_role=api_role))

        recipe_resource.add_method(
                'POST',
                authorizer=authorizer,
                integration=apigateway.LambdaIntegration(
                    recipe_handler,
                    credentials_role=api_role))

        recipe_resource.add_method(
                'DELETE',
                authorizer=authorizer,
                integration=apigateway.LambdaIntegration(
                    recipe_handler,
                    credentials_role=api_role))

        collection_resource.add_method(
                'GET',
                authorizer=authorizer,
                integration=apigateway.LambdaIntegration(
                    collection_handler,
                    credentials_role=api_role))

        image_resource.add_method(
                'GET',
                authorizer=authorizer,
                integration=apigateway.AwsIntegration(
                    service='s3',
                    path=image_bucket.bucket_website_url + '/{imageId}',
                    integration_http_method='GET',
                    options=apigateway.IntegrationOptions(
                        credentials_role=api_role)))

        image_resource.add_method(
                'PUT',
                authorizer=authorizer,
                integration=apigateway.LambdaIntegration(
                    image_handler,
                    credentials_role=api_role))

        return api

    def create_certificates(self, environment, domain_name, zone):
        env_certificate = acm.Certificate(
                self,
                environment + '-certificate',
                domain_name=environment + '.' + domain_name,
                validation=acm.CertificateValidation.from_dns(zone))
        frontend_certificate = acm.Certificate(
                self,
                environment + '-frontend-certificate',
                domain_name='www.' + environment + '.' + domain_name,
                validation=acm.CertificateValidation.from_dns(zone))
        api_certificate = acm.Certificate(
                self,
                environment + '-api-certificate',
                domain_name='api.' + environment + '.' + domain_name,
                validation=acm.CertificateValidation.from_dns(zone))
        return api_certificate

    def configure_dns(
            self,
            environment,
            domain_name,
            frontend_bucket):
        zone = route53.HostedZone.from_lookup(
                self,
                'zone',
                domain_name=domain_name)
        record = route53.ARecord(
                self,
                environment + '-frontend-record',
                zone=zone,
                target=route53.RecordTarget.from_alias(
                    route53_targets.BucketWebsiteTarget(frontend_bucket)),
                record_name='www.' + environment)
        return zone

    def create_frontend_deployment(self, environment, frontend_bucket):
        build_process = subprocess.run(
                'npm run build:' + environment,
                cwd='frontend',
                shell=True)
        build_process.check_returncode()

        frontend_deployment = s3_deployment.BucketDeployment(
                self,
                'frontend-deployment-' + environment,
                sources=[s3_deployment.Source.asset('frontend/build')],
                destination_bucket=frontend_bucket,
                retain_on_delete=False)
