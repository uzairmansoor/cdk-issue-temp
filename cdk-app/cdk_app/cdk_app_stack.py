import aws_cdk
from aws_cdk import Stack, CfnOutput, aws_events_targets
from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ssm as ssm
from aws_cdk import Aws as AWS
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

###################################  Running  ####################################################
class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table_objects = {}
        self.ssm_parameters = {}

        # enableOldTableDefs = parameters.enableOldTableDefs
        # table_defs = old_table_defs if enableOldTableDefs else new_table_defs
        # for table_def in table_defs:
        #     table_object = _dynamodb.Table(self,
        #         table_name= f"{parameters.project}-{parameters.env}-{parameters.app}-oldDynamoTable",
        #         id=table_def['id'],
        #         partition_key=_dynamodb.Attribute(
        #             name=table_def['partition_key'],
        #             type=_dynamodb.AttributeType.STRING
        #         ),
        #         billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
        #         removal_policy=aws_cdk.RemovalPolicy.DESTROY
        #     )

        #     self.table_objects[table_def['id']] = table_object

        #     ssm_param = ssm.StringParameter(
        #         self, f"{table_def['id']}Parameter",
        #         parameter_name=f"/{construct_id}/{table_def['id']}",
        #         string_value=table_object.table_name,
        #         simple_name=False,
        #     )
        #     self.ssm_parameters[table_def['id']] = ssm_param.string_value

###################################  Running  ####################################################

        enableOldTableDefs = parameters.enableOldTableDefs
        if enableOldTableDefs:
            for table_def in old_table_defs:
                table_object = _dynamodb.Table(self,
                    # table_name= f"{parameters.project}-{parameters.env}-{parameters.app}-oldDynamoTable",
                    id=table_def['id'],
                    partition_key=_dynamodb.Attribute(
                        name=table_def['partition_key'],
                        type=_dynamodb.AttributeType.STRING
                    ),
                    billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
                    removal_policy=aws_cdk.RemovalPolicy.DESTROY
                )

                self.table_objects[table_def['id']] = table_object

                ssm_param = ssm.StringParameter(
                    self, f"{table_def['id']}Parameter",
                    parameter_name=f"/{construct_id}/{table_def['id']}",
                    string_value=table_object.table_name,
                    simple_name=False,
                )
                self.ssm_parameters[table_def['id']] = ssm_param.string_value
        else:
            for table_def in new_table_defs:
                table_object = _dynamodb.Table(self,
                    # table_name= f"{parameters.project}-{parameters.env}-{parameters.app}-newDynamoTable",
                    id=table_def['id'],
                    partition_key=_dynamodb.Attribute(
                        name=table_def['partition_key'],
                        type=_dynamodb.AttributeType.STRING
                    ),
                    billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
                    removal_policy=aws_cdk.RemovalPolicy.DESTROY
                )

                self.table_objects[table_def['id']] = table_object

                ssm_param = ssm.StringParameter(
                    self, f"{table_def['id']}Parameter",
                    parameter_name=f"/{construct_id}/{table_def['id']}",
                    string_value=table_object.table_name,
                    simple_name=False,
                )
                self.ssm_parameters[table_def['id']] = ssm_param.string_value