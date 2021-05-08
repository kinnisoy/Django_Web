from django import forms
from captcha.fields import CaptchaField     # 一定要导入这行


class UserForm(forms.Form):
    captcha = CaptchaField(label='验证码',
                           required=True,
                            error_messages={'required': '验证码不能为空'})
