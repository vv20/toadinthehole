#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stack.cdn_stack import ToadInTheHoleCDNStack
from stack.main_stack import ToadInTheHoleMainStack

app = cdk.App()
ToadInTheHoleCDNStack(
        app,
        'cdn-dev',
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleMainStack(
        app,
        'main-dev',
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleCDNStack(
        app,
        'cdn-prod',
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
ToadInTheHoleMainStack(
        app,
        'main-prod',
        cross_region_references=True,
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')))
app.synth()
