#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_app.cdk_app_stack import CdkAppStack
from cdk_app.lambda_stack import LambdaStack

primary_env = {'account': '007756798683', 'region': 'us-east-1'}

app = cdk.App()
cdk_app_stack = CdkAppStack(app, "cdk-app", env=primary_env)
# table_one_arn = cdk.CfnParameter.value_from_lookup(
#     cdk_app_stack, "/cdk-app/tableOneParameter"
# )
# table_two_arn = cdk.CfnParameter.value_from_lookup(
#     cdk_app_stack, "/cdk-app/tableTwoParameter"
# )

lambda_stack = LambdaStack(app, 'lambda-stack', env=primary_env) #cdk_app_stack.table_objects
lambda_stack.add_dependency(cdk_app_stack)
app.synth()
