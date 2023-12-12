#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.frontend_stack import ToadInTheHoleFrontendStack
from stack.backend_stack import ToadInTheHoleBackendStack

app = cdk.App()
ToadInTheHoleFrontendStack(
        app,
        'frontend-dev',
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleBackendStack(
        app,
        'backend-dev',
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleFrontendStack(
        app,
        'frontend-prod',
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleBackendStack(
        app,
        'backend-prod',
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))

app.synth()
