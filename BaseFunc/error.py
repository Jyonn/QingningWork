# coding=utf-8
class Error:
    def __init__(self):
        pass

    NOT_FOUND_USER_ID = 1028
    PARAM_FORMAT_ERROR = 1027
    UNDEFINED_RANK_TYPE = 1026
    COMMENT_TOO_LONG = 1025
    WORK_NAME_TOO_LONG = 1024
    NICKNAME_TOO_LONG = 1023
    CAN_NOT_DELETE_CAUSE_CONFIRMED = 1022
    EXIST_USERNAME = 1021
    WRONG_USERNAME = 1020
    EXIST_NICKNAME = 1019
    LOGIN_AGAIN = 1018
    FROZEN_USER = 1017
    NOT_YOUR_WORK = 1016
    NOT_UNDER_REVIEW = 1015
    WORK_IS_PRIVATE = 1014
    WORK_HAS_DELETED = 1013
    NOT_FOUND_WORK_ID = 1012
    NOT_FOUND_WORK_TYPE = 1011
    NOT_FOUND_FILE = 1010
    REQUIRE_REVIEWER = 1009
    REQUIRE_WRITER = 1008
    NO_PASSWORD_LOGIN = 1007
    DENY_LOGIN = 1006
    NEED_LOGIN = 1005
    WRONG_PASSWORD = 1004
    NOT_FOUND_USERNAME = 1003
    REQUIRE_PARAM = 1002
    REQUIRE_JSON = 1001
    NOT_FOUND_ERROR = 1000
    UNKNOWN = 1
    OK = 0

    ERROR_DICT = [
        (OK, "操作成功"),
        (UNKNOWN, "未知错误"),
        (NOT_FOUND_ERROR, "不存在的错误"),
        (REQUIRE_JSON, "需要JSON数据"),
        (REQUIRE_PARAM, "参数不完整"),
        (NOT_FOUND_USERNAME, "不存在的用户名"),
        (WRONG_PASSWORD, "用户名或密码错误"),
        (NEED_LOGIN, "尚未登录"),
        (DENY_LOGIN, "已经登录"),
        (NO_PASSWORD_LOGIN, "已开启免密登录"),
        (REQUIRE_WRITER, "需要作者登录"),
        (REQUIRE_REVIEWER, "需要审稿员登录"),
        (NOT_FOUND_FILE, "没有上传的文件"),
        (NOT_FOUND_WORK_TYPE, "不存在的作品类型"),
        (NOT_FOUND_WORK_ID, "不存在的作品"),
        (WORK_HAS_DELETED, "作品已被删除"),
        (WORK_IS_PRIVATE, "作品没有公开"),
        (NOT_UNDER_REVIEW, "作品不在审阅状态"),
        (NOT_YOUR_WORK, "不是你的作品"),
        (FROZEN_USER, "账号被冻结，请联系社长"),
        (LOGIN_AGAIN, "重新登录"),
        (EXIST_NICKNAME, "已存在的昵称"),
        (WRONG_USERNAME, "错误的账号"),
        (EXIST_USERNAME, "已存在的账号"),
        (CAN_NOT_DELETE_CAUSE_CONFIRMED, "稿件已被确认收录，无法删除"),
        (NICKNAME_TOO_LONG, "笔名不能超过6个字符"),
        (WORK_NAME_TOO_LONG, "作品名称不能超过20个字符"),
        (COMMENT_TOO_LONG, "评论不能超过300个字符"),
        (UNDEFINED_RANK_TYPE, "未定义的排序类型"),
        (PARAM_FORMAT_ERROR, "参数格式错误"),
        (NOT_FOUND_USER_ID, "不存在的用户"),
    ]
