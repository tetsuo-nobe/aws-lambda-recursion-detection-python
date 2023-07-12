# AWS Lambda の再帰呼出し検知のサンプル (Python 版)

* [AWS Document](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/invocation-recursion.html)
* [AWS Blog](https://aws.amazon.com/jp/blogs/compute/detecting-and-stopping-recursive-loops-in-aws-lambda-functions/)
* [Java のサンプル](https://github.com/aws-samples/aws-lambda-recursion-detection-sample)

---

## サンプルの使用方法
  - **シナリオ**: ソースキューから注文メッセージを受信して、ステータスを **Processed** に書き換えた後にターゲットキューに送信するところを、環境変数の設定を間違えてソースキューに送信してしまった。それゆえ、再帰呼出しが発生する。 再帰呼出し検知が発動して、16回を超える呼出しが発生した時、それ以上呼出しを行わないことを確認する。

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
  - 再帰呼出し検知を確認する
    - Lambda 関数 `demo-recursion-detection-python` の CloudWatch Logs を参照して、16 回呼び出されていることを確認する
      - 検索で `START` を指定するとわかりやすい
    - SQS キュー `demo-recursion-detection-deadletter-queue` に送信したメッセージが格納されていることを確認する 

      ```
      aws sqs send-message --queue-url <SOURCE_QUEUE_URL>  --message-body '{\"orderId\":"1",\"productName\":\"Bolt\",\"orderStatus\":\"Submitted\"}' --profile devserverless

      ```
---
### 参考情報

* CloudWatch metrics
    * RecursiveInvocationsDropped 
      - 16回超えてドロップが発生した（イベントの処理を停止した）回数　

