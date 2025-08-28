from django import forms
from .models import Departemen

class DepartemenForm(forms.ModelForm):
    class Meta:
        model = Departemen
        fields = ['nama_departemen']

        labels = {
            'nama_departemen': 'Department Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mt-2 mb-2'})
            field.widget.attrs.update({'autocomplete': 'off'})

        '''if field_name in ['amount_before_tax', 'total_invoice_amount', 'tax_amount']:
                field.widget.attrs.update({'class': 'form-control number-with-commas mt-2 mb-2'})

            if field_name == 'private_key':
                field.widget.attrs.update({'class': 'form-control form-select mt-2 mb-2', 'required': 'required'})

            if field_name == 'plain_text':
                field.widget.attrs.update({'readonly': 'readonly', 'style' : 'background: transparent !important; border: transparent;'})

        # Mengambil data private_key dari model PrivateKey dan mengubahnya menjadi tuple (id, private_key)
        self.fields['private_key'].choices = [
            (key.id, f"{key.private_key}") for key in PrivateKey.objects.all()
        ]'''