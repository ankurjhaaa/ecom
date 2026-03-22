from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Author, Genere, Book


class AuthorInsertForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "email", "contact"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit("submit", "Add Author"))


class GenereInsertForm(forms.ModelForm):
    class Meta:
        model = Genere
        fields = ["title", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit("submit", "Add Genere"))


class BookInsertForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "price",
            "discount_price",
            "description",
            "nu_of_pages",
            "author",
            "genere",
            "cover_image",
            "edition",
            "isbn",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit("submit", "Add Book"))
