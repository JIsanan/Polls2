from django import forms


class Comment(forms.Form):
    comment = forms.CharField(max_length=5000)
