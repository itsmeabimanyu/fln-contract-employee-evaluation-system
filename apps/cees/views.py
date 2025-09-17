from django.shortcuts import render
from django.views.generic import (
    CreateView, TemplateView, View, ListView,
    DetailView, UpdateView
)
from .models import (
    Departemen, Jabatan, DataKaryawan,
    MasaKontrak, KategoriPenilaian, Pertanyaan,
    Jawaban, KategoriPerJabatan, DataAbsensiSementara)

from .forms import (
    DepartemenForm, JabatanForm, DataKaryawanForm,
    UpdateDataKaryawanForm, MasaKontrakForm, KategoriPenilaianForm,
    PertanyaanForm, JawabanForm, KategoriPerJabatanForm,
    ResponseForm, UploadExcelForm
)
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.
class ListDepartemen(TemplateView):
    template_name = 'pages/base_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Department'
        context['card_title'] = 'Department'
        context['formset'] = DepartemenForm
        context['buttons_action'] = f"""
            <button type="button" data-bs-toggle="modal" data-bs-target="#modal-first" class="btn btn-danger" id="delete-button" ><i class="bi bi-trash3-fill"></i>Delete Checked</button>
            """
        context['act_modal'] = {
            'Delete Checked': {
                'modal_id': f'modal-first',
                'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                'action_button': f'<button type="submit" name="action" value="delete_checked" class="btn btn-danger" id="delete-modal-button"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
            }
        }
        
        items = Departemen.objects.filter(deleted_at__isnull=True).order_by('nama_departemen')
        # Tambah tombol ke tiap baris data
        for item in items:
            item.form_update = DepartemenForm(instance=item)
            item.buttons_action = [
                f"""
                <div class="bs-component">
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button class="btn btn-sm btn-warning" type="button" data-bs-toggle='modal' data-bs-target='#modal-first-{item.id}' title="Edit"><i class="bi bi-pencil-square"></i></button>
                            <button class="btn btn-sm btn-danger" type="button" data-bs-toggle='modal' data-bs-target='#modal-second-{item.id}' title="Delete"><i class="bi bi-trash3-fill"></i></button>
                        </div>
                    </div>
                </div>
                """
                ]

            # Content modal
            item.modals_form = {
                f'Update': {
                    'modal_id': f'modal-first-{item.id}',
                    'action_button': f'<button type="submit" name="action" value="edit" class="btn btn-warning"><i class="bi bi-check-circle-fill me-2"></i>Submit</button>',
                    'icon': f'<i class="bi bi-pencil-square me-2"></i>',
                },
                f'Delete': {
                    'modal_id': f'modal-second-{item.id}',
                    'type': 'delete',
                    'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                    'action_button': f'<button type="submit" name="action" value="delete" class="btn btn-danger"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
                }
            }

        context['items'] = items
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save':
            department_names = self.request.POST.getlist('nama_departemen')

            for department_name in department_names:
                Departemen.objects.create(
                    nama_departemen=department_name
                )
            # messages.success(self.request, 'Invoice added successfully!')

        elif action == 'edit':
            item_id = request.POST.get('item_id')
            departemen = get_object_or_404(Departemen, pk=item_id)
            form = DepartemenForm(request.POST, instance=departemen)
            
            if form.is_valid():
                form.save()

        elif action == 'delete':
            item_id = self.request.POST.get('item_id')
            departemen = get_object_or_404(Departemen, pk=item_id)
            departemen.soft_delete()

        elif action == 'delete_checked':
            # Mendapatkan ID yang dipilih dari checkbox
            selected_ids = self.request.POST.getlist('select')
            
            if selected_ids:
                items = Departemen.objects.filter(id__in=selected_ids)
                for item in items:
                    item.soft_delete()

        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # messages.error(self.request, 'There was an error creating the Invoice. Please check the form and try again.')
        return response

    # Optional: You can define success_url to redirect after form submission
    '''def get_success_url(self):
        # Redirect to a specific page after a successful form submission
        return reverse_lazy('invoice_create_manual')  # Replace with the name of the URL for your list page or another page.'''

class ListJabatan(TemplateView):
    template_name = 'pages/base_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Position'
        context['card_title'] = 'Position'
        context['formset'] = JabatanForm
        context['buttons_action'] = f"""
            <button type="button" data-bs-toggle="modal" data-bs-target="#modal-first" class="btn btn-danger" id="delete-button" ><i class="bi bi-trash3-fill"></i>Delete Checked</button>
            """
        context['act_modal'] = {
            'Delete Checked': {
                'modal_id': f'modal-first',
                'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                'action_button': f'<button type="submit" name="action" value="delete_checked" class="btn btn-danger" id="delete-modal-button"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
            }
        }
        
        items = Jabatan.objects.filter(deleted_at__isnull=True).order_by('nama_jabatan')
        # Tambah tombol ke tiap baris data
        for item in items:
            item.form_update = JabatanForm(instance=item)
            item.buttons_action = [
                f"""
                <div class="bs-component">
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button class="btn btn-sm btn-warning" type="button" data-bs-toggle='modal' data-bs-target='#modal-first-{item.id}' title="Edit"><i class="bi bi-pencil-square"></i></button>
                            <button class="btn btn-sm btn-danger" type="button" data-bs-toggle='modal' data-bs-target='#modal-second-{item.id}' title="Delete"><i class="bi bi-trash3-fill"></i></button>
                        </div>
                    </div>
                </div>
                """
                ]

            # Content modal
            item.modals_form = {
                f'Update': {
                    'modal_id': f'modal-first-{item.id}',
                    'action_button': f'<button type="submit" name="action" value="edit" class="btn btn-warning"><i class="bi bi-check-circle-fill me-2"></i>Submit</button>',
                    'icon': f'<i class="bi bi-pencil-square me-2"></i>',
                },
                f'Delete': {
                    'modal_id': f'modal-second-{item.id}',
                    'type': 'delete',
                    'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                    'action_button': f'<button type="submit" name="action" value="delete" class="btn btn-danger"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
                }
            }

        context['items'] = items
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save':
            position_names = self.request.POST.getlist('nama_jabatan')
            levels = self.request.POST.getlist('level')

            for position_name, level in zip(position_names, levels):
                Jabatan.objects.create(
                    nama_jabatan=position_name,
                    level=level
                )
            # messages.success(self.request, 'Invoice added successfully!')

        elif action == 'edit':
            item_id = request.POST.get('item_id')
            departemen = get_object_or_404(Jabatan, pk=item_id)
            form = JabatanForm(request.POST, instance=departemen)
            
            if form.is_valid():
                form.save()

        elif action == 'delete':
            item_id = self.request.POST.get('item_id')
            departemen = get_object_or_404(Jabatan, pk=item_id)
            departemen.soft_delete()

        elif action == 'delete_checked':
            # Mendapatkan ID yang dipilih dari checkbox
            selected_ids = self.request.POST.getlist('select')
            
            if selected_ids:
                items = Jabatan.objects.filter(id__in=selected_ids)
                for item in items:
                    item.soft_delete()

        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # messages.error(self.request, 'There was an error creating the Invoice. Please check the form and try again.')
        return response

    # Optional: You can define success_url to redirect after form submission
    '''def get_success_url(self):
        # Redirect to a specific page after a successful form submission
        return reverse_lazy('invoice_create_manual')  # Replace with the name of the URL for your list page or another page.'''
    
