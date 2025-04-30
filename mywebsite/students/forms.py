# 定義表單格式與樣式
from django import forms

# class PostForm(forms.Form):
#     stdName = forms.CharField(max_length=20, initial="")
#     stdSex = forms.CharField(max_length=2, initial="M")
#     stdBirth = forms.DateField()
#     stdEmail = forms.EmailField(max_length=100, initial="", required=False)
#     stdPhone = forms.CharField(max_length=50, initial="", required=False)
#     stdAddr = forms.CharField(max_length=255, initial="", required=False)

# 表單驗證進階設計
from django.core.validators import EmailValidator, RegexValidator

class PostForm(forms.Form):
    stdName = forms.CharField(
        max_length=20,
        label="姓名",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入姓名'
        })
    )
    
    GENDER_CHOICES = [
        ('M', '男生'),
        ('F', '女生'),
    ]
    stdSex = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="性別",
        initial='M',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    stdBirthday = forms.DateField(
        label="生日",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    stdEmail = forms.EmailField(
        max_length=100,
        label="Email",
        required=False,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'xxx@xxx.xxx'
        })
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="電話號碼格式應為: '+999999999'。最多15位數字。"
    )
    stdPhone = forms.CharField(
        max_length=50,
        label="電話",
        required=False,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入電話號碼'
        })
    )
    
    stdAddr = forms.CharField(
        max_length=255,
        label="地址",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '請輸入地址'
        })
    )
    
    def clean_stdEmail(self):
        email = self.cleaned_data.get('stdEmail')
        if email and not email.endswith(('.com', '.edu', '.org', '.net')):
            raise forms.ValidationError("請提供有效的電子郵件域名")
        return email