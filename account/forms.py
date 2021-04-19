from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import AccountUser, role, WorkPlace
from django.contrib.auth import authenticate

ACCOUNT_TYPE= [
    ('admin', 'Workplace'),
    ('user', 'Single User'),
    ]
class AdminUserForm(UserCreationForm):
    first_name= forms.CharField(max_length=100, widget= forms.TextInput(
                                attrs={'class':'form-control'}))
    last_name= forms.CharField(max_length=100, widget= forms.TextInput(
                               attrs={'class':'form-control'}))
    username= forms.CharField(max_length=100, widget= forms.TextInput(
                              attrs={'class':'form-control'}))
    workplace= forms.CharField(max_length=100, widget= forms.TextInput(
                              attrs={'class':'form-control'}))
    # password = forms.CharField(max_length=32, widget=forms.PasswordInput(
    #                             attrs={'class':'form-control'})) 
    # password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(
    #                             attrs={'class':'form-control'}))
    email= forms.EmailField(widget= forms.EmailInput(
                            attrs={'class':'form-control'}))
    # account_type = forms.ChoiceField(choices=ACCOUNT_TYPE, widget=forms.RadioSelect)

    class Meta:
        model = AccountUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'workplace']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        user.role = 'AD'
        workplace = self.cleaned_data.get('workplace')
        workplace_id = WorkPlace.objects.create(name=workplace)
        user.workplace_id = workplace_id
        user.save()
        # role = self.cleaned_data.get('role')
        # org = self.cleaned_data.get('org')
        # profile = ScrummyUser()
        # profile.user = user
        # profile.role =role
        # profile.org = org
        # profile.save()

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class SingleUserForm(UserCreationForm):
    first_name= forms.CharField(max_length=100, widget= forms.TextInput(
                                attrs={'class':'form-control'}))
    last_name= forms.CharField(max_length=100, widget= forms.TextInput(
                               attrs={'class':'form-control'}))
    username= forms.CharField(max_length=100, widget= forms.TextInput(
                              attrs={'class':'form-control'}))
   
    email= forms.EmailField(widget= forms.EmailInput(
                            attrs={'class':'form-control'}))
    # account_type = forms.ChoiceField(choices=ACCOUNT_TYPE, widget=forms.RadioSelect)

    class Meta:
        model = AccountUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        user.role = 'US'
        # workplace = self.cleaned_data.get('workplace')
        # workplace_id = WorkPlace.objects.create(name=workplace)
        # user.workplace = workplace_id
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(max_length=32, label="Password", widget=forms.PasswordInput(
                               attrs={'class':'form-control'}))

    class Meta:
        model = AccountUser
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login details")

# class EditAccountUserForm(forms.ModelForm):
#     class Meta:
#         model = AccountUser
#         fields = ('first_name', 'last_name', 'username', 'role')