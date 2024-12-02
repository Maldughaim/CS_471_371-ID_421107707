from django.contrib.auth.models import User
from django import forms

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=255, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), max_length=255, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)  # Get the user instance without saving
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()  # Save the user instance
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=255)
