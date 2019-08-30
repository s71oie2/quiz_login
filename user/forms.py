from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField
from .validators import RegisteredEmailValidator
from django.core.files.images import get_image_dimensions
# 회원가입
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
                # 8.19 소이 - 변경
                'email', 'name', 'postcode', 'address', 'detail_address', 'ref_address', 'phone',
        ]

    # def clean_profile(self):
    #     profile = self.cleaned_data['profile']
    #
    #     try:
    #         w, h = get_image_dimensions(profile)
    #
    #         # validate dimensions
    #         max_width = max_height = 500
    #         if w > max_width or h > max_height:
    #             raise forms.ValidationError(
    #                 u'Please use an image that is '
    #                 '%s x %s pixels or smaller.' % (max_width, max_height))
    #
    #         # validate content type
    #         main, sub = profile.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
    #             raise forms.ValidationError(u'Please use a JPEG, '
    #                                         'GIF or PNG image.')
    #
    #         # validate file size
    #         if len(profile) > (20 * 1024):
    #             raise forms.ValidationError(
    #                 u'Avatar file size may not exceed 20k.')
    #
    #     except AttributeError:
    #         """
    #         Handles case when we are updating the user profile
    #         and do not supply a new avatar
    #         """
    #         pass
    #
    #     return profile
# 로그인
class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

# 재발송 이메일
class VerificationEmailForm(forms.Form):
    email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))

# 190705 예림
# 마이페이지
class profileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'postcode', 'address', 'detail_address', 'ref_address', 'phone', ]

