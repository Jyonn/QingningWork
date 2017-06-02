from qiniu import Auth, put_file, etag
from qiniu import BucketManager


class QiNiu:
    access_key = 'oX6jJmjudP-3BXHJ3A8lYjEQRlQHBc70734ZyTR4'
    secret_key = 'l7bAEUyU00tcjYGQ63TZw1QGksLJXXZQ2q_EqDyh'
    bucket_name = 'qingningimage'
    host = 'http://ooj8t2ocf.bkt.clouddn.com'
    q = Auth(access_key, secret_key)

    @staticmethod
    def upload(key, local_file):
        token = QiNiu.q.upload_token(QiNiu.bucket_name, key, 3600)
        ret, info = put_file(token, key, local_file)
        return ret['key'] == key and ret['hash'] == etag(local_file)

    @staticmethod
    def delete(key):
        bucket = BucketManager(QiNiu.q)
        ret, info = bucket.delete(QiNiu.bucket_name, key)
        return ret == {}
