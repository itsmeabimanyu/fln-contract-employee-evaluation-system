from django import forms
from .models import Departemen, Jabatan, DataKaryawan
from django.utils import timezone

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
        fields = ['nama_jabatan', 'level']

        labels = {
            'nama_jabatan': 'Position Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mt-2 mb-2'})
            field.widget.attrs.update({'autocomplete': 'off'})

class DataKaryawanForm(forms.ModelForm):
    class Meta:
        model = DataKaryawan
        fields = ['nik', 'nama', 'tempat_lahir', 'tanggal_lahir', 'departemen', 'jabatan', 'status_karyawan', 'tgl_mulai_kontrak', 'tgl_akhir_kontrak', 'keterangan']

        labels = {
            'nik': 'NIK',
            'nama': 'Name',
            'tempat_lahir': 'Birthplace',
            'tanggal_lahir': 'Birthdate',
            'departemen': 'Department',
            'jabatan': 'Position',
            'status_karyawan': 'Status',
            'tgl_mulai_kontrak': 'Start Date',
            'tgl_akhir_kontrak': 'End Date',
            'keterangan': 'Reason'
        }

        widgets = {
            'departemen': forms.Select(attrs={'class': 'form-select'}),
            'jabatan': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'
            
            if field_name in ['tgl_mulai_kontrak', 'tgl_akhir_kontrak']:
                field.widget.attrs['class'] = 'form-control datepicker'
            elif field_name == 'tanggal_lahir':
                field.widget.attrs['class'] = 'form-control bdatepicker'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'