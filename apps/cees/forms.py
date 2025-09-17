from django import forms
from .models import (
    Departemen, Jabatan, DataKaryawan,
    MasaKontrak, KategoriPenilaian, Pertanyaan,
    Jawaban, KategoriPerJabatan, HasilPenilaian, DataAbsensiSementara
)

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
    departemen = forms.ModelChoiceField(
        queryset=Departemen.objects.filter(deleted_at__isnull=True),  # Filter active departemen
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Department'
    )

    jabatan = forms.ModelChoiceField(
        queryset=Jabatan.objects.filter(deleted_at__isnull=True),  # Filter active jabatan
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Position'
    )

    tgl_mulai_kontrak = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y'),
        input_formats=['%d-%m-%Y'],
        label='Start Date'
    )
    tgl_akhir_kontrak = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y'),
        input_formats=['%d-%m-%Y'],
        label='End Date'
    )

    status_karyawan = forms.ChoiceField(
        choices=MasaKontrak._meta.get_field('status_karyawan').choices,  # Ambil choices dari field status_karyawan di MasaKontrak
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='contract',
        label='Status'
    )

    class Meta:
        model = DataKaryawan
        fields = ['nik', 'nama', 'tempat_lahir', 'tanggal_lahir']

        labels = {
            'nik': 'NIK',
            'nama': 'Name',
            'tempat_lahir': 'Birthplace',
            'tanggal_lahir': 'Birthdate',
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
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

        # Prefill tanggal kontrak jika instance dan kontraknya ada
        if instance:
            kontrak = instance.masa_kontrak.order_by('-tgl_mulai_kontrak').first()
            if kontrak:
                self.fields['tgl_mulai_kontrak'].initial = kontrak.tgl_mulai_kontrak.strftime('%d-%m-%Y')
                self.fields['tgl_akhir_kontrak'].initial = kontrak.tgl_akhir_kontrak.strftime('%d-%m-%Y')

class UpdateDataKaryawanForm(forms.ModelForm):

    class Meta:
        model = DataKaryawan
        fields = ['nik', 'nama', 'tempat_lahir', 'tanggal_lahir']

        labels = {
            'nik': 'NIK',
            'nama': 'Name',
            'tempat_lahir': 'Birthplace',
            'tanggal_lahir': 'Birthdate',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'

            if field_name == 'tanggal_lahir':
                field.widget.attrs['class'] = 'form-control bdatepicker'  # Menambahkan kelas CSS
                field.widget.attrs['type'] = 'date'
                field.widget.format = '%d-%m-%Y'  # Menetapkan format tanggal untuk widget
                field.input_formats = ['%d-%m-%Y']  # Menetapkan format input untuk validasi
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class MasaKontrakForm(forms.ModelForm):
    class Meta:
        model = MasaKontrak
        fields = ['departemen', 'jabatan', 'tgl_mulai_kontrak', 'tgl_akhir_kontrak', 'status_karyawan']

        labels = {
            'departemen': 'Department',
            'jabatan': 'Position',
            'status_karyawan': 'Status',
            'tgl_mulai_kontrak': 'Start Date',
            'tgl_akhir_kontrak': 'End Date'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter departemen dan jabatan hanya yang belum dihapus (deleted_at is null)
        self.fields['departemen'].queryset = Departemen.objects.filter(deleted_at__isnull=True)
        self.fields['jabatan'].queryset = Jabatan.objects.filter(deleted_at__isnull=True)

        for field_name, field in self.fields.items():
            field.widget.attrs['autocomplete'] = 'off'

            if field_name in ['tgl_mulai_kontrak', 'tgl_akhir_kontrak']:
                field.widget = forms.DateInput(
                    format='%d-%m-%Y',
                    attrs={'class': 'form-control datepicker', 'type': 'text'}
                )
                field.input_formats = ['%d-%m-%Y'] 
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class KategoriPenilaianForm(forms.ModelForm):
    class Meta:
        model = KategoriPenilaian
        fields = ['nama_kategori', 'bobot_nilai']

        labels = {
            'nama_kategori': 'Category Name',
            'bobot_nilai': 'Score Weight (%)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mt-2 mb-2'})
            field.widget.attrs.update({'autocomplete': 'off'})

class PertanyaanForm(forms.ModelForm):
    class Meta:
        model = Pertanyaan
        fields = ['teks_pertanyaan']
        labels = {
            'teks_pertanyaan': 'Question Text'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control mt-2 mb-2',
                'autocomplete': 'off'
            })

class JawabanForm(forms.ModelForm):
    class Meta:
        model = Jawaban
        fields = ['teks_jawaban', 'poin']
        labels = {
            'teks_jawaban': 'Answer Text',
            'poin': 'Point'
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'teks_jawaban':
                field.widget.attrs.update({
                    'placeholder': 'Enter the answer text here...',
                    'class': 'form-control jawaban-teks',
                    'autocomplete': 'off'
                })
            elif field_name == 'poin':
                field.widget.attrs.update({
                    'placeholder': 'Enter point value...',
                    'class': 'form-control jawaban-poin',
                    'autocomplete': 'off'
                })

class KategoriPerJabatanForm(forms.ModelForm):
    class Meta:
        model = KategoriPerJabatan
        fields = ['jabatan', 'kategori']
        widgets = {
            'kategori': forms.CheckboxSelectMultiple(),  # atau forms.SelectMultiple()
        }

        labels = {
            'jabatan': 'Position',
            'kategori': 'Category'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pastikan instance sudah ada dan punya id
        instance_id = getattr(self.instance, 'id', None)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'

            # Ganti id HTML berdasarkan instance
            if instance_id:
                field.widget.attrs['id'] = f'{field_name}_{instance_id}'

class ResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.jabatan = kwargs.pop('jabatan', None)
        super().__init__(*args, **kwargs)

        pertanyaan_list = [
            ('tanpa absen', 'dtg tanpa abesn')
        ]

        for field_name, label in pertanyaan_list:
            self.fields[field_name] = forms.IntegerField(
                label = label,
                min_value=0,
                required=True
            )

        self.kategori_data = []  # untuk akses di template

        if self.jabatan:
            # Ambil kategori yang terkait jabatan
            kategori_ids = KategoriPerJabatan.objects.filter(jabatan=self.jabatan, deleted_at__isnull=True).values_list('kategori__id', flat=True)
            kategori_queryset = KategoriPenilaian.objects.filter(id__in=kategori_ids, deleted_at__isnull=True)

            for kategori in kategori_queryset:
                questions = Pertanyaan.objects.filter(kategori=kategori, deleted_at__isnull=True)

                pertanyaan_fields = []

                for question in questions:
                    jawaban_qs = Jawaban.objects.filter(pertanyaan=question, deleted_at__isnull=True)
                    choices = [(str(j.id), j.teks_jawaban) for j in jawaban_qs]

                    field_name = f"question_{question.id}"
                    self.fields[field_name] = forms.ChoiceField(label=f"{kategori.nama_kategori} - {question.teks_pertanyaan}", choices=choices, widget=forms.RadioSelect, required=True)

                    pertanyaan_fields.append({
                        'field_name': field_name,
                        'question_text': question.teks_pertanyaan,
                        'choices': choices,
                    })

                self.kategori_data.append({
                    'kategori_nama': f"{kategori.nama_kategori} ({kategori.bobot_nilai}%)",
                    'pertanyaan': pertanyaan_fields,
                })


        """ Note. Custom kategori Absensi """
        
        self.kategori_data = []

        kategori_absensi_queryset = KategoriPenilaian.objects.filter(
            nama_kategori="KEHADIRAN", deleted_at__isnull=True
        )

        for kategori in kategori_absensi_queryset:
            attendance_questions = Pertanyaan.objects.filter(
                kategori=kategori, deleted_at__isnull=True
            )
            pertanyaan_fields = []

            for question in attendance_questions:
                jawaban_qs = Jawaban.objects.filter(pertanyaan=question, deleted_at__isnull=True)
                jawaban_fields = []

                for jawaban in jawaban_qs:
                    field_name = f"question_{question.id}_jawaban_{jawaban.id}"
                    self.fields[field_name] = forms.CharField(
                        label=f"{jawaban.teks_jawaban}",
                        required=False,
                        widget=forms.TextInput(attrs={'placeholder': 'Isi nilai atau keterangan...'})
                    )

                    jawaban_fields.append({
                        'field_name': field_name,
                        'jawaban_text': jawaban.teks_jawaban,
                    })

                pertanyaan_fields.append({
                    'question_text': question.teks_pertanyaan,
                    'jawaban_fields': jawaban_fields,
                })

            self.kategori_data.append({
                'kategori_nama': f"{kategori.nama_kategori} ({kategori.bobot_nilai}%)",
                'pertanyaan': pertanyaan_fields,
            })
                
class UploadExcelForm(forms.Form):
    file = forms.FileField(
        label='Select an Excel file',
        widget=forms.FileInput(attrs={'accept': '.xls,.xlsx'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mt-2 mb-2'})
            field.widget.attrs.update({'autocomplete': 'off'})

""" Note. Custom kategori Absensi """
class AbsensiForm(forms.Form):
    title = "KEHADIRAN (20%)"

    '''
    kategori = forms.CharField(
        label="",
        max_length=100,
        initial="Kehadiran",
        widget=forms.HiddenInput()

    )

    bobot_nilai = forms.CharField(
        label="",
        max_length=100,
        initial="20",
        widget=forms.HiddenInput()

    )
    '''

    '''
    mangkir = forms.IntegerField(label="Mangkir/Absen (Potong Gaji/Cuti)", min_value=0, initial=0)
    tanpa_absen = forms.IntegerField(label="Datang/Pulang Tanpa Absen", min_value=0, initial=0)
    terlambat = forms.IntegerField(label="Terlambat", min_value=0, initial=0)
    izin_cepat = forms.IntegerField(label="Izin/Pulang Cepat", min_value=0, initial=0)
    '''

    mangkir = forms.CharField(label="Mangkir/Absen (Potong Gaji/Cuti)")
    tanpa_absen = forms.CharField(label="Datang/Pulang Tanpa Absen")
    terlambat = forms.CharField(label="Terlambat")
    izin_cepat = forms.CharField(label="Izin/Pulang Cepat")

    # Bobot nilai untuk masing-masing pelanggaran
    bobot = {
        'mangkir': 5,
        'tanpa_absen': 0.25,
        'terlambat': 0.25,
        'izin_cepat': 0.25,
    }

    def __init__(self, *args, **kwargs):
        self.karyawan = kwargs.pop('karyawan', None)
        super().__init__(*args, **kwargs)

        if self.karyawan:
            nik = str(self.karyawan.nik)  # atau self.karyawan.get('nik')

            """ Catatan:
            exact → Pencocokan harus persis sama dan case-sensitive.
            iexact → Pencocokan harus sama persis tapi case-insensitive.
            """

            count_terlambat = DataAbsensiSementara.objects.filter(
                nik=nik,
                keterangan__iexact="datang terlambat"
            ).count()

            self.fields['terlambat'].initial = count_terlambat

            count_izin_cepat = DataAbsensiSementara.objects.filter(
                nik=nik,
                keterangan__iexact="pulang cepat"
            ).count()

            self.fields['izin_cepat'].initial = count_izin_cepat

            count_dtg_tanpa_absen = DataAbsensiSementara.objects.filter(
                nik=nik,
                keterangan__iexact="datang tidak absen"
            ).count()

            count_plg_tanpa_absen = DataAbsensiSementara.objects.filter(
                nik=nik,
                keterangan__iexact="pulang tidak absen"
            ).count()

            self.fields['tanpa_absen'].initial = count_dtg_tanpa_absen + count_plg_tanpa_absen

            count_mangkir = DataAbsensiSementara.objects.filter(
                nik=nik,
                keterangan__iexact="mangkir / tanpa alasan"
            ).count()

            count_cuti_pot_gaji = DataAbsensiSementara.objects.filter(
                nik=nik,
                keterangan__iexact="cuti potong gaji"
            ).count()

            self.fields['mangkir'].initial = count_mangkir + count_cuti_pot_gaji

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mt-2 mb-2 border-0'})
            field.widget.attrs.update({'autocomplete': 'off'})
            field.widget.attrs.update({'readonly': 'readonly'})


