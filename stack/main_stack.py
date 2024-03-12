from aws_cdk import BundlingOptions, CfnOutput, Duration, Fn, Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as cloudfront_origins
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from aws_cdk import aws_s3 as s3
from constructs import Construct

from stack.common import (Component, Domain, LocalBundler,
                          get_environment_domain)


class ToadInTheHoleMainStack(Stack):

    def __init__(
            self,
            scope,
            construct_id,
            frontend_certificate_arn,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain_name = self.node.try_get_context('domain_name')
        environment = self.node.try_get_context('environment')
        localhost_access = bool(self.node.try_get_context('localhost_access'))
        frontend_bucket, image_bucket = self.create_s3_buckets(environment)
        recipe_table = self.create_dynamodb_table(environment)
        api_role, lambda_role = self.setup_iam(
                environment,
                image_bucket,
                recipe_table)
        user_pool = self.setup_cognito(environment)
        recipe_handler, collection_handler, image_handler = self.create_lambda_handlers(
                environment,
                api_role,
                lambda_role,
                recipe_table,
                image_bucket)
        zone = self.lookup_zone(domain_name)
        api_certificate = self.create_certificate(environment, domain_name, zone)
        frontend_certificate = self.lookup_frontend_certificate(environment, frontend_certificate_arn)
        api = self.create_api_gateway(
                environment,
                domain_name,
                api_role,
                user_pool,
                recipe_handler,
                collection_handler,
                image_handler,
                image_bucket,
                api_certificate,
                localhost_access)
        distribution = self.create_cdn_distribution(
                environment,
                domain_name,
                frontend_bucket,
                image_bucket,
                frontend_certificate)
        self.configure_dns(environment, domain_name, zone, distribution, api)
        self.create_exports(environment, frontend_bucket)

    def create_s3_buckets(self, environment):
        frontend_bucket = s3.Bucket(
                self,
                Component.FRONTEND_BUCKET.get_component_name(environment),
                website_index_document='index.html',
                public_read_access=True,
                block_public_access=s3.BlockPublicAccess(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False))

        image_bucket = s3.Bucket(
                self,
                Component.IMAGE_BUCKET.get_component_name(environment),
                public_read_access=True,
                block_public_access=s3.BlockPublicAccess(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False))
        return frontend_bucket, image_bucket

    def create_dynamodb_table(self, environment):
        recipe_table = dynamodb.TableV2(
                self,
                Component.RECIPE_TABLE.get_component_name(environment),
                table_name=Component.RECIPE_TABLE.get_component_name(environment),
                partition_key=dynamodb.Attribute(name='slug', type=dynamodb.AttributeType.STRING),
                billing=dynamodb.Billing.on_demand())
        return recipe_table

    def setup_iam(
            self,
            environment,
            image_bucket,
            recipe_table):
        lambda_role = iam.Role(
                self,
                Component.LAMBDA_ROLE.get_component_name(environment),
                assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'))

        api_role = iam.Role(
                self,
                Component.API_ROLE.get_component_name(environment),
                assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com'))

        image_bucket_write_only_policy = iam.Policy(
                self,
                Component.IMAGE_BUCKET_WRITE_ONLY_POLICY.get_component_name(environment),
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            's3-bucket:PutObject',
                            's3-bucket:GetObject',
                            's3-bucket:PutObjectAcl'
                        ],
                        resources=[image_bucket.bucket_arn]
                    )])
        image_bucket_write_only_policy.attach_to_role(lambda_role)

        recipe_table_read_write_policy = iam.Policy(
                self,
                Component.RECIPE_TABLE_READ_WRITE_POLICY.get_component_name(environment),
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            'dynamodb:BatchGetItem',
                            'dynamodb:DeleteItem',
                            'dynamodb:GetItem',
                            'dynamodb:PutItem',
                            'dynamodb:Query',
                            'dynamodb:Scan',
                            'dynamodb:UpdateItem'],
                        resources=[recipe_table.table_arn])])
        recipe_table_read_write_policy.attach_to_role(lambda_role)

        return api_role, lambda_role

    def setup_cognito(self, environment):
        user_pool = cognito.UserPool(
                self,
                Component.USER_POOL.get_component_name(environment),
                user_pool_name=Component.USER_POOL.get_component_name(environment),
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

        user_pool.add_client(
                Component.USER_POOL_CLIENT.get_component_name(environment),
                user_pool_client_name=Component.USER_POOL_CLIENT.get_component_name(environment),
                o_auth=cognito.OAuthSettings(
                    flows=cognito.OAuthFlows(authorization_code_grant=True),
                    scopes=[cognito.OAuthScope.OPENID]),
                supported_identity_providers=[
                    cognito.UserPoolClientIdentityProvider.COGNITO],
                refresh_token_validity=Duration.hours(1),
                id_token_validity=Duration.minutes(30),
                access_token_validity=Duration.minutes(30))

        return user_pool

    def create_lambda_handlers(
            self,
            environment,
            api_role,
            lambda_role,
            recipe_table,
            image_bucket):
        lambda_kwargs = {
                'code'       : lambda_.Code.from_asset(
                    'backend',
                    bundling=BundlingOptions(
                        image=lambda_.Runtime.PYTHON_3_9.bundling_image,
                        command=[],
                        local=LocalBundler())),
                'role'       : lambda_role,
                'runtime'    : lambda_.Runtime.PYTHON_3_9,
                'environment': {
                    'RECIPE_TABLE_NAME': recipe_table.table_name,
                    'IMAGE_BUCKET_ARN': image_bucket.bucket_arn
                }
        }

        recipe_handler = lambda_.Function(
                self,
                Component.RECIPE_HANDLER.get_component_name(environment),
                handler='recipe.handler',
                **lambda_kwargs)

        collection_handler = lambda_.Function(
                self,
                Component.COLLECTION_HANDLER.get_component_name(environment),
                handler='recipe_collection.handler',
                **lambda_kwargs)

        image_handler = lambda_.Function(
                self,
                Component.IMAGE_HANDLER.get_component_name(environment),
                handler='image.handler',
                **lambda_kwargs)

        lambda_invocation_policy = iam.Policy(
                self,
                Component.LAMBDA_EXECUTION_POLICY.get_component_name(environment),
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            'lambda:InvokeFunction'],
                        resources=[
                            recipe_handler.function_arn,
                            collection_handler.function_arn,
                            image_handler.function_arn])])
        lambda_invocation_policy.attach_to_role(api_role)

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
            certificate,
            localhost_access):
        authorizer = apigateway.CognitoUserPoolsAuthorizer(
                self,
                Component.USER_POOL_AUTHORIZER.get_component_name(environment),
                cognito_user_pools=[user_pool])

        cors_origins = ['https://' + Domain.FRONTEND.get_domain_name(environment, domain_name) + ':8080']
        if (localhost_access):
            cors_origins.append('https://localhost:3000')

        api = apigateway.RestApi(
                self,
                Component.API.get_component_name(environment),
                rest_api_name=Component.API.get_component_name(environment),
                domain_name=apigateway.DomainNameOptions(
                    certificate=certificate,
                    domain_name=Domain.API.get_domain_name(environment, domain_name)),
                default_cors_preflight_options=apigateway.CorsOptions(
                    allow_origins=cors_origins,
                    allow_credentials=True),
                deploy=True)

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
                integration=apigateway.LambdaIntegration(
                    image_handler,
                    credentials_role=api_role))

        return api

    def lookup_zone(self, domain_name):
        return route53.HostedZone.from_lookup(
                self,
                'zone',
                domain_name=domain_name)

    def create_certificate(self, environment, domain_name, zone):
        acm.Certificate(
                self,
                Component.ENVIRONMENT_CERTIFICATE.get_component_name(environment),
                domain_name=get_environment_domain(environment, domain_name),
                validation=acm.CertificateValidation.from_dns(zone))

        api_certificate = acm.Certificate(
                self,
                Component.API_CERTIFICATE.get_component_name(environment),
                domain_name=Domain.API.get_domain_name(environment, domain_name),
                validation=acm.CertificateValidation.from_dns(zone))

        return api_certificate

    def lookup_frontend_certificate(
            self,
            environment,
            frontend_certificate_arn):
        return acm.Certificate.from_certificate_arn(
                self,
                Component.FRONTEND_CERTIFICATE.get_component_name(environment),
                frontend_certificate_arn)

    def create_cdn_distribution(
            self,
            environment,
            domain_name,
            frontend_bucket,
            image_bucket,
            frontend_certificate):
        oai = cloudfront.OriginAccessIdentity(
                self,
                Component.ORIGIN_ACCESS_IDENTITY.get_component_name(environment))
        frontend_bucket.grant_read(oai)
        image_bucket.grant_read(oai)

        distribution = cloudfront.Distribution(
                self,
                Component.DISTRIBUTION.get_component_name(environment),
                default_root_object='index.html',
                default_behavior=cloudfront.BehaviorOptions(
                    origin=cloudfront_origins.S3Origin(
                        frontend_bucket,
                        origin_access_identity=oai)),
                additional_behaviors={
                    '/image/*': cloudfront.BehaviorOptions(
                        origin=cloudfront_origins.S3Origin(
                            image_bucket,
                            origin_access_identity=oai))
                },
                certificate=frontend_certificate,
                domain_names=[Domain.FRONTEND.get_domain_name(environment, domain_name)])

        return distribution

    def configure_dns(self, environment, domain_name, zone, distribution, api):
        route53.ARecord(
                self,
                Component.FRONTEND_ALIAS_RECORD.get_component_name(environment),
                zone=zone,
                record_name=Domain.FRONTEND.get_domain_name(environment, domain_name),
                target=route53.RecordTarget.from_alias(
                    route53_targets.CloudFrontTarget(distribution)))
        route53.ARecord(
                self,
                Component.API_ALIAS_RECORD.get_component_name(environment),
                zone=zone,
                record_name=Domain.API.get_domain_name(environment, domain_name),
                target=route53.RecordTarget.from_alias(
                    route53_targets.ApiGateway(api)))

    def create_exports(self, environment, frontend_bucket):
        CfnOutput(
                self,
                Component.FRONTEND_BUCKET_EXPORT.get_component_name(environment),
                export_name=Component.FRONTEND_BUCKET_EXPORT.get_component_name(environment),
                value=frontend_bucket.bucket_arn)
