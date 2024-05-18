import aws_cdk
from aws_cdk import Stack, aws_lambda as _lambda, aws_ssm as ssm, aws_iam as iam, Aws as AWS
from constructs import Construct
from . import parameters

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
            'tableOne','tableTwo'
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
            'tableOne'
        ]
    }
]
class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, ssm_parameters: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaExecutionRole = iam.Role(self, "lambdaExecutionRole",
            role_name = "lambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        
        lambdaExecutionRole.attach_inline_policy(
            iam.Policy(self, 'ec2MskClusterPolicy',
                statements = [
                    iam.PolicyStatement(
                        effect = iam.Effect.ALLOW,
                        actions=[
                            "dynamodb:Query"
                        ],
                        resources= [
                            f"arn:aws:dynamodb:{AWS.REGION}:{AWS.ACCOUNT_ID}:table/*"
                        ]
                    )
                ]
            )
        )

        self.ssm_parameters = ssm_parameters

        enableOldLambdaDefs = parameters.enableOldLambdaDefs
        lambda_defs = old_lambda_defs if enableOldLambdaDefs else new_lambda_defs
        for lambda_def in lambda_defs:
            lambda_env_data={}
            
            for table_used in lambda_def['tables_used']:
                # table_name = ssm.StringParameter.value_from_lookup(
                #     self, f"/cdk-app/{table_used}"
                # )
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
        
        # else:
        #     for lambda_def in new_lambda_defs:
        #         lambda_env_data={}

        #         for table_used in lambda_def['tables_used']:
        #             table_name = ssm.StringParameter.value_from_lookup(
        #                 self, f"/cdk-app/{table_used}"
        #             )
        #             lambda_env_data[f'TABLENAME{table_used.upper()}'] = table_name

        #         sample_lambda = _lambda.Function(self,
        #             id=lambda_def['id'],
        #             runtime=_lambda.Runtime.PYTHON_3_9,
        #             code=_lambda.Code.from_asset("lambda"),
        #             handler=f"{lambda_def['id']}.handler",
        #             environment=lambda_env_data
        #         )

                # for table_used in lambda_def['tables_used']:
                #     tables[table_used].grant_read_write_data(sample_lambda)
