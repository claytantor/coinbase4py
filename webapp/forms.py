from django import forms

class ButtonForm(forms.Form):
    payment_type = forms.ChoiceField(
        widget=forms.Select,
        label='Payment Type',
        choices=(("buy_now","Buy Now"),("donation","Donation")),
        error_messages={'required': 'Choose a payment type'}
    )
    amount = forms.FloatField(
        label='BTC Payment Amount',
        initial=0.01,
        error_messages={'required': 'A button value in BTC is required'}
    )
    description = forms.CharField(
        label='Button Description',
        initial='My Coinbase Button',
        error_messages={'required': 'Please enter a description of the button purpose'}
    )


