#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_app.cdk_app_stack import CdkAppStack
from cdk_app.lambda_stack import LambdaStack
from cdk_app.combined import CombinedStack
import os

primary_env = {'account': '355986150263', 'region': 'us-east-2'}

app = cdk.App()
# combinedStack = CombinedStack(app, "cdk-app", env=primary_env)

cdkAppStack = CdkAppStack(app, "cdk-new-app", env=primary_env)

lambda_stack = LambdaStack(app, 'lambda-new-stack', ssm_parameters=cdkAppStack.ssm_parameters, env=primary_env)
lambda_stack.add_dependency(cdkAppStack)
app.synth()
