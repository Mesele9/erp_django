from django import forms

class RatingForm(forms.Form):
    guest_name = forms.CharField(
        label="Your Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    stars = forms.ChoiceField(
        label="Rating",
        choices=[(i, f"{i} Stars") for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    comment = forms.CharField(
        label="Comment",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )