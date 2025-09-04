from django.shortcuts import redirect
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('list_departemen')),
    path('master/department/', views.ListDepartemen.as_view(), name='list_departemen'),
    path('master/position/', views.ListJabatan.as_view(), name='list_jabatan'),
    path('master/employee/', views.ListKaryawan.as_view(), name='list_karyawan'),
    path('master/employee/update/<uuid:pk>/', views.UpdateKaryawan.as_view(), name='update_karyawan'),
    path('master/form/category/', views.CreateKategori.as_view(), name='create_kategori'),
    path('master/form/evaluation-category/', views.ListKategori.as_view(), name='list_kategori'),
    path('master/form/evaluation-category/update/<uuid:pk>', views.UpdateKategori.as_view(), name='update_kategori'),
]

# Tambahkan register/ hanya jika dalam mode DEBUG (development)
'''if settings.DEBUG:
    urlpatterns += [
        # Register
        path('register/', views.RegisterAccount.as_view(), name='register'), # *Untuk testing non ldap (disable saat produksi)
    ]'''

# Media file hanya disajikan saat development (DEBUG=True)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)