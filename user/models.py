from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Rank(models.Model):
    rank = models.CharField('등급', max_length=10)
    requirement = models.IntegerField('등급조건', validators=[MinValueValidator(0), MaxValueValidator(599)], default=0)
    ticket = models.IntegerField('등급별 응모권', validators=[MinValueValidator(0), MaxValueValidator(20)], default=1)
    photo = models.ImageField('사진', upload_to='user/rank/', null=True)
    
    def __str__(self):
        return self.rank

    class Meta:
        verbose_name_plural = "등급관리"
        verbose_name = "등급"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='이메일', max_length=30, unique=True, blank=False)
    name = models.CharField('이름', max_length=10, blank=True)
    phone = models.CharField('전화번호', max_length=13)
    address = models.CharField('주소', max_length=30, blank=True)
    # profile = models.ImageField('프로필 사진', upload_to='user/profile/', null=True, blank=True, default="user/profile/5조_erd.png")
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, verbose_name='등급', default=1)
    ticket = models.IntegerField('응모권', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    ticketing = models.IntegerField('응모횟수', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,  # 기본값을 False 로 변경
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField('가입일', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # 필수입력값

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 프로필 저장 없을 때 기본값으로 넣어주려했으나 default가 잘되어서 필요없어짐
    # def set_profile(self):
    #     _profile = self.profile
    #     if not _profile:
    #         self.profile = "user/profile/5조_erd.png"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "회원정보"
        verbose_name = "회원"


class Item(models.Model):
    name = models.CharField('도구이름', max_length=20)
    photo = models.ImageField(upload_to='user/item/', null=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "도구"
        verbose_name = "도구"
        
        
class HaveItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='도구')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='회원')
    item_count = models.IntegerField('도구 개수', default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        verbose_name_plural = "소유도구"
        verbose_name = "소유도구"
    