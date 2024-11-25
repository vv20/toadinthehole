from aws_cdk import BundlingOptions, Duration, Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as cloudfront_origins
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_cognito_identitypool_alpha as cognito_identitypool
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_logs as logs
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from aws_cdk import aws_s3 as s3
from constructs import Construct

from ..common import (Component, Domain, LocalBundler,
                          get_environment_domain)


class ToadInTheHoleMainStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            frontend_certificate_arn: str,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.frontend_certificate_arn: str = frontend_certificate_arn
        self.domain_name: str = self.node.try_get_context('domain_name')
        self.stack_environment: str = self.node.try_get_context('environment')
        self.host_at_apex: bool = bool(self.node.try_get_context('host_at_apex'))

        self.create_s3_buckets()
        self.create_dynamodb_table()
        self.setup_iam()
        self.setup_cognito()
        self.create_lambda_handlers()
        self.lookup_zone()
        self.create_certificate()
        self.lookup_frontend_certificate()
        self.create_api_gateway()
        self.create_cdn_distribution()
        self.configure_dns()
        self.create_exports()

    def create_s3_buckets(self) -> None:
        self.frontend_bucket: s3.Bucket = s3.Bucket(
                self,
                Component.FRONTEND_BUCKET.get_component_name(self.stack_environment),
                website_index_document='index.html',
                public_read_access=True,
                block_public_access=s3.BlockPublicAccess(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False))

        self.image_bucket: s3.Bucket = s3.Bucket(
                self,
                Component.IMAGE_BUCKET.get_component_name(self.stack_environment),
                public_read_access=True,
                block_public_access=s3.BlockPublicAccess(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False),
                cors=[s3.CorsRule(
                    allowed_origins=["*"],
                    allowed_methods=[s3.HttpMethods.PUT],
                    allowed_headers=["*"])])

    def create_dynamodb_table(self) -> None:
        self.recipe_table: dynamodb.TableV2 = dynamodb.TableV2(
                self,
                Component.RECIPE_TABLE.get_component_name(self.stack_environment),
                table_name=Component.RECIPE_TABLE.get_component_name(self.stack_environment),
                partition_key=dynamodb.Attribute(name='recipe_slug', type=dynamodb.AttributeType.STRING),
                billing=dynamodb.Billing.on_demand())

    def setup_iam(self) -> None:
        self.lambda_role: iam.Role = iam.Role(
                self,
                Component.LAMBDA_ROLE.get_component_name(self.stack_environment),
                assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'))

        self.api_role: iam.Role = iam.Role(
                self,
                Component.API_ROLE.get_component_name(self.stack_environment),
                assumed_by=iam.ServicePrincipal('apigateway.amazonaws.com'))

        self.user_role: iam.Role = iam.Role(
                self,
                Component.USER_ROLE.get_component_name(self.stack_environment),
                assumed_by=iam.FederatedPrincipal(
                    'cognito-identity.amazonaws.com',
                    assume_role_action='sts:AssumeRoleWithWebIdentity',
                    conditions={
                        'StringEquals': {
                            'cognito-identity.amazonaws.com:aud': 'eu-west-2:86954a34-383d-4969-902f-8cab127d2f6d'
                        },
                        'ForAnyValue:StringLike': {
                            'cognito-identity.amazonaws.com:amr': 'authenticated'
                        }
                    }))

        self.image_bucket_write_only_policy: iam.Policy = iam.Policy(
                self,
                Component.IMAGE_BUCKET_WRITE_ONLY_POLICY.get_component_name(self.stack_environment),
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            's3-bucket:PutObject',
                        ],
                        resources=[self.image_bucket.bucket_arn]
                    )])
        self.image_bucket_write_only_policy.attach_to_role(self.user_role)

        self.recipe_table_read_write_policy: iam.Policy = iam.Policy(
                self,
                Component.RECIPE_TABLE_READ_WRITE_POLICY.get_component_name(self.stack_environment),
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
                        resources=[self.recipe_table.table_arn])])
        self.recipe_table_read_write_policy.attach_to_role(self.lambda_role)

    def setup_cognito(self) -> None:
        self.user_pool: cognito.UserPool = cognito.UserPool(
                self,
                Component.USER_POOL.get_component_name(self.stack_environment),
                user_pool_name=Component.USER_POOL.get_component_name(self.stack_environment),
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
        
        self.user_pool_client: cognito.UserPoolClient = self.user_pool.add_client(
                Component.USER_POOL_CLIENT.get_component_name(self.stack_environment),
                user_pool_client_name=Component.USER_POOL_CLIENT.get_component_name(self.stack_environment),
                o_auth=cognito.OAuthSettings(
                    flows=cognito.OAuthFlows(authorization_code_grant=True),
                    scopes=[cognito.OAuthScope.OPENID]),
                supported_identity_providers=[
                    cognito.UserPoolClientIdentityProvider.COGNITO],
                refresh_token_validity=Duration.hours(1),
                id_token_validity=Duration.minutes(30),
                access_token_validity=Duration.minutes(30))

        self.identity_pool: cognito_identitypool.IdentityPool = cognito_identitypool.IdentityPool(
            self,
            Component.IDENTITY_POOL.get_component_name(self.stack_environment),
            identity_pool_name=Component.IDENTITY_POOL.get_component_name(self.stack_environment),
            authentication_providers=cognito_identitypool.IdentityPoolAuthenticationProviders(
                user_pools=[cognito_identitypool.UserPoolAuthenticationProvider(
                    user_pool=self.user_pool,
                    user_pool_client=self.user_pool_client)]),
            authenticated_role=self.user_role)

    def create_lambda_handlers(self) -> None:
        lambda_kwargs: dict[str, any] = {
                'code'       : lambda_.Code.from_asset(
                    'backend/main',
                    bundling=BundlingOptions(
                        image=lambda_.Runtime.PYTHON_3_9.bundling_image,
                        command=[],
                        local=LocalBundler())),
                'role'       : self.lambda_role,
                'runtime'    : lambda_.Runtime.PYTHON_3_9,
                'environment': {
                    'RECIPE_TABLE_NAME': self.recipe_table.table_name,
                    'IMAGE_BUCKET_NAME': self.image_bucket.bucket_name,
                }
        }

        self.recipe_handler: lambda_.Function = lambda_.Function(
                self,
                Component.RECIPE_HANDLER.get_component_name(self.stack_environment),
                handler='main.recipe.handler',
                **lambda_kwargs)

        self.collection_handler: lambda_.Function = lambda_.Function(
                self,
                Component.COLLECTION_HANDLER.get_component_name(self.stack_environment),
                handler='main.recipe_collection.handler',
                **lambda_kwargs)

        self.image_handler: lambda_.Function = lambda_.Function(
                self,
                Component.IMAGE_HANDLER.get_component_name(self.stack_environment),
                handler='main.image.handler',
                **lambda_kwargs)

        self.lambda_invocation_policy: iam.Policy = iam.Policy(
                self,
                Component.LAMBDA_EXECUTION_POLICY.get_component_name(self.stack_environment),
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            'lambda:InvokeFunction'],
                        resources=[
                            self.recipe_handler.function_arn,
                            self.collection_handler.function_arn,
                            self.image_handler.function_arn])])
        self.lambda_invocation_policy.attach_to_role(self.api_role)

    def create_api_gateway(self) -> None:
        self.authorizer: apigateway.CognitoUserPoolsAuthorizer = apigateway.CognitoUserPoolsAuthorizer(
                self,
                Component.USER_POOL_AUTHORIZER.get_component_name(self.stack_environment),
                cognito_user_pools=[self.user_pool])

        self.log_group: logs.LogGroup = logs.LogGroup(
                self,
                Component.LOG_GROUP.get_component_name(self.stack_environment),
                log_group_name=Component.LOG_GROUP.get_component_name(self.stack_environment),
                retention=logs.RetentionDays.ONE_MONTH)

        self.api: apigateway.RestApi = apigateway.RestApi(
                self,
                Component.API.get_component_name(self.stack_environment),
                rest_api_name=Component.API.get_component_name(self.stack_environment),
                cloud_watch_role=True,
                domain_name=apigateway.DomainNameOptions(
                    certificate=self.certificate,
                    domain_name=Domain.API.get_domain_name(self.stack_environment, self.domain_name)),
                default_cors_preflight_options=apigateway.CorsOptions(
                    allow_origins=['*'],
                    allow_credentials=True,
                    allow_headers=apigateway.Cors.DEFAULT_HEADERS,
                    allow_methods=apigateway.Cors.ALL_METHODS),
                deploy_options=apigateway.StageOptions(
                    data_trace_enabled=True,
                    logging_level=apigateway.MethodLoggingLevel.INFO,
                    access_log_destination=apigateway.LogGroupLogDestination(self.log_group)),
                deploy=True)

        recipe_resource: apigateway.Resource = self.api.root.add_resource('recipe')
        collection_resource: apigateway.Resource = self.api.root.add_resource('collection')
        image_resource: apigateway.Resource = self.api.root.add_resource('image')

        recipe_resource.add_method(
                'GET',
                authorizer=self.authorizer,
                integration=apigateway.LambdaIntegration(
                    self.recipe_handler,
                    credentials_role=self.api_role))

        recipe_resource.add_method(
                'POST',
                authorizer=self.authorizer,
                integration=apigateway.LambdaIntegration(
                    self.recipe_handler,
                    credentials_role=self.api_role))

        recipe_resource.add_method(
                'DELETE',
                authorizer=self.authorizer,
                integration=apigateway.LambdaIntegration(
                    self.recipe_handler,
                    credentials_role=self.api_role))

        collection_resource.add_method(
                'GET',
                authorizer=self.authorizer,
                integration=apigateway.LambdaIntegration(
                    self.collection_handler,
                    credentials_role=self.api_role))

        image_resource.add_method(
                'GET',
                authorizer=self.authorizer,
                integration=apigateway.LambdaIntegration(
                    self.image_handler,
                    credentials_role=self.api_role))

    def lookup_zone(self) -> None:
        self.zone: route53.HostedZone = route53.HostedZone.from_lookup(
                self,
                'zone',
                domain_name=self.domain_name)

    def create_certificate(self) -> None:
        self.certificate: acm.Certificate = acm.Certificate(
                self,
                Component.ENVIRONMENT_CERTIFICATE.get_component_name(self.stack_environment),
                domain_name=get_environment_domain(self.stack_environment, self.domain_name),
                validation=acm.CertificateValidation.from_dns(self.zone))

        self.api_certificate: acm.Certificate = acm.Certificate(
                self,
                Component.API_CERTIFICATE.get_component_name(self.stack_environment),
                domain_name=Domain.API.get_domain_name(self.stack_environment, self.domain_name),
                validation=acm.CertificateValidation.from_dns(self.zone))

    def lookup_frontend_certificate(self) -> None:
        self.frontend_certificate: acm.Certificate = acm.Certificate.from_certificate_arn(
                self,
                Component.FRONTEND_CERTIFICATE.get_component_name(self.stack_environment),
                self.frontend_certificate_arn)

    def create_cdn_distribution(self) -> None:
        self.oai: cloudfront.OriginAccessIdentity = cloudfront.OriginAccessIdentity(
                self,
                Component.ORIGIN_ACCESS_IDENTITY.get_component_name(self.stack_environment))
        self.frontend_bucket.grant_read(self.oai)
        self.image_bucket.grant_read(self.oai)

        domain_names: list[str] = [
                Domain.FRONTEND.get_domain_name(self.stack_environment, self.domain_name)]
        if self.host_at_apex:
            domain_names.append(self.domain_name)

        self.distribution: cloudfront.Distribution = cloudfront.Distribution(
                self,
                Component.DISTRIBUTION.get_component_name(self.stack_environment),
                default_root_object='index.html',
                default_behavior=cloudfront.BehaviorOptions(
                    origin=cloudfront_origins.S3BucketOrigin.with_origin_access_identity(
                        bucket=self.frontend_bucket,
                        origin_access_identity=self.oai)),
                additional_behaviors={
                    '/image/*': cloudfront.BehaviorOptions(
                        origin=cloudfront_origins.S3BucketOrigin.with_origin_access_identity(
                            self.image_bucket,
                            origin_access_identity=self.oai))
                },
                certificate=self.frontend_certificate,
                domain_names=domain_names)

    def configure_dns(self) -> None:
        self.frontend_record: route53.ARecord = route53.ARecord(
                self,
                Component.FRONTEND_ALIAS_RECORD.get_component_name(self.stack_environment),
                zone=self.zone,
                record_name=Domain.FRONTEND.get_domain_name(self.stack_environment, self.domain_name),
                target=route53.RecordTarget.from_alias(
                    route53_targets.CloudFrontTarget(self.distribution)))
        self.api_record: route53.ARecord = route53.ARecord(
                self,
                Component.API_ALIAS_RECORD.get_component_name(self.stack_environment),
                zone=self.zone,
                record_name=Domain.API.get_domain_name(self.stack_environment, self.domain_name),
                target=route53.RecordTarget.from_alias(
                    route53_targets.ApiGateway(self.api)))
        if self.host_at_apex:
            self.apex_record: route53.ARecord = route53.ARecord(
                    self,
                    Component.APEX_ALIAS_RECORD.get_component_name(self.stack_environment),
                    zone=self.zone,
                    record_name=self.domain_name,
                    target=route53.RecordTarget.from_alias(
                        route53_targets.Route53RecordTarget(self.frontend_record)))

    def create_exports(self) -> None:
        self.frontend_bucket_arn: str = self.frontend_bucket.bucket_arn