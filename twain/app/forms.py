from django import forms
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from .models import *
# from django_countries.widgets import CountrySelectWidget
from .models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','id':'password1','placeholder':'Enter your password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control','id':'password2','placeholder':'Confirm your password'}))

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name','username1')
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control','id':'email','placeholder':'Enter your email'}),
            'username1':forms.TextInput(attrs={'class':'form-control','id':'username','placeholder':'Enter your name'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','id':'first_name','placeholder':'Enter your first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','id':'last_name','placeholder':'Enter your last name'}),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class DealerForm(forms.ModelForm):
    class Meta:
        model=DealerProfileModel
        fields='__all__'
        exclude = ['user']

        widgets={
            # 'company_email':forms.EmailInput(attrs={'class':'form-control','id':'company_email','placeholder':"Enter your Company's email"}),
            'company_logo':forms.FileInput(attrs={
                'class':'form-control','id':'company_logo'
            }),
            'company_desc':forms.TextInput(attrs={'class':'form-control','id':'company_desc','placeholder':"Enter a detailed description about your company"}),
            'company_short_desc':forms.TextInput(attrs={'class':'form-control','id':'company_short_desc','placeholder':"Enter a short description about your company"}),
        }

class CostomerForm(forms.ModelForm):
    class Meta:
        model=CostomerProfileModel
        fields= ['city','state','profile_desc','profile_picture','resume','long_description','category']
        #exclude = ['user']'__all__'
        #  'address','skills', 'experience', 'available', 'linkedin_profile', 'github_profile', 'language', 'Education', 'dob'
        widgets={
            # 'address':forms.TextInput(attrs={'class':'form-control','id':'address','placeholder':"Enter your address"}),
            'city':forms.TextInput(attrs={'class':'form-control','id':'city','placeholder':"Enter your city"}),
            # 'country':CountrySelectWidget(),
            'state':forms.TextInput(attrs={'class':'form-control','id':'state','placeholder':"Enter your state"}),
            'profile_desc':forms.TextInput(attrs={'class':'form-control','id':'profile_desc','placeholder':"profile description"}),
            'category':forms.Select(attrs={'class':'form-control','id':'category','placeholder':"----"}),
            # 'linkedin_profile':forms.TextInput(attrs={'class':'form-control','id':'linkedin_profile','placeholder':"Enter your linkedin profile"}),
            # 'github_profile':forms.TextInput(attrs={'class':'form-control','id':'github_profile','placeholder':"Enter your github profile"}),
            'profile_picture':forms.FileInput(attrs={'class':'form-control','id':'profile_picture'}),
            'resume':forms.FileInput(attrs={'class':'form-control','id':'resume'}),
            'long_description':forms.TextInput(attrs={'class':'form-control','id':'long_description','placeholder':"Enter a detailed description about you"}),
        }


class PostJobForm(forms.ModelForm):
    # option_1 = PostjobModel.objects.get(job_type)
    # option_2 = PostjobModel.objects.get(job_type__id = 2)
    
    class Meta:
        model=PostjobModel
        
        fields= '__all__'
        exclude = ['is_completed', 'slug', 'Attachment', ]
        # try:
        #     job_type = JobTypeModel.objects.all()
        #     Choices = []
        #     for i in job_type:
        #         a = (str(i.id), i.job_type_title)
        #         Choices.append(a)
        #     print(Choices)
        # except:
        #     pass
    
        # ['job_title','short_desc','full_desc','deadline','askamount']
        widgets={
            'job_title':forms.TextInput(attrs={'class':'form-control','id':'job_title','placeholder':""}),
            'short_desc':forms.TextInput(attrs={'class':'form-control','id':'short_desc','placeholder':""}),
            'full_desc':CKEditorWidget(),
            'deadline':forms.DateInput(attrs={'type':'date','class':'form-control','id':'deadline','placeholder':"Enter Deadline for the job"}),
            'askamount':forms.TextInput(attrs={
                'id':'askamount',}),
            'askamount_2':forms.TextInput(attrs={
                'id':'askamount'}),
            'category_type':forms.Select(attrs={'class':'form-select'}),
            'skill_type': forms.SelectMultiple()
            }

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model=ApplyForJobModel
        fields=['pitch','bidamount']
        widgets={
            'bidamount':forms.TextInput(attrs={'class':'form-control','id':'bidamount','placeholder':'Enter Your Proposal Amount'}),
            'pitch':forms.Textarea(attrs={'class':'form-control','id':'pitch','placeholder':'Enter Your Proposal'}),

        }