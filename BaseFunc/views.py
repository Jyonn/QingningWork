from BaseFunc.decorator import *
from BaseFunc.img_captcha import create_validate_code


@require_GET
def get_image_captcha(request):
    """
    生成图片验证码
    """
    captcha_img_correct, img_pil = create_validate_code(point_chance=1)
    save_captcha(request, "image", captcha_img_correct)

    resp = HttpResponse('', content_type='image/jpg')
    img_pil.save(resp, format='jpeg')  # 将图片PIL写入到响应中
    # 在响应头部告诉浏览器不要缓存这个图片
    resp['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
    return resp


@require_POST
@require_json
@require_params(["captcha"])
def confirm_image_captcha(request):
    """
    验证图片验证码
    """
    captcha = request.POST["captcha"]
    ret_code = confirm_captcha(request, "image", captcha)
    return response(body=ret_code)
