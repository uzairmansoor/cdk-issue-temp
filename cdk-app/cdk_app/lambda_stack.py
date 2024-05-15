import aws_cdk
from aws_cdk import Stack, aws_lambda as _lambda, aws_ssm as ssm, aws_iam as iam
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
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        enableOldLambdaDefs = parameters.enableOldLambdaDefs
        if enableOldLambdaDefs:
        ### update old_lambda_defs and new_lambda_defs here:
            for lambda_def in old_lambda_defs:
                lambda_env_data={}
                
                for table_used in lambda_def['tables_used']:
                    table_arn = ssm.StringParameter.value_from_lookup(
                        self, f"/cdk-app/{table_used}"
                    )
                    lambda_env_data[f'TABLENAME{table_used.upper()}'] = table_arn

                # for table_used in lambda_def['tables_used']:
                #     lambda_env_data[f'TABLENAME{table_used.upper()}'] = tables[table_used].table_name

                sample_lambda = _lambda.Function(self,
                    id=lambda_def['id'],
                    runtime=_lambda.Runtime.PYTHON_3_9,
                    code=_lambda.Code.from_asset("lambda"),
                    handler=f"{lambda_def['id']}.handler",
                    # role=iam.Role.from_role_arn(self, f"{lambda_def['id']}IamRole", role_arn="arn:aws:iam::355986150263:role/service-role/MyLambdaFunc-role-paxc3b5h"),
                    environment=lambda_env_data
                )

                # for table_used in lambda_def['tables_used']:
                #     tables[table_used].grant_read_write_data(sample_lambda)
        else:
            for lambda_def in new_lambda_defs:
                lambda_env_data={}

                for table_used in lambda_def['tables_used']:
                    table_arn = ssm.StringParameter.value_from_lookup(
                        self, f"/cdk-app/{table_used}"
                    )
                    lambda_env_data[f'TABLENAME{table_used.upper()}'] = table_arn
                
                # for table_used in lambda_def['tables_used']:
                #     lambda_env_data[f'TABLENAME{table_used.upper()}'] = tables[table_used].table_name

                sample_lambda = _lambda.Function(self,
                    id=lambda_def['id'],
                    runtime=_lambda.Runtime.PYTHON_3_9,
                    code=_lambda.Code.from_asset("lambda"),
                    handler=f"{lambda_def['id']}.handler",
                    environment=lambda_env_data
                )

                # for table_used in lambda_def['tables_used']:
                #     tables[table_used].grant_read_write_data(sample_lambda)
