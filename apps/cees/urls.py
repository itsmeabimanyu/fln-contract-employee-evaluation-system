from django.shortcuts import redirect
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('list_departemen')),
    path('master/department/list', views.ListDepartemen.as_view(), name='list_departemen'),
    path('master/position/list/', views.ListJabatan.as_view(), name='list_jabatan'),
    path('master/employee/list/', views.ListKaryawan.as_view(), name='list_karyawan'),
    path('master/employee/update/<uuid:pk>/', views.UpdateKaryawan.as_view(), name='update_karyawan'),
    path('evaluation/form/', views.CreateKategori.as_view(), name='create_kategori'),
    path('evaluation/list/', views.ListKategori.as_view(), name='list_kategori'),
    path('evaluation/update/<uuid:pk>/', views.UpdateKategori.as_view(), name='update_kategori'),
    path('evaluation/assign-category/list/', views.ListKategoriPerJabatan.as_view(), name='list_mapping'),
    path('evaluation/employee/list/', views.ListPenilaianKaryawan.as_view(), name='list_penilaian_karyawan'),
    path('evaluation/form/<uuid:pk>', views.CreatePenilaianKaryawan.as_view(), name='create_penilaian_karyawan'),
    # Note. Custom kategori Absensi
    path('evaluation/import/attendance/', views.UploadExcelAbsensi.as_view(), name='upload_excel_absensi'),
    path('rangkuman/<uuid:pk>/', views.RangkumanPenilaian.as_view(), name='rangkuman'),
]

# Tambahkan register/ hanya jika dalam mode DEBUG (development)
'''if settings.DEBUG:
    urlpatterns += [
        # Register
        path('register/', views.RegisterAccount.as_view(), name='register'), # *Untuk testing non ldap (disable saat produksi)
    ]'''

# Media file hanya disajikan saat development (DEBUG=True)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)