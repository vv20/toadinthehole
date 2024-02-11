from os.path import exists

from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment

from stack.common import Component


class ToadInTheHoleFrontendDeploymentStack(Stack):

    def __init__(
            self,
            scope,
            construct_id,
            frontend_bucket_arn,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        environment = self.node.try_get_context('environment')
        frontend_bucket = s3.Bucket.from_bucket_arn(
                self,
                Component.FRONTEND_BUCKET.get_component_name(environment),
                frontend_bucket_arn)
        if not exists('frontend/build'):
            return
        s3_deployment.BucketDeployment(
                self,
                Component.FRONTEND_DEPLOYMENT.get_component_name(environment),
                sources=[s3_deployment.Source.asset('frontend/build')],
                destination_bucket=frontend_bucket,
                retain_on_delete=False)
