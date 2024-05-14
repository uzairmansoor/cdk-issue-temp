#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_app.cdk_app_stack import CdkAppStack
from cdk_app.lambda_stack import LambdaStack

primary_env = {'account': '355986150263', 'region': 'us-east-1'}

app = cdk.App()
cdk_app_stack = CdkAppStack(app, "cdk-app", env=primary_env)
# table_one_arn = cdk.CfnParameter.value_from_lookup(
#     cdk_app_stack, "/cdk-app/tableOneParameter"
# )
# table_two_arn = cdk.CfnParameter.value_from_lookup(
#     cdk_app_stack, "/cdk-app/tableTwoParameter"
# )

LambdaStack(app, 'lambda-stack', env=primary_env) #cdk_app_stack.table_objects

app.synth()
