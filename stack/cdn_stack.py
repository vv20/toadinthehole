from os.path import exists
from urllib.parse import urlparse

from aws_cdk import Fn, Stack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as cloudfront_origins
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from constructs import Construct

from stack.common import Component


class ToadInTheHoleCDNStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain_name = self.node.try_get_context('domain_name')
        environment = self.node.try_get_context('environment')
        frontend_bucket, image_bucket = self.lookup_s3_buckets(environment)
        zone = self.lookup_zone(domain_name)
        frontend_certificate = self.create_certificate(environment, domain_name, zone)
        distribution = self.create_cdn_distribution(
                environment,
                domain_name,
                frontend_bucket,
                image_bucket,
                frontend_certificate)
        self.configure_dns(environment, domain_name, zone, distribution)
        self.create_frontend_deployment(environment, frontend_bucket)

    def lookup_s3_buckets(self, environment):
        frontend_bucket_arn = Fn.import_value(Component.FRONTEND_BUCKET_EXPORT.get_component_name(environment))
        image_bucket_arn = Fn.import_value(Component.IMAGE_BUCKET_EXPORT.get_component_name(environment))

        frontend_bucket = s3.Bucket.from_bucket_arn(
                self,
                Component.FRONTEND_BUCKET.get_component_name(environment),
                frontend_bucket_arn)
        image_bucket = s3.Bucket.from_bucket_arn(
                self,
                Component.IMAGE_BUCKET.get_component_name(environment),
                image_bucket_arn)

        return frontend_bucket, image_bucket

    def lookup_zone(self, domain_name):
        return route53.HostedZone.from_lookup(
                self,
                'zone',
                domain_name=domain_name)

    def create_certificate(self, environment, domain_name, zone):
        frontend_certificate = acm.Certificate(
                self,
                Component.FRONTEND_CERTIFICATE.get_component_name(environment),
                domain_name='www.' + environment + '.' + domain_name,
                validation=acm.CertificateValidation.from_dns(zone))
        return frontend_certificate

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
                            origin_access_identity=oai)),
                    '/api/*': cloudfront.BehaviorOptions(
                        origin=cloudfront_origins.HttpOrigin('api.' + environment + '.' + domain_name))
                },
                certificate=frontend_certificate,
                domain_names=['www.' + environment + '.' + domain_name])

        return distribution

    def configure_dns(self, environment, domain_name, zone, distribution):
        route53.ARecord(
                self,
                Component.ALIAS_RECORD.get_component_name(environment),
                zone=zone,
                record_name='www.' + environment + '.' + domain_name,
                target=route53.RecordTarget.from_alias(
                    route53_targets.CloudFrontTarget(distribution)))

    def create_frontend_deployment(self, environment, frontend_bucket):
        if not exists('frontend/build'):
            return
        s3_deployment.BucketDeployment(
                self,
                Component.FRONTEND_DEPLOYMENT.get_component_name(environment),
                sources=[s3_deployment.Source.asset('frontend/build')],
                destination_bucket=frontend_bucket,
                retain_on_delete=False)
