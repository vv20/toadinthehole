from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    Stack
)
from constructs import Construct
from os.path import exists

class ToadInTheHoleFrontendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain_name = self.node.try_get_context('domain_name')
        frontend_bucket = self.create_s3_bucket(construct_id)
        zone = self.lookup_zone(domain_name)
        distribution = self.create_cdn_distribution(
                construct_id,
                domain_name,
                frontend_bucket)
        self.configure_dns(construct_id, domain_name, zone, distribution)
        self.create_frontend_deployment(construct_id, frontend_bucket)

    def create_s3_bucket(self, environment):
        frontend_bucket = s3.Bucket(
                self,
                'ToadInTheHoleFrontendBucket' + environment,
                website_index_document='index.html',
                public_read_access=True,
                block_public_access=s3.BlockPublicAccess(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False))
        return frontend_bucket

    def lookup_zone(self, domain_name):
        return route53.HostedZone.from_lookup(
                self,
                'zone',
                domain_name=domain_name)

    def create_cdn_distribution(
            self,
            environment,
            domain_name,
            frontend_bucket):
        oai = cloudfront.OriginAccessIdentity(
                self,
                'ToadInTheHoleOriginAccessIdentity' + environment)
        frontend_bucket.grant_read(oai)

        distribution = cloudfront.Distribution(
                self,
                'ToadInTheHoleCloudFrontDistribution' + environment,
                default_root_object='index.html',
                default_behavior=cloudfront.BehaviorOptions(
                    origin=cloudfront_origins.S3Origin(
                        frontend_bucket,
                        origin_access_identity=oai)),
                domain_names=['www.' + environment + '.' + domain_name])

        return distribution

    def configure_dns(self, environment, domain_name, zone, distribution):
        route53.ARecord(
                self,
                'ToadInTheHoleFrontendAliasRecord' + environment,
                zone=zone,
                record_name='www.' + environment + '.' + domain_name,
                target=route53.RecordTarget.from_alias(
                    route53_targets.CloudFrontTarget(distribution)))

    def create_frontend_deployment(self, environment, frontend_bucket):
        if not exists('frontend/build'):
            return
        s3_deployment.BucketDeployment(
                self,
                'ToadInTheHoleFrontendDeployment' + environment,
                sources=[s3_deployment.Source.asset('frontend/build')],
                destination_bucket=frontend_bucket,
                retain_on_delete=False)