class ListKaryawan(TemplateView):
    template_name = 'pages/base_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee'
        context['card_title'] = 'Employee'
        context['formset'] = DataKaryawanForm
        context['fields'] = {
            'nik': 'NIK',
            'nama': 'Name',
            'tempat_lahir': 'Birthplace',
            'tanggal_lahir': 'Birthdate',
            'departemen': 'Department',
            'jabatan': 'Position',
            'tgl_mulai_kontrak': 'Start Date',
            'tgl_akhir_kontrak': 'End Date',
            'status_karyawan': 'Status',
        }
          
        context['buttons_action'] = f"""
            <button type="button" data-bs-toggle="modal" data-bs-target="#modal-first" class="btn btn-danger" id="delete-button" ><i class="bi bi-trash3-fill"></i>Delete Checked</button>
            """
        context['act_modal'] = {
            'Delete Checked': {
                'modal_id': f'modal-first',
                'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                'action_button': f'<button type="submit" name="action" value="delete_checked" class="btn btn-danger" id="delete-modal-button"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
            }
        }
        
        items = DataKaryawan.objects.filter(deleted_at__isnull=True)
        # Tambah tombol ke tiap baris data
        for item in items:
            kontrak = MasaKontrak.objects.filter(karyawan=item.id, deleted_at__isnull=True).last()
            item.departemen = kontrak.departemen if kontrak else None
            item.jabatan = kontrak.jabatan if kontrak else None
            item.tgl_mulai_kontrak = kontrak.tgl_mulai_kontrak if kontrak else None
            item.tgl_akhir_kontrak = kontrak.tgl_akhir_kontrak if kontrak else None
            item.status_karyawan = kontrak.status_karyawan if kontrak else None

            item.form_update = DataKaryawanForm(instance=item)
            item.buttons_action = [
                f"""
                <div class="bs-component">
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button type='button' class='btn btn-sm btn-warning' onclick='window.location.href=\"{reverse('update_karyawan', args=[item.id])}\"'><i class="bi bi-pencil-square"></i></button>
                            <button class="btn btn-sm btn-danger" type="button" data-bs-toggle='modal' data-bs-target='#modal-second-{item.id}' title="Delete"><i class="bi bi-trash3-fill"></i></button>
                        </div>
                    </div>
                </div>
                """
                ]

            # Content modal
            item.modals_form = {
                f'Update': {
                    'modal_id': f'modal-first-{item.id}',
                    'action_button': f'<button type="submit" name="action" value="edit" class="btn btn-warning"><i class="bi bi-check-circle-fill me-2"></i>Submit</button>',
                    'icon': f'<i class="bi bi-pencil-square me-2"></i>',
                },
                f'Delete': {
                    'modal_id': f'modal-second-{item.id}',
                    'type': 'delete',
                    'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                    'action_button': f'<button type="submit" name="action" value="delete" class="btn btn-danger"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
                }
            }

        context['items'] = items
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save':
            ids = self.request.POST.getlist('nik')
            names = self.request.POST.getlist('nama')
            birthplaces = self.request.POST.getlist('tempat_lahir')
            birthdates = self.request.POST.getlist('tanggal_lahir')
            departments = self.request.POST.getlist('departemen')
            positions = self.request.POST.getlist('jabatan')
            employee_statuses = self.request.POST.getlist('status_karyawan')
            start_dates = self.request.POST.getlist('tgl_mulai_kontrak')
            end_dates = self.request.POST.getlist('tgl_akhir_kontrak')

            for id, name, birthplace, birthdate, department, position, employee_status, start_date, end_date in zip(ids, names, birthplaces, birthdates, departments, positions, employee_statuses, start_dates, end_dates):
                try:
                    birthdate_parsed = datetime.strptime(birthdate, "%d-%m-%Y").date()
                    start_date_parsed = datetime.strptime(start_date, "%d-%m-%Y").date()
                    end_date_parsed = datetime.strptime(end_date, "%d-%m-%Y").date()
                except ValueError as e:
                    # Kamu bisa log atau skip data yang gagal parsing
                    print(f"Format tanggal salah: {e}")
                    continue
                
                karyawan = DataKaryawan.objects.create(
                    nik=id,
                    nama=name,
                    tempat_lahir=birthplace,
                    tanggal_lahir=birthdate_parsed,
                )

                # Buat masa kontrak terkait
                MasaKontrak.objects.create(
                    departemen=get_object_or_404(Departemen, pk=department),
                    jabatan=get_object_or_404(Jabatan, pk=position),
                    karyawan=karyawan,
                    tgl_mulai_kontrak=start_date_parsed,
                    tgl_akhir_kontrak=end_date_parsed,
                    status_karyawan=employee_status
                )

        elif action == 'edit':
            item_id = request.POST.get('item_id')
            data_karyawan = get_object_or_404(DataKaryawan, pk=item_id)
            form = DataKaryawanForm(request.POST, instance=data_karyawan)
            
            if form.is_valid():
                karyawan = form.save()

                # Ambil tanggal dari POST
                start_date = request.POST.get('tgl_mulai_kontrak')
                end_date = request.POST.get('tgl_akhir_kontrak')
                employee_status = request.POST.get('status_karyawan')

                try:
                    tgl_mulai_parsed = datetime.strptime(start_date, "%d-%m-%Y").date()
                    tgl_akhir_parsed = datetime.strptime(end_date, "%d-%m-%Y").date()
                except ValueError as e:
                    print(f"Format tanggal salah: {e}")
                    # Bisa tambahkan error message ke context jika perlu
                    return

                # Cari masa kontrak terakhir (atau satu-satunya)
                kontrak = karyawan.masa_kontrak.order_by('-tgl_mulai_kontrak').first()

                if kontrak:
                    # Update kontrak yang ada
                    kontrak.tgl_mulai_kontrak = tgl_mulai_parsed
                    kontrak.tgl_akhir_kontrak = tgl_akhir_parsed
                    kontrak.status_karyawan = employee_status
                    kontrak.save()
                else:
                    # Jika belum ada kontrak, buat baru
                    MasaKontrak.objects.create(
                        karyawan=karyawan,
                        tgl_mulai_kontrak=tgl_mulai_parsed,
                        tgl_akhir_kontrak=tgl_akhir_parsed
                    )

        elif action == 'delete':
            item_id = self.request.POST.get('item_id')
            data_karyawan = get_object_or_404(DataKaryawan, pk=item_id)
            data_karyawan.soft_delete()

        elif action == 'delete_checked':
            # Mendapatkan ID yang dipilih dari checkbox
            selected_ids = self.request.POST.getlist('select')
            
            if selected_ids:
                items = DataKaryawan.objects.filter(id__in=selected_ids)
                for item in items:
                    item.soft_delete()

        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # messages.error(self.request, 'There was an error creating the Invoice. Please check the form and try again.')
        return response

    # Optional: You can define success_url to redirect after form submission
    '''def get_success_url(self):
        # Redirect to a specific page after a successful form submission
        return reverse_lazy('invoice_create_manual')  # Replace with the name of the URL for your list page or another page.'''

