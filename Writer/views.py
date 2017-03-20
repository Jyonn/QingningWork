import datetime

from AbstractUser.models import LikeUser
from BaseFunc.decorator import *
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


@require_POST
@require_json
@require_params(["rank_begin", "rank_end", "rank_type"])
def rank(request):
    """
    获取作者排名
    request
    {
        rank_begin: 排名首
        rank_end: 排名末
        rank_type: 排名类型，仅 total_works 和 total_received
    }
    response
    {
        rank: 排名序号
        avatar: 头像
        nickname: 昵称
        uid: 用户编号
        work_number: 排名类型作品数量
        like_number: 作者受喜爱数
        mine_like: 当前用户对作者的喜爱
    }
    """
    rank_type = request.POST["rank_type"]
    rank_begin = request.POST["rank_begin"]
    rank_end = request.POST["rank_end"]
    try:
        rank_begin = int(rank_begin)
        rank_end = int(rank_end)
    except:
        return error_response(Error.PARAM_FORMAT_ERROR)
    if rank_type not in ["total_works", "total_received"]:
        return error_response(Error.UNDEFINED_RANK_TYPE)
    writers = Writer.objects.filter(is_frozen=False).order_by("-"+rank_type)
    if rank_begin < 0:
        rank_begin = 0
    if rank_end < 0 or rank_end > writers.count():
        rank_end = writers.count()

    if require_login_func(request):
        user, user_type = get_user_from_session(request)
    else:
        user = None

    return_list = []
    rank_num = 0
    rank_rank = 0
    for i in range(0, rank_end):
        writer = writers[i]
        if i == 0:
            rank_rank = 1
            rank_num = getattr(writer, rank_type)
        else:
            this_num = getattr(writer, rank_type)
            if rank_num > this_num:
                rank_num = this_num
                rank_rank = i + 1
        if i < rank_begin:
            continue

        if user is None:
            mine_like = None
        else:
            try:
                mine_like = LikeUser.objects.get(
                    re_user_liked__uid=writer.uid,
                    re_user_to_like__uid=user.uid
                ).result
            except:
                mine_like = None
        return_list.append(dict(
            rank=rank_rank,
            uid=writer.uid,
            avatar=writer.avatar,
            nickname=writer.nickname,
            work_number=getattr(writer, rank_type),
            like_number=writer.total_likes,
            mine_like=mine_like,
        ))
    return response(body=return_list)
