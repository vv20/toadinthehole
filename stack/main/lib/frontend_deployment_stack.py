from os.path import exists

from aws_cdk import Fn, Stack
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from constructs import Construct

from ..common import Component


class ToadInTheHoleFrontendDeploymentStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.stack_environment: str = self.node.try_get_context('environment')
        self.frontend_bucket_arn: str = Fn.import_value(Component.FRONTEND_BUCKET_EXPORT.get_component_name(self.stack_environment))

        self.frontend_bucket: s3.Bucket = s3.Bucket.from_bucket_arn(
                self,
                Component.FRONTEND_BUCKET.get_component_name(self.stack_environment),
                self.frontend_bucket_arn)
        if not exists('frontend/build'):
            return
        self.frontend_deployment: s3_deployment.BucketDeployment = s3_deployment.BucketDeployment(
                self,
                Component.FRONTEND_DEPLOYMENT.get_component_name(self.stack_environment),
                sources=[s3_deployment.Source.asset('frontend/build')],
                destination_bucket=self.frontend_bucket,
                retain_on_delete=False)