class UpdateKaryawan(TemplateView):
    template_name = 'pages/list.html'

    def dispatch(self, request, *args, **kwargs):
        # Ambil pk sekali dan simpan sebagai atribut instance
        pk = kwargs.get('pk')
        self.karyawan = DataKaryawan.objects.get(id=pk, deleted_at__isnull=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee Update'
        context['card_title'] = 'Employee (Update)'
        context['form'] = UpdateDataKaryawanForm(instance=self.karyawan)
        context['formset'] = MasaKontrakForm  
        context['buttons_action'] = f"""
            <button type="button" data-bs-toggle="modal" data-bs-target="#modal-first" class="btn btn-danger" id="delete-button" ><i class="bi bi-trash3-fill"></i>Delete Checked</button>
            """
        context['act_modal'] = {
            'Delete Checked': {
                'modal_id': f'modal-first',
                'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                'action_button': f'<button type="submit" name="action" value="delete_checked" class="btn btn-danger" id="delete-modal-button"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
            }
        }

        items = MasaKontrak.objects.filter(karyawan=self.karyawan, deleted_at__isnull=True)
        # Tambah tombol ke tiap baris data
        for item in items:
            item.form_update = MasaKontrakForm(instance=item)
            item.buttons_action = [
                f"""
                <div class="bs-component">
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button class="btn btn-sm btn-warning" type="button" data-bs-toggle='modal' data-bs-target='#modal-first-{item.id}' title="Edit"><i class="bi bi-pencil-square"></i></button>
                            <button class="btn btn-sm btn-danger" type="button" data-bs-toggle='modal' data-bs-target='#modal-second-{item.id}' title="Delete"><i class="bi bi-trash3-fill"></i></button>
                        </div>
                    </div>
                </div>
                """
                ]

            # Content modal
            item.modals_form = {
                f'Update': {
                    'modal_id': f'modal-first-{item.id}',
                    'action_button': f'<button type="submit" name="action" value="edit" class="btn btn-warning"><i class="bi bi-check-circle-fill me-2"></i>Submit</button>',
                    'icon': f'<i class="bi bi-pencil-square me-2"></i>',
                },
                f'Delete': {
                    'modal_id': f'modal-second-{item.id}',
                    'type': 'delete',
                    'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                    'action_button': f'<button type="submit" name="action" value="delete" class="btn btn-danger"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
                }
            }
        context['items'] = items
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save':
            departments = self.request.POST.getlist('departemen')
            positions = self.request.POST.getlist('jabatan')
            employee_statuses = self.request.POST.getlist('status_karyawan')
            start_dates = self.request.POST.getlist('tgl_mulai_kontrak')
            end_dates = self.request.POST.getlist('tgl_akhir_kontrak')

            for department, position, employee_status, start_date, end_date in zip(departments, positions, employee_statuses, start_dates, end_dates):
                try:
                    start_date_parsed = datetime.strptime(start_date, "%d-%m-%Y").date()
                    end_date_parsed = datetime.strptime(end_date, "%d-%m-%Y").date()
                except ValueError as e:
                    # Kamu bisa log atau skip data yang gagal parsing
                    print(f"Format tanggal salah: {e}")
                    continue

                MasaKontrak.objects.create(
                    departemen=get_object_or_404(Departemen, pk=department),
                    jabatan=get_object_or_404(Jabatan, pk=position),
                    karyawan=self.karyawan,
                    tgl_mulai_kontrak=start_date_parsed,
                    tgl_akhir_kontrak=end_date_parsed,
                    status_karyawan=employee_status
                )

        elif action == 'edit':
            item_id = request.POST.get('item_id')
            masa_kontrak = get_object_or_404(MasaKontrak, pk=item_id)
            form = MasaKontrakForm(request.POST, instance=masa_kontrak)
            
            if form.is_valid():
                form.save()

        elif action == 'edit_form':
            item_id = request.POST.get('item_id')
            masa_kontrak = get_object_or_404(DataKaryawan, pk=item_id)
            form = UpdateDataKaryawanForm(request.POST, instance=masa_kontrak)

            if form.is_valid():
                form.save()
                return redirect('list_karyawan')
            
        elif action == 'delete':
            item_id = self.request.POST.get('item_id')
            masa_kontrak = get_object_or_404(MasaKontrak, pk=item_id)
            masa_kontrak.soft_delete()

        elif action == 'delete_checked':
            # Mendapatkan ID yang dipilih dari checkbox
            selected_ids = self.request.POST.getlist('select')
            
            if selected_ids:
                items = MasaKontrak.objects.filter(id__in=selected_ids)
                for item in items:
                    item.soft_delete()

        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # messages.error(self.request, 'There was an error creating the Invoice. Please check the form and try again.')
        return response
    
'''
class CreateKategori(TemplateView):
    template_name = 'pages/create_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evaluation'
        context['card_title'] = 'Evaluation'
        context['kategori_form'] = KategoriPenilaianForm
        context['pertanyaan_form'] = PertanyaanForm
        context['jawaban_form'] = JawabanForm
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save':
            category = request.POST.get('nama_kategori')
            score_weight = request.POST.get('bobot_nilai')
            questions = request.POST.getlist('teks_pertanyaan')

            # print("Kategori:", category)
            # print("Bobot:", score_weight)

            kategori = KategoriPenilaian.objects.create(
                nama_kategori=category,
                bobot_nilai=score_weight
            )
            # Loop pertanyaan
            for i, question in enumerate(questions):
                # print(f"Pertanyaan {i+1}: {question}")

                # Ambil jawaban dan poin khusus pertanyaan ke-i
                jawaban_teks_list = request.POST.getlist(f'jawaban_{i}_teks[]')
                jawaban_poin_list = request.POST.getlist(f'jawaban_{i}_poin[]')

                pertanyaan = Pertanyaan.objects.create(teks_pertanyaan=question, kategori=kategori)

                for j, (teks, poin) in enumerate(zip(jawaban_teks_list, jawaban_poin_list)):
                    # print(f"  Jawaban {j+1}: {teks} (Poin: {poin})")
                    Jawaban.objects.create(pertanyaan=pertanyaan, teks_jawaban=teks, poin=poin)
        return redirect(self.request.META.get('HTTP_REFERER'))
'''

class ListKategori(TemplateView):
    template_name = 'pages/base_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evaluation'
        context['card_title'] = 'Evaluation'
        context['formset'] = KategoriPenilaianForm
        context['buttons_action'] = f"""
            <button type="button" data-bs-toggle="modal" data-bs-target="#modal-first" class="btn btn-danger" id="delete-button" ><i class="bi bi-trash3-fill"></i>Delete Checked</button>
            """
        context['dis_add_row'] = True
        
        context['act_modal'] = {
            'Delete Checked': {
                'modal_id': f'modal-first',
                'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                'action_button': f'<button type="submit" name="action" value="delete_checked" class="btn btn-danger" id="delete-modal-button"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
            }
        }

        items = KategoriPenilaian.objects.filter(deleted_at__isnull=True)
        for item in items:
            item.buttons_action = [
                f"""
                <div class="bs-component">
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button type='button' class='btn btn-sm btn-warning' onclick='window.location.href=\"{reverse('update_kategori', args=[item.id])}\"'><i class="bi bi-pencil-square"></i></button>
                            <button class="btn btn-sm btn-danger" type="button" data-bs-toggle='modal' data-bs-target='#modal-second-{item.id}' title="Delete"><i class="bi bi-trash3-fill"></i></button>
                        </div>
                    </div>
                </div>
                """
                ]
            
            # Content modal
            item.modals_form = {
                f'Delete': {
                    'modal_id': f'modal-second-{item.id}',
                    'type': 'delete',
                    'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                    'action_button': f'<button type="submit" name="action" value="delete" class="btn btn-danger"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
                }
            }

        context['items'] = items
        context['btn_group'] = f"""<button class='btn btn-info btn-sm' type='button' onclick='window.location.href=\"{reverse('create_kategori')}\"'><i class="bi bi-journal-plus"></i> New Form</button>"""
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'delete':
            item_id = self.request.POST.get('item_id')
            data_kategori = get_object_or_404(KategoriPenilaian, pk=item_id)
            data_kategori.soft_delete()

            for pertanyaan in Pertanyaan.objects.filter(kategori=data_kategori, deleted_at__isnull=True):
                pertanyaan.soft_delete()

                for jawaban in Jawaban.objects.filter(pertanyaan=pertanyaan, deleted_at__isnull=True):
                    jawaban.soft_delete()

        elif action == 'delete_checked':
            # Mendapatkan ID yang dipilih dari checkbox
            selected_ids = self.request.POST.getlist('select')
            if selected_ids:
                items = KategoriPenilaian.objects.filter(id__in=selected_ids)
                for item in items:
                    item.soft_delete()
                    for pertanyaan in Pertanyaan.objects.filter(kategori=item, deleted_at__isnull=True):
                        pertanyaan.soft_delete()
                        for jawaban in Jawaban.objects.filter(pertanyaan=pertanyaan, deleted_at__isnull=True):
                            jawaban.soft_delete()

        return redirect(self.request.META.get('HTTP_REFERER'))
 
class CreateKategori(TemplateView):
    template_name = 'pages/create_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evaluation'
        context['card_title'] = 'Evaluation'
        context['kategori_form'] = KategoriPenilaianForm
        context['pertanyaan_form'] = PertanyaanForm
        context['jawaban_form'] = JawabanForm

        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action == 'save':
            category = request.POST.get('nama_kategori')
            score_weight = request.POST.get('bobot_nilai')
            questions = request.POST.getlist('teks_pertanyaan')

            # print("Kategori:", category)
            # print("Bobot:", score_weight)

            kategori = KategoriPenilaian.objects.create(
                nama_kategori=category,
                bobot_nilai=score_weight
            )
            # Loop pertanyaan
            for i, question in enumerate(questions):
                # print(f"Pertanyaan {i+1}: {question}")

                # Ambil jawaban dan poin khusus pertanyaan ke-i
                jawaban_teks_list = request.POST.getlist(f'jawaban_{i}_teks[]')
                jawaban_poin_list = request.POST.getlist(f'jawaban_{i}_poin[]')

                pertanyaan = Pertanyaan.objects.create(teks_pertanyaan=question, kategori=kategori)

                for j, (teks, poin) in enumerate(zip(jawaban_teks_list, jawaban_poin_list)):
                    # print(f"  Jawaban {j+1}: {teks} (Poin: {poin})")
                    Jawaban.objects.create(pertanyaan=pertanyaan, teks_jawaban=teks, poin=poin)

        return redirect(self.request.META.get('HTTP_REFERER'))

class UpdateKategori(TemplateView):
    template_name = 'pages/create_category.html'

    def dispatch(self, request, *args, **kwargs):
        # Ambil pk sekali dan simpan sebagai atribut instance
        pk = kwargs.get('pk')
        self.kategori = KategoriPenilaian.objects.get(id=pk, deleted_at__isnull=True)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evaluation'
        context['card_title'] = 'Evaluation (Update)'
        context['kategori_form'] = KategoriPenilaianForm(instance=self.kategori)
        context['pertanyaan_form'] = PertanyaanForm
        context['jawaban_form'] = JawabanForm

        # Ambil semua pertanyaan terkait kategori ini
        pertanyaan_terkait = Pertanyaan.objects.filter(kategori=self.kategori, deleted_at__isnull=True)
        for item in pertanyaan_terkait:
            item.pertanyaan_form = PertanyaanForm(instance=item, prefix=f'pertanyaan-{item.id}')
            jawaban_list = Jawaban.objects.filter(pertanyaan=item, deleted_at__isnull=True)
            '''item.jawaban_form = [
                JawabanForm(
                    initial={
                        'teks_jawaban': jawaban.teks_jawaban,
                        'poin': jawaban.poin
                    },
                    prefix=f'jawaban-{jawaban.id}'
                )
                for jawaban in jawaban_list
            ]'''
            item.jawaban_form = [
                JawabanForm(
                    instance=jawaban,
                    prefix=f'jawaban-{jawaban.id}'
                )
                for jawaban in jawaban_list
            ]

        context['items'] = pertanyaan_terkait
        return context
    
    def post(self, request, *args, **kwargs):
        
        action = request.POST.get('action')
        if action == 'save':

            # 1. Hapus jawaban
            deleted_jawaban_ids = request.POST.getlist('deleted_jawaban_ids')
            if deleted_jawaban_ids:
                for jawaban in Jawaban.objects.filter(id__in=deleted_jawaban_ids):
                    jawaban.soft_delete()

            # 2. Hapus pertanyaan dan jawaban terkait
            deleted_pertanyaan_ids = request.POST.getlist('deleted_pertanyaan_ids')
            if deleted_pertanyaan_ids:
                for pertanyaan in Pertanyaan.objects.filter(id__in=deleted_pertanyaan_ids):
                    pertanyaan.soft_delete()
                    # Soft delete semua jawaban yang terkait
                    for jawaban in Jawaban.objects.filter(pertanyaan=pertanyaan):
                        jawaban.soft_delete()

            # 3. Simpan form kategori
            kategori_form = KategoriPenilaianForm(request.POST, instance=self.kategori)
            if kategori_form.is_valid():
                kategori_form.save()
            else:
                return redirect(self.request.META.get('HTTP_REFERER'))
            
            # 4. Update pertanyaan & jawaban existing
            pertanyaans = Pertanyaan.objects.filter(kategori=self.kategori, deleted_at__isnull=True)
            for pertanyaan in pertanyaans:
                prefix = f'pertanyaan-{pertanyaan.id}'
                p_form = PertanyaanForm(request.POST, instance=pertanyaan, prefix=prefix)

                if p_form.is_valid():
                    p_form.save()
                else:
                    return redirect(self.request.META.get('HTTP_REFERER'))

                # Update jawaban existing
                jawaban_list = Jawaban.objects.filter(pertanyaan=pertanyaan, deleted_at__isnull=True)
                for jawaban in jawaban_list:
                    jawaban_prefix = f'jawaban-{jawaban.id}'
                    j_form = JawabanForm(request.POST, instance=jawaban, prefix=jawaban_prefix)
                    
                    if j_form.is_valid():
                        j_form.save()
                        print(f"Jawaban {jawaban.id} saved successfully.")
                    else:
                        print(f"Jawaban {jawaban.id} form errors:", j_form.errors)

                # Tambah jawaban baru (yang tidak punya ID)
                new_jawaban_teks = request.POST.getlist(f'jawaban-{pertanyaan.id}-teks[]')
                new_jawaban_poin = request.POST.getlist(f'jawaban-{pertanyaan.id}-poin[]')
                print(new_jawaban_poin)

                for teks_jawaban, poin in zip(new_jawaban_teks, new_jawaban_poin):
                    # Lewati jika teks kosong
                    if not teks_jawaban.strip():
                        continue

                    try:
                        poin_int = int(poin)
                    except (ValueError, TypeError):
                        poin_int = 0

                    Jawaban.objects.create(
                        pertanyaan=pertanyaan,
                        teks_jawaban=teks_jawaban.strip(),
                        poin=poin_int
                    )

            # 5. Tambah pertanyaan baru (dan jawaban baru)
            new_questions = request.POST.getlist('teks_pertanyaan')
            for i, teks in enumerate(new_questions):
                # Simpan pertanyaan
                pertanyaan = Pertanyaan.objects.create(
                    kategori=self.kategori,
                    teks_pertanyaan=teks
                )

                # Ambil jawaban terkait berdasarkan index
                jawaban_teks_list = request.POST.getlist(f'jawaban_{i}_teks[]')
                jawaban_poin_list = request.POST.getlist(f'jawaban_{i}_poin[]')
                for teks_jawaban, poin in zip(jawaban_teks_list, jawaban_poin_list):
                    Jawaban.objects.create(
                        pertanyaan=pertanyaan,
                        teks_jawaban=teks_jawaban,
                        poin=poin
                    )
            
            return redirect(self.request.META.get('HTTP_REFERER'))

# Note:* disini add row dimatikan karena belum fix untuk input beberapa row  (next pakai formset)
# Note: Hapus permanen
class ListKategoriPerJabatan(TemplateView):
    template_name = 'pages/base_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evaluation'
        context['card_title'] = 'Evaluation (Assign Category)'
        context['formset'] = KategoriPerJabatanForm
        context['buttons_action'] = f"""
            <button type="button" data-bs-toggle="modal" data-bs-target="#modal-first" class="btn btn-danger" id="delete-button" ><i class="bi bi-trash3-fill"></i>Delete Checked</button>
            """
        
        context['act_modal'] = {
            'Delete Checked': {
                'modal_id': f'modal-first',
                'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                'action_button': f'<button type="submit" name="action" value="delete_checked" class="btn btn-danger" id="delete-modal-button"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
            }
        }
        
        context['dis_add_row'] = True
        context['fields'] = {
            'jabatan': 'Position',
            'kategori_list': 'Category'
        }
        
        items = KategoriPerJabatan.objects.filter(deleted_at__isnull=True)

        # Tambah tombol ke tiap baris data
        for item in items:
            item.buttons_action = [
                f"""
                <div class="bs-component">
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button class="btn btn-sm btn-warning" type="button" data-bs-toggle='modal' data-bs-target='#modal-first-{item.id}' title="Edit"><i class="bi bi-pencil-square"></i></button>
                            <button class="btn btn-sm btn-danger" type="button" data-bs-toggle='modal' data-bs-target='#modal-second-{item.id}' title="Delete"><i class="bi bi-trash3-fill"></i></button>
                        </div>
                    </div>
                </div>
                """
                ]
            
            item.kategori_list = ", ".join([f"{k.nama_kategori} ({k.bobot_nilai})" for k in item.kategori.all()])

            item.form_update = KategoriPerJabatanForm(instance=item)
            
            # Content modal
            item.modals_form = {
                f'Update': {
                    'modal_id': f'modal-first-{item.id}',
                    'action_button': f'<button type="submit" name="action" value="edit" class="btn btn-warning"><i class="bi bi-check-circle-fill me-2"></i>Submit</button>',
                    'icon': f'<i class="bi bi-pencil-square me-2"></i>',
                },
                f'Delete': {
                    'modal_id': f'modal-second-{item.id}',
                    'type': 'delete',
                    'icon' : '<i class="bi bi-trash-fill me-2"></i>',
                    'action_button': f'<button type="submit" name="action" value="delete" class="btn btn-danger"><i class="bi bi-check-circle-fill me-2"></i>Delete</button>',
                }
            }

        context['items'] = items
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')

        if action == 'save':
            form = KategoriPerJabatanForm(request.POST)
            if form.is_valid():
                jabatan = form.cleaned_data['jabatan']
                # Cek apakah jabatan sudah ada
                if KategoriPerJabatan.objects.filter(jabatan=jabatan, deleted_at__isnull=True).exists():
                    messages.error(request, f'Jabatan "{jabatan}" sudah memiliki entri.')
                else:
                    form.save()
                    messages.success(request, 'Data berhasil disimpan.')

        elif action == 'edit':
            item_id = request.POST.get('item_id')
            kategori_jabatan = get_object_or_404(KategoriPerJabatan, pk=item_id)
            form = KategoriPerJabatanForm(request.POST, instance=kategori_jabatan)
            if form.is_valid():
                jabatan = form.cleaned_data['jabatan']
                # Cek apakah jabatan sudah ada di entri lain
                if KategoriPerJabatan.objects.filter(jabatan=jabatan, deleted_at__isnull=True).exclude(pk=kategori_jabatan.pk).exists():
                    messages.error(request, f'Jabatan "{jabatan}" sudah memiliki entri.')
                else:
                    form.save()
                    messages.success(request, 'Data berhasil diperbarui.')

        elif action == 'delete':
            item_id = self.request.POST.get('item_id')
            kategori_jabatan = get_object_or_404(KategoriPerJabatan, pk=item_id)
            kategori_jabatan.soft_delete()

        elif action == 'delete_checked':
            # Mendapatkan ID yang dipilih dari checkbox
            selected_ids = self.request.POST.getlist('select')
            
            if selected_ids:
                items = KategoriPerJabatan.objects.filter(id__in=selected_ids)
                for item in items:
                    item.soft_delete()

        return redirect(self.request.META.get('HTTP_REFERER'))
    
class ListPenilaianKaryawan(TemplateView):
    template_name = 'pages/base_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee Evaluation'
        context['card_title'] = 'Employee Evaluation'
        context['fields'] = {
            'nik': 'NIK',
            'nama': 'Name',
            'tempat_lahir': 'Birthplace',
            'tanggal_lahir': 'Birthdate',
            'departemen': 'Department',
            'jabatan': 'Position',
            'tgl_mulai_kontrak': 'Start Date',
            'tgl_akhir_kontrak': 'End Date',
            'status_karyawan': 'Status',
        }

        items = MasaKontrak.objects.filter(deleted_at__isnull=True)
        for item in items:
            item.nik = item.karyawan.nik
            item.nama = item.karyawan.nama
            item.tempat_lahir = item.karyawan.tempat_lahir
            item.tanggal_lahir = item.karyawan.tanggal_lahir

            item.buttons_action = [
                f"""
                <div class="bs-component">
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button type='button' class='btn btn-sm btn-warning' onclick='window.location.href=\"{reverse('create_penilaian_karyawan', args=[item.id])}\"'><i class="bi bi-pencil-square"></i></button>
                            <button class="btn btn-sm btn-danger" type="button" data-bs-toggle='modal' data-bs-target='#modal-second-{item.id}' title="Delete"><i class="bi bi-trash3-fill"></i></button>
                        </div>
                    </div>
                </div>
                """
                ]

        context['items'] = items

        return context
    
class CreatePenilaianKaryawan(TemplateView):
    template_name = 'pages/create_evaluation.html'

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.masakontrak = MasaKontrak.objects.get(id=pk, deleted_at__isnull=True)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = ResponseForm(jabatan=self.masakontrak.jabatan)
        context = self.get_context_data(**kwargs)
        context['formset'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee Evaluation'
        context['card_title'] = 'Employee Evaluation'
        context['fields'] = {
            'nik': 'NIK',
            'nama': 'Name',
            'tempat_lahir': 'Birthplace',
            'tanggal_lahir': 'Birthdate',
            'departemen': 'Department',
            'jabatan': 'Position',
            'tgl_mulai_kontrak': 'Start Date',
            'tgl_akhir_kontrak': 'End Date',
            'status_karyawan': 'Status',
        }
        items = MasaKontrak.objects.filter(id=self.masakontrak.id, deleted_at__isnull=True)
        for item in items:
            item.nik = item.karyawan.nik
            item.nama = item.karyawan.nama
            item.tempat_lahir = item.karyawan.tempat_lahir
            item.tanggal_lahir = item.karyawan.tanggal_lahir

        context['items'] = items
        return context

import pandas as pd
import json
from django.utils.safestring import mark_safe
class UploadExcelAbsensi(TemplateView):
    template_name = 'pages/create_attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Import Attendance'
        context['card_title'] = 'Import Attendance'
        context['formset'] = UploadExcelForm
        context['dis_add_row'] = True
        return context
    
    def post(self, request, *args, **kwargs):
        form = UploadExcelForm(request.POST, request.FILES)
        context = self.get_context_data()

        # Step 1: Upload Excel 
        if form.is_valid():
            excel_file = request.FILES['file']

            try:
                df = pd.read_excel(excel_file)

                allowed_keterangan = [
                    "cuti potong gaji", 
                    "datang terlambat", 
                    "datang tidak absen", 
                    "pulang cepat"
                ]

                keterangan_list = df.iloc[:, 7].astype(str).str.lower().str.strip()

                if not keterangan_list.isin(allowed_keterangan).all():
                    context['error'] = "Gagal: Terdapat keterangan tidak valid di file yang diunggah."
                    # return render(request, self.template_name, context)

                # Ambil kolom 1 dan 12 kalau cukup kolom
                if df.shape[1] >= 12:
                    kolom_nik = df.iloc[:, 0]
                    kolom_nama = df.iloc[:, 1]
                    kolom_keterangan = df.iloc[:, 7]
                    kolom_tanggal_masuk = df.iloc[:, 9]
                    kolom_jam_masuk = df.iloc[:, 10]
                    kolom_tanggal_keluar = df.iloc[:, 11]
                    kolom_jam_keluar = df.iloc[:, 12]

                    '''
                    print("Isi Kolom 1 (NIK):")
                    for nik in kolom_nik:
                        print(nik)

                    print("\nIsi Kolom 8:")
                    for keterangan in kolom_keterangan:
                        print(keterangan)
                    '''

                    items = []
                    for nik, nama, ket, tgl_in, jam_in, tgl_out, jam_out in zip(
                        kolom_nik, kolom_nama, kolom_keterangan,
                        kolom_tanggal_masuk, kolom_jam_masuk,
                        kolom_tanggal_keluar, kolom_jam_keluar
                    ):
                        # absen_masuk = f"{tgl_in} {jam_in}".strip()
                        # absen_keluar = f"{tgl_out} {jam_out}".strip()

                        items.append({
                            'kolom_nik': str(nik),
                            'kolom_nama': str(nama),
                            'kolom_keterangan': str(ket),
                            # 'absen_masuk': str(absen_masuk),
                            # 'absen_keluar': str(absen_keluar),
                            'tgl_absen_masuk': str(tgl_in),
                            'jam_absen_masuk': str(jam_in),
                            'tgl_absen_keluar': str(tgl_out),
                            'jam_absen_keluar': str(jam_out),
                        })

                    # Simpan sementara ke session
                    request.session['uploaded_items'] = items

                    context['items'] = items
                    context['fields'] = {
                        'kolom_nik': 'NIK',
                        'kolom_nama': 'Employee Name',
                        'kolom_keterangan': 'Reason',
                        # 'absen_masuk': 'Actual Date Time In',
                        # 'absen_keluar': 'Actual Date Time Out',
                        'tgl_absen_masuk': 'Actual Date In',
                        'jam_absen_masuk': 'Actual Time In',
                        'tgl_absen_keluar': 'Actual Date Out',
                        'jam_absen_keluar': 'Actual Time Out',
                    }

                    context['success'] = True

            except Exception as e:
                context['error'] = f"Gagal membaca file Excel: {e}"

        # Step 2: Confirm Simpan ke DB
        if 'confirm' in request.POST:
            items = request.session.get('uploaded_items')
            
            if items:
                DataAbsensiSementara.objects.all().delete()
                for item in items:
                    DataAbsensiSementara.objects.create(
                        nik=item['kolom_nik'],
                        # nama=item['kolom_nama'],
                        keterangan=item['kolom_keterangan'],
                        # absen_masuk=item['absen_masuk'],
                        # absen_keluar=item['absen_keluar'],
                    )
                context['success'] = "Data berhasil disimpan ke database."
            else:
                context['error'] = "Tidak ada data untuk disimpan."

            return redirect(self.request.META.get('HTTP_REFERER'))
                
        return render(request, self.template_name, context)

    
    
