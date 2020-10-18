from django import forms

class AuctionForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control col-5 col-lg-3'}))
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'class' : 'form-control col-9 col-lg-4 entry_content h-50', 'rows':'10'}))
    price = forms.FloatField()
    image = forms.URLField()
    category = forms.CharField()


class CommentForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control col-5 col-lg-3'}))
    content = forms.CharField(
        label="Tell me waht you think...",
        widget=forms.Textarea(attrs={'class' : 'form-control col-9 col-lg-10 entry_content h-50', 'rows':'4'}))


class BidForm(forms.Form):
    price = forms.FloatField(
        label="",
        widget=forms.NumberInput(attrs={'class' : 'form-control col-7'}))

    
