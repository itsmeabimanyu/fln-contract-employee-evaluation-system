from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class Departemen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_departemen = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_departemen
    
    def soft_delete(self):
        self.deleted_at = timezone.now()  # Set waktu penghapusan
        self.save()

    class Meta:
        ordering = ['nama_departemen']

class Jabatan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_jabatan = models.CharField(max_length=255)
    level = models.PositiveIntegerField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_jabatan
    
    def soft_delete(self):
        self.deleted_at = timezone.now()  # Set waktu penghapusan
        self.save()

    class Meta:
        ordering = ['nama_jabatan']  # ascending

class DataKaryawan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nik = models.IntegerField()
    nama = models.CharField(max_length=255)
    tempat_lahir = models.CharField(max_length=255)
    tanggal_lahir = models.DateField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama
    
    def soft_delete(self):
        self.deleted_at = timezone.now()  # Set waktu penghapusan
        self.save()

class MasaKontrak(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    karyawan = models.ForeignKey('DataKaryawan', on_delete=models.CASCADE, related_name='masa_kontrak')
    departemen = models.ForeignKey(Departemen, on_delete=models.CASCADE)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    status_karyawan = models.CharField(
        max_length=20,
        choices=[
            ('contract', 'CONTRACT'),
            ('intern', 'INTERN'),
        ],
        default='kontrak'
    )
    tgl_mulai_kontrak = models.DateField()
    tgl_akhir_kontrak = models.DateField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.karyawan.nama} ({self.tgl_mulai_kontrak} - {self.tgl_akhir_kontrak})"

    class Meta:
        ordering = ['tgl_mulai_kontrak']

    def soft_delete(self):
        self.deleted_at = timezone.now()  # Set waktu penghapusan
        self.save()
    
class KategoriPenilaian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_kategori = models.CharField(max_length=255)
    bobot_nilai = models.PositiveIntegerField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nama_kategori']

    def __str__(self):
        return f"{self.nama_kategori} ({self.bobot_nilai})"
    
    def soft_delete(self):
        self.deleted_at = timezone.now()  # Set waktu penghapusan
        self.save()

class Pertanyaan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kategori = models.ForeignKey(KategoriPenilaian, on_delete=models.CASCADE)
    teks_pertanyaan = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teks_pertanyaan

    def soft_delete(self):
        self.deleted_at = timezone.now()  # Set waktu penghapusan
        self.save()
    
class Jawaban(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pertanyaan = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    teks_jawaban = models.CharField(max_length=255)
    poin = models.DecimalField(max_digits=5, decimal_places=2)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teks_jawaban

    def soft_delete(self):
        self.deleted_at = timezone.now()  # Set waktu penghapusan
        self.save()
    
    class Meta:
        ordering = ['poin']
    
"""
class HasilPenilaian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    karyawan = models.ForeignKey(DataKaryawan, on_delete=models.CASCADE)
    pertanyaan = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    jawaban = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.karyawan.nama} - {self.pertanyaan.nama_pertanyaan}"
"""

class KategoriPerJabatan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.CASCADE)
    kategori = models.ManyToManyField(KategoriPenilaian, related_name='kategori')
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()  # Set waktu penghapusan
        self.save()

    def __str__(self):
        if self.pk:  # pastikan objek sudah disimpan
            kategori_names = ", ".join([f"{k.nama_kategori} ({k.bobot_nilai})" for k in self.kategori.all()])
            return f"{self.jabatan} - [{kategori_names}]"

class HasilPenilaian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    karyawan = models.ForeignKey(DataKaryawan, on_delete=models.CASCADE)
    jawaban = models.ForeignKey(Jawaban, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

""" Note. Custom kategori Absensi """
class DataAbsensiSementara(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nik = models.CharField(max_length=50)
    keterangan = models.CharField(max_length=100)