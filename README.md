# Amazon SNS Batch SMS Subscription Creator

## 使用方式

準備好存有手機號碼的檔案 `phones.txt`：

```text
09203**3**
09808**2**
```

確定要訂閱的 Amazon SNS topic ARN `arn:aws:sns:<region>:<account ID>:<topic name>`，記得檢查是否有權限新增訂閱到這個 topic。

安裝套件：

```
$ pipenv install
```

執行程式訂閱：

```
$ pipenv run python create_subscriptions.py arn:aws:sns:<region>:<account ID>:<topic name> phones.txt
```
