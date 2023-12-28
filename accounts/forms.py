from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .constants import GENDER_TYPE, ACCOUNT_TYPE
from django import forms
from .models import UserBankAccount, UserAddress

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    post_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta: 
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'birth_date', 'gender','account_type', 'street', 'city', 'post_code', 'country']
    
    def save(self, commit=True):
        user =  super().save(commit=False)
        if commit == True:
            user.save() #* saving user model data
            street = self.cleaned_data.get('street')
            city = self.cleaned_data.get('city')
            post_code = self.cleaned_data.get('post_code')
            country = self.cleaned_data.get('country')

            UserAddress.objects.create(
                user = user,
                street = street,
                city = city,
                post_code = post_code,
                country = country
            )

            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            account_type = self.cleaned_data.get('account_type')

            UserBankAccount.objects.create(
                user = user,
                account_type = account_type,
                gender = gender,
                birth_date = birth_date,
                account_no = 10000 + user.id
            )
        return user
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-2 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })

class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    post_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        # jodi user er account thake 
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserBankAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street'].initial = user_address.street
                self.fields['city'].initial = user_address.city
                self.fields['post_code'].initial = user_address.post_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserBankAccount.objects.get_or_create(user=user) 
            #* jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
            user_address, created = UserAddress.objects.get_or_create(user=user) 

            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street = self.cleaned_data['street']
            user_address.city = self.cleaned_data['city']
            user_address.post_code = self.cleaned_data['post_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
        

            
