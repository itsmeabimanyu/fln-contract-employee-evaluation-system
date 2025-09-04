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
    id = models.AutoField(primary_key=True)
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
        return self.nama_kategori

class Pertanyaan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kategori = models.ForeignKey(KategoriPenilaian, on_delete=models.CASCADE)
    teks_pertanyaan = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teks_pertanyaan
    
class Jawaban(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pertanyaan = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    teks_jawaban = models.CharField(max_length=255)
    poin = models.PositiveIntegerField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teks_jawaban
    
"""
class HasilPenilaian(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    karyawan = models.ForeignKey(DataKaryawan, on_delete=models.CASCADE)
    pertanyaan = models.ForeignKey(Pertanyaan, on_delete=models.CASCADE)
    jawaban = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.karyawan.nama} - {self.pertanyaan.nama_pertanyaan}"
"""

