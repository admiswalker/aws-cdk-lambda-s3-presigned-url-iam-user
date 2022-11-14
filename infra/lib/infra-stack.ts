import * as cdk from 'aws-cdk-lib';
import { Stack, StackProps } from 'aws-cdk-lib';
import { aws_s3 as S3, aws_lambda as Lambda, aws_iam as Iam, aws_ssm as Ssm, aws_s3_notifications as S3notify, aws_kms as kms } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { PythonFunction, PythonLayerVersion } from '@aws-cdk/aws-lambda-python-alpha';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';


interface InfraStackProps extends StackProps {
  prj_name: string;
  env: any;
}
export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: InfraStackProps) {
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
    });
    
    /*
    const secret_key_id = new secretsmanager.Secret(this, 'SecretKeyId');
    const secret_key = new secretsmanager.Secret(this, 'SecretKey');
    const access_key = new Iam.AccessKey(this, 'AccessKey', {
      user: iam_user,
      status: {
        accessKeyId: secret_key_id.secretValue,
        accessKey: secret_key.secretValue,
      }
    });
    */
    const access_key = new Iam.CfnAccessKey(this, 'AccessKey', {
      userName: iam_user.userName,
    });
    const secret_access_key_id = new Ssm.StringParameter(this, 'SecretKeyId', {
      parameterName: 'secret-access-key-id',
      stringValue: access_key.ref, // CDK からは暗号化して保存できないため，本番では Management Console から暗号化オプションを付けて登録する．参考：https://dev.classmethod.jp/articles/to-see-the-issued-iam-access-key-does-not-change-when-the-stack-is-redeployed-by-aws-cdk/
    });
    const secret_access_key = new Ssm.StringParameter(this, 'SecretKey', {
      parameterName: 'secret-access-key',
      stringValue: access_key.attrSecretAccessKey, // CDK からは暗号化して保存できないため，本番では Management Console から暗号化オプションを付けて登録する．参考：https://dev.classmethod.jp/articles/to-see-the-issued-iam-access-key-does-not-change-when-the-stack-is-redeployed-by-aws-cdk/
    });
    /*
    //値の確認用に出力
    new cdk.CfnOutput(this, "access_key_id", { value: secret_access_key_id });
    new cdk.CfnOutput(this, "secret_access_key", {
      value: secret_access_key,
    });
    //*/

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
        }
      ]
    };
    const lambda_exe_role = new Iam.Role(this, 'lambda_exe_role', {
      roleName: 'example_lambda_exe_role',
      assumedBy: new Iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [Iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore')],
      inlinePolicies: {
        inlinePolicies: Iam.PolicyDocument.fromJson(json),
      },
    });
    secret.grantRead(lambda_exe_role);
    s3_raw_bucket.grantRead(lambda_exe_role);
    secret_access_key_id.grantRead(lambda_exe_role);
    secret_access_key.grantRead(lambda_exe_role);

    const s3_presigned_url_policy = new Iam.Policy(this, 'policy', { 
      policyName: 's3access',
      statements: [ new Iam.PolicyStatement({
        effect: Iam.Effect.ALLOW,
        actions: [
          's3:GetObject',
        ],
        resources: [s3_raw_bucket.bucketArn+'/*'],
      })],
    });
    iam_user.attachInlinePolicy(s3_presigned_url_policy);

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
