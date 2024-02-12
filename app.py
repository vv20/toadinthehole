#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.cdn_stack import ToadInTheHoleCDNStack
from stack.frontend_deployment_stack import \
    ToadInTheHoleFrontendDeploymentStack
from stack.main_stack import ToadInTheHoleMainStack

app = cdk.App()

environment = app.node.try_get_context('environment')

cdn_stack = ToadInTheHoleCDNStack(
        app,
        'cdn-' + environment,
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='us-east-1'))
main_stack = ToadInTheHoleMainStack(
        app,
        'main-' + environment,
        cdn_stack.frontend_certificate_arn,
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleFrontendDeploymentStack(
        app,
        'frontend-deployment-' + environment,
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))



app.synth()
