import * as cdk from 'aws-cdk-lib';
import { aws_s3 as S3, aws_lambda as Lambda, aws_iam as Iam, aws_ssm as Ssm, aws_s3_notifications as S3notify } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { PythonFunction, PythonLayerVersion } from '@aws-cdk/aws-lambda-python-alpha';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';


export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // S3 bucket
    const s3_raw_bucket = new S3.Bucket(this, 's3-raw-bucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    })
    
    const s3_proced_bucket = new S3.Bucket(this, 's3-proced-bucket', {
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    })

    const secret = new secretsmanager.Secret(this, 'Secret');
    const iam_user = new Iam.User(this, 'User', {
      password: secret.secretValue
    })

    const json = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "s3:ListBucket",
            "s3:ListAllMyBuckets"
          ],
          "Resource": ["*"]
        },
        {
          "Effect": "Allow",
          "Action": [
            "s3:GetObject",
            "s3:GetObjectVersion"
          ],
          "Resource": [
            s3_raw_bucket.bucketArn,
            s3_raw_bucket.bucketArn+"/*"
          ]
        }
      ]
    };
    const lambda_exe_role = new Iam.Role(this, 'lambda_exe_role', {
      roleName: 'example_lambda_exe_role',
      assumedBy: new Iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [],
      inlinePolicies: {
        inlinePolicies: Iam.PolicyDocument.fromJson(json),
      },
    });

    // lambda function triggered by s3 hook
    const s3_hook_lambda = new PythonFunction(this, 'LambdaFunction', {
      role: lambda_exe_role,
      timeout: cdk.Duration.seconds(10),
      entry: 'lib/lambda/src',
      runtime: Lambda.Runtime.PYTHON_3_9,
      index: 'index.py',
      handler: 'handler',
      environment: {
        S3_PROCED_BUCKET_NAME: s3_raw_bucket.bucketName,
        SECRET_NAME: secret.secretName,
      },
    });
    //s3_raw_bucket.addObjectCreatedNotification(new S3notify.LambdaDestination(s3_hook_lambda))
    //s3_raw_bucket.grantRead(s3_hook_lambda) // CreatedNotification により lambda が再帰呼び出しできないように，read か write のみ付与する
    //s3_proced_bucket.grantWrite(s3_hook_lambda) // CreatedNotification により lambda が再帰呼び出しできないように，read か write のみ付与する
  }
}
