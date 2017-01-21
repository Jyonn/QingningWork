import datetime
from Base.decorator import *
from Work.models import Work
from Comment.models import Comment
from Writer.models import Writer
from Work.views import get_packed_work


def get_rank(writer, order_by):
    writers = Writer.objects.filter(is_frozen=False).order_by(order_by)
    attr = order_by
    if order_by[0] == '-':
        attr = attr[1:]
    rank = 0
    for ret_writer in writers:
        rank += 1
        if getattr(ret_writer, attr) == getattr(writer, attr):
            break
    return rank


@require_POST
@require_login_writer
def info(request):
    """
    获取作者基本信息
    response
    {
        nickname: 笔名/昵称
        avatar: 头像地址
        total_works: 全部作品数
        total_received: 被采纳的作品数
        total_refused: 被驳回的作品数
        total_fee: 全部稿费
        total_works_rank: 全部作品排名
        total_received_rank: 被采纳作品排名
        login_times: 登录次数
        last_ipv4: 上次登录地址
        last_login: 上次登录时间
    }
    """
    writer, user_type = get_user_from_session(request)
    if writer is None:
        return error_response(Error.LOGIN_AGAIN)
    total_works_rank = get_rank(writer, "-total_works")
    total_received_rank = get_rank(writer, "-total_received")

    last_login_str = "第一次登录" if writer.last_login is None else writer.last_login.strftime("%Y-%m-%d %H:%M:%S")
    ip_str = "第一次登录" if writer.last_ipv4 is None else get_address_by_ip_via_sina(writer.last_ipv4)

    return_dict = dict(
        nickname=writer.nickname,
        avatar=writer.avatar,
        total_works=writer.total_works,
        total_received=writer.total_received,
        total_refused=writer.total_refused,
        total_fee=writer.total_fee,
        total_works_rank=total_works_rank,
        total_received_rank=total_received_rank,
        login_times=writer.login_times,
        last_ipv4=ip_str,
        last_login=last_login_str,
    )

    return response(body=return_dict)


def get_related_lists(request):
    """
    获取作者作品列表
    response
    {
        code: 0,
        msg: "ok",
        body: [{
            wid: 作品编号
            writer_name: 作者名称
            work_name: 作品名称
            create_time: 创建时间
            status: 稿件状态
            is_public: 是否公开
            is_delete: 是否被删除
            recv_num: 过审数
            refs_num: 驳回数
        },  {
            ...
        }]
    }
    """
    # 获取作者
    writer, user_type = get_user_from_session(request)
    if writer is None:
        return error_response(Error.LOGIN_AGAIN)

    # 获取所有此作者的非删除稿件
    works = Work.objects.filter(
        re_writer=writer,
        is_delete=False,  # 非删除稿件
    )

    return_list = []
    for work in works:
        return_list.append(get_packed_work(work))

    return response(body=return_list)
