from aws_cdk import (
    aws_certificatemanager as acm,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    aws_route53 as route53,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    Stack
)
from constructs import Construct

class ToadInTheHoleFrontendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain_name = self.node.try_get_context('domain_name')
        frontend_bucket = self.create_s3_bucket(construct_id)
        frontend_certificate = self.create_certificate(construct_id, domain_name)
        self.create_cdn_distribution(
                construct_id,
                domain_name,
                frontend_bucket,
                frontend_certificate)
        self.create_frontend_deployment(construct_id, frontend_bucket)

    def create_s3_bucket(self, environment):
        frontend_bucket = s3.Bucket(
                self,
                'toad-in-the-hole-frontend-' + environment,
                website_index_document='index.html')
        return frontend_bucket

    def create_certificate(self, environment, domain_name):
        zone = route53.HostedZone.from_lookup(
                self,
                'zone',
                domain_name=domain_name)
        frontend_certificate = acm.Certificate(
                self,
                environment + '-frontend-certificate',
                domain_name='www.' + environment + '.' + domain_name,
                validation=acm.CertificateValidation.from_dns(zone))
        return frontend_certificate

    def create_cdn_distribution(
            self,
            environment,
            domain_name,
            frontend_bucket,
            frontend_certificate):
        oai = cloudfront.OriginAccessIdentity(
                self,
                environment + '-origin-access-identity')
        frontend_bucket.grant_read(oai)

        distribution = cloudfront.Distribution(
                self,
                environment + '-distribution',
                default_root_object='index.html',
                default_behavior=cloudfront.BehaviorOptions(
                    origin=cloudfront_origins.S3Origin(
                        frontend_bucket,
                        origin_access_identity=oai)),
                certificate=frontend_certificate,
                domain_names=['www.' + environment + '.' + domain_name])

    def create_frontend_deployment(self, environment, frontend_bucket):
        frontend_deployment = s3_deployment.BucketDeployment(
                self,
                'frontend-deployment-' + environment,
                sources=[s3_deployment.Source.asset('frontend/build')],
                destination_bucket=frontend_bucket,
                retain_on_delete=False)
