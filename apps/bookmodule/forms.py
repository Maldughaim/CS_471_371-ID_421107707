from django import forms
from .models import Book,Address,Student,Student2, Address2, Images

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'edition', 'price']

class StudentForm(forms.ModelForm):
    address = forms.ModelChoiceField(
        queryset=Address.objects.all().order_by('city'),
        empty_label="Select an Address",)

    class Meta:
        model = Student
        fields = ['name', 'age', 'address']

class StudentForm2(forms.ModelForm):
    addresses = forms.ModelMultipleChoiceField(
        queryset=Address2.objects.all().order_by('city'),
        label='Address',
        widget=forms.CheckboxSelectMultiple(),
        required=False)

    class Meta:
        model = Student2
        fields = ['name', 'age', 'addresses']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['coverPage']