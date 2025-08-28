from django import forms
from .models import Departemen, Jabatan

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

class JabatanForm(forms.ModelForm):
    class Meta:
        model = Jabatan
        fields = ['nama_jabatan']

        labels = {
            'nama_jabatan': 'Position Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mt-2 mb-2'})
            field.widget.attrs.update({'autocomplete': 'off'})