import datetime

from Base.decorator import *
from Work.models import Work


@require_POST
@require_json
@require_params(["work_type", "work_name", "writer_name", "content"])
@require_login_reviewer
def upload_work(request):
    work_type = request.POST["work_type"]  # 作品类型（WORK_TYPE_FILE文件上传; WORK_TYPE_TEXT文本上传）
    work_name = request.POST["work_name"]  # 作品名称，指题目
    writer_name = request.POST["writer_name"]  # 作者名称
    content = request.POST["content"]
    reviewer, user_type = get_user_from_session(request)

    try:
        work_type = int(work_type)
    except:
        return error_response(Error.NOT_FOUND_WORK_TYPE)
    if work_type not in [Work.WORK_TYPE_FILE, Work.WORK_TYPE_TEXT]:
        # 不存在的作品类型
        return error_response(Error.NOT_FOUND_WORK_TYPE)

    if work_type == Work.WORK_TYPE_FILE:
        # 如果是文件，获取文件扩展名
        if request.FILES.get("file") is None:
            return error_response(Error.NOT_FOUND_FILE)
        str = request.FILES.get("file").name
        ext_name = "" if str.find(".") == -1 else "." + str.split(".")[-1]
    else:
        # 如果是文本，默认扩展名为txt
        ext_name = ".txt"

    moment = datetime.datetime.now()
    head_filename = moment.strftime("%Y%m%d_%H%M%S_")
    from django.utils.crypto import get_random_string
    # 保存的文件名设置为上传时间+随机子串+扩展名
    filename = head_filename + get_random_string(length=8) + ext_name[:8]
    from QingningWork.settings import WORK_URL
    # 保存的文件路径
    file_path = WORK_URL + filename

    if work_type == Work.WORK_TYPE_FILE:
        # 上传文件，使用chunk保存
        save_file = request.FILES.get("file")
        with open(file_path, "wb+") as f:
            for chunk in save_file.chunks():
                f.write(chunk)
            f.close()
    else:
        # 保存文本文件
        with open(file_path, "wb+") as f:
            f.write(content)
            f.close()

    # 存入数据库
    Work.create(
        re_reviewer=reviewer,
        writer_name=writer_name,
        work_name=work_name,
        work_store=file_path,
        work_type=work_type,
        is_public=True,
        status=Work.STATUS_UNDER_REVIEW,
    )

    return response()
