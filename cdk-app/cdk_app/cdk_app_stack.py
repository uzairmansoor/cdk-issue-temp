import aws_cdk
from aws_cdk import Stack, CfnOutput, aws_events_targets
from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from constructs import Construct
from . import parameters

old_table_defs = [
    {
        'id': 'tableOne',
        'partition_key': "PartitionKey"
    },
    {
        'id': 'tableTwo',
        'partition_key': "PartitionKey"
    }
]

new_table_defs = [
    {
        'id': 'tableOne',
        'partition_key': "PartitionKey"
    }
]

class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table_objects = {}

        enableOldTableDefs = parameters.enableOldTableDefs
        if enableOldTableDefs:
        ### update old_table_defs and new_table_defs here:
            for table_def in old_table_defs:
                table_object = _dynamodb.Table(self,
                    id=table_def['id'],
                    partition_key=_dynamodb.Attribute(
                        name=table_def['partition_key'],
                        type=_dynamodb.AttributeType.STRING
                    ),
                    billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
                    removal_policy=aws_cdk.RemovalPolicy.DESTROY
                )

                # self.table_objects[table_def['id']] = table_object

                ssm.StringParameter(
                    self, f"{table_def['id']}Parameter",
                    parameter_name=f"/{construct_id}/{table_def['id']}",
                    string_value=table_object.table_arn,
                    simple_name=False,
                )
        else:
            for table_def in new_table_defs:
                table_object = _dynamodb.Table(self,
                    id=table_def['id'],
                    partition_key=_dynamodb.Attribute(
                        name=table_def['partition_key'],
                        type=_dynamodb.AttributeType.STRING
                    ),
                    billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
                    removal_policy=aws_cdk.RemovalPolicy.DESTROY
                )

                self.table_objects[table_def['id']] = table_object

                ssm.StringParameter(
                    self, f"{table_def['id']}Parameter",
                    parameter_name=f"/{construct_id}/{table_def['id']}",
                    string_value=table_object.table_arn,
                    simple_name=False,
                )

###############################################################################################
        #     CfnOutput(self, f'{table_def["id"]}Arn', value=table_object.table_arn)

        # # Create a custom resource to monitor table deletion
        # delete_handler = _lambda.Function(self, 'TableDeleteHandler',
        #     runtime=_lambda.Runtime.PYTHON_3_9,
        #     handler='deleteTable.handler',
        #     code=_lambda.Code.from_asset('lambda'),
        #     environment={
        #         'TABLE_NAMES': ','.join([table_def['id'] for table_def in new_table_defs])
        #     }
        # )

        # # Subscribe the handler to relevant CloudFormation events
        # events.Rule(self, 'TableDeleteRule',
        #     event_pattern={
        #         'source': ['aws.cloudformation'],
        #         'detail': {
        #             'eventName': ['DeleteStack', 'DeleteResource']
        #         }
        #     },
        #     targets=[aws_events_targets.LambdaFunction(delete_handler)]
        # )

        # # Grant permissions for the delete handler to modify lambda functions
        # delete_handler.add_to_role_policy(iam.PolicyStatement(
        #     actions=[
        #         'lambda:UpdateFunctionCode',
        #         'lambda:UpdateFunctionConfiguration'
        #     ],
        #     resources=['*']
        # ))

        # # Export delete handler ARN
        # CfnOutput(self, 'DeleteHandlerArn', value=delete_handler.function_arn)