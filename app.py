#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.cdn_stack import ToadInTheHoleCDNStack
from stack.main_stack import ToadInTheHoleMainStack

app = cdk.App()

environment = app.node.try_get_context('environment')

stack = cdk.Stack(app, environment)

ToadInTheHoleMainStack(
        stack,
        'main-' + environment,
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleCDNStack(
        stack,
        'cdn-' + environment,
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='us-east-1'))
app.synth()
