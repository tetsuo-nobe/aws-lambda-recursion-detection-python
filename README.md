# AWS Lambda の再帰呼出し検知のサンプル (Python 版)

* [Document URL](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/invocation-recursion.html)
* [Blog URL](https://aws.amazon.com/jp/blogs/compute/detecting-and-stopping-recursive-loops-in-aws-lambda-functions/)
⋆ [Java のサンプル](https://github.com/aws-samples/aws-lambda-recursion-detection-sample)

---

## サンプルの使用方法

  - AWS SAM が使用できる環境を用意して `cd aws-lambda-recursion-detection-python` に移動
  - AWS SAM でビルドする
    - Python 3.8 が使用できる場合: `sam build`
    - Python 3.8 は使用できないが Docker が使用できる場合: `sam build --use-container`
  - AWS SAM でデプロイする
    - **samconfig.toml は環境に応じて用意する必要がある。** よって当リポジトリに含まれている samconfig.toml は削除して、下記を実行して再作成する
        - `sam deploy --guided` を実行
    - **Outputs** セクションに表示される **Key** が **SourceSQSqueueURL** の値をメモしておく
  - Amazon SQS キューにメッセージを送信する
    - 下記の  <SOURCE_QUEUE_URL> をメモしておいた **SourceSQSqueueURL** の値に置き換えて実行する。

      ```
      aws sqs send-message --queue-url <SOURCE_QUEUE_URL>  --message-body '{\"orderId\":"1",\"productName\":\"Bolt\",\"orderStatus\":\"Submitted\"}' --profile devserverless

      ```
---
### 参考情報

* CloudWatch metrics
    * RecursiveInvocationsDropped 
      - 16回超えてドロップが発生した（イベントの処理を停止した）回数　

