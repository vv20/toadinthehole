#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.stack import ToadInTheHoleStack

app = cdk.App()
ToadInTheHoleStack(
        app,
        'dev',
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleStack(
        app,
        'prod',
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))

app.synth()
