import aws_cdk
from aws_cdk import Stack, CfnOutput, Aws as AWS
from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets
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
    },
    {
        'id': 'tableTwo',
        'partition_key': "PartitionKey"
    }
]

old_lambda_defs = [
    {
        'id': 'lambdaOne',
        'tables_used': [
            'tableOne'
        ]
    },
    {
        'id': 'lambdaTwo',
        'tables_used': [
            'tableOne', 'tableTwo'
        ]
    }
]

new_lambda_defs = [
    {
        'id': 'lambdaOne',
        'tables_used': [
            'tableOne'
        ]
    },
    {
        'id': 'lambdaTwo',
        'tables_used': [
            'tableOne', 'tableTwo'
        ]
    }
]

class CombinedStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table_objects = {}
        self.ssm_parameters = {}

        enableOldTableDefs = parameters.enableOldTableDefs
        table_defs = old_table_defs if enableOldTableDefs else new_table_defs
        for table_def in table_defs:
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

            ssm_param = ssm.StringParameter(
                self, f"{table_def['id']}Parameter",
                parameter_name=f"/{construct_id}/{table_def['id']}",
                string_value=table_object.table_name,
                simple_name=False,
            )
            self.ssm_parameters[table_def['id']] = ssm_param.string_value

        self.create_lambda_functions()

    def create_lambda_functions(self):
        lambdaExecutionRole = iam.Role(self, "lambdaExecutionRole",
            role_name="lambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        lambdaExecutionRole.attach_inline_policy(
            iam.Policy(self, 'dynamodbPolicy',
                statements=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "dynamodb:Query"
                        ],
                        resources=[
                            f"arn:aws:dynamodb:{AWS.REGION}:{AWS.ACCOUNT_ID}:table/*"
                        ]
                    )
                ]
            )
        )

        enableOldLambdaDefs = parameters.enableOldLambdaDefs
        lambda_defs = old_lambda_defs if enableOldLambdaDefs else new_lambda_defs
        for lambda_def in lambda_defs:
            lambda_env_data = {}

            for table_used in lambda_def['tables_used']:
                table_name = self.ssm_parameters.get(table_used)
                lambda_env_data[f'TABLENAME{table_used.upper()}'] = table_name

            sample_lambda = _lambda.Function(self,
                id=lambda_def['id'],
                runtime=_lambda.Runtime.PYTHON_3_9,
                code=_lambda.Code.from_asset("lambda"),
                handler=f"{lambda_def['id']}.handler",
                role=iam.Role.from_role_arn(self, f"{lambda_def['id']}IamRole", role_arn=lambdaExecutionRole.role_arn),
                environment=lambda_env_data
            )
