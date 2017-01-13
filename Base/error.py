class Error:
    NOT_FOUND_WORK_TYPE = 1011
    NOT_FOUND_FILE = 1010
    NEED_REVIEWER = 1009
    NEED_WRITER = 1008
    NO_PASSWORD_LOGIN = 1007
    DENY_LOGIN = 1006
    NEED_LOGIN = 1005
    WRONG_PASSWORD = 1004
    NOT_FOUND_USERNAME = 1003
    NEED_PARAM = 1002
    NEED_JSON = 1001
    NOT_FOUND_ERROR = 1000
    UNKNOWN = 1

    ERROR_DICT = [
        (UNKNOWN, "未知错误"),
        (NOT_FOUND_ERROR, "不存在的错误"),
        (NEED_JSON, "需要JSON数据"),
        (NEED_PARAM, "参数不完整"),
        (NOT_FOUND_USERNAME, "不存在的用户名"),
        (WRONG_PASSWORD, "用户名或密码错误"),
        (NEED_LOGIN, "尚未登录"),
        (DENY_LOGIN, "已经登录"),
        (NO_PASSWORD_LOGIN, "已开启免密登录"),
        (NEED_WRITER, "需要作者登录"),
        (NEED_REVIEWER, "需要审稿员登录"),
        (NOT_FOUND_FILE, "没有上传的文件"),
        (NOT_FOUND_WORK_TYPE, "不存在的作品类型"),
    ]
