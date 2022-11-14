# aws-cdk-lambda-s3-presigned-url-iam-user

## AWS CDK プロジェクトの初期化

```
$ mkdir [MakeEmptyDir]
$ cd [MakeEmptyDir]
$ cdk init app --language typescript
```

## Lambda のデプロイメントパッケージ作成

- [.zip ファイルアーカイブで Python Lambda 関数をデプロイする](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-package.html)
- [aws_s3_hook_lambda/lib/lambda/cnvFile/](https://github.com/admiswalker/aws_s3_hook_lambda/tree/main/lib/lambda/cnvFile)

## IAM User と Secret の管理

- [Python アプリケーションで AWS Secrets Manager シークレットを取得する](https://docs.aws.amazon.com/ja_jp/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html)
- [CloudFormationでIAMアクセスキーの発行とSecrets Managerへの格納をしてみた](https://dev.classmethod.jp/articles/issuing-iam-access-keys-and-storing-them-in-secrets-manager-with-cloudformation/)
- [[AWS CDK] 発行したIAMアクセスキーがスタックの再デプロイ時に変更されないのか確認してみた](https://dev.classmethod.jp/articles/to-see-the-issued-iam-access-key-does-not-change-when-the-stack-is-redeployed-by-aws-cdk/)

