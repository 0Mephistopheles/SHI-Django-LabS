from django import forms
from DB_Management.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'publicationyear', 'genre', 'language', 'authorid', 'publisherid']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'publicationyear': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'authorid': 'Автор',
            'publisherid': 'Видавець',
            'title': 'Назва книги'
        }