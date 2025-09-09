from django.shortcuts import render
from django.views.generic import (
    CreateView, TemplateView, View, ListView,
    DetailView, UpdateView
)
from .models import Departemen, Jabatan, DataKaryawan, MasaKontrak, KategoriPenilaian, Pertanyaan, Jawaban
from .forms import DepartemenForm, JabatanForm, DataKaryawanForm, UpdateDataKaryawanForm, MasaKontrakForm, KategoriPenilaianForm, PertanyaanForm, JawabanForm
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from django.urls import reverse, reverse_lazy

# Create your views here.
class ListDepartemen(TemplateView):
    template_name = 'pages/create.html'

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
            print(selected_ids)
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
    template_name = 'pages/create.html'

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
            print(selected_ids)
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
    template_name = 'pages/create.html'

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
            print(selected_ids)
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
            print(selected_ids)
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
    template_name = 'pages/create_evaluation.html'

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
    template_name = 'pages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evaluation'
        context['card_title'] = 'Evaluation'
        context['formset'] = KategoriPenilaianForm
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
        context['items'] = items
        return context
    
'''
class UpdateKategori(TemplateView):
    template_name = 'pages/update_evaluation.html'

    def dispatch(self, request, *args, **kwargs):
        # Ambil pk sekali dan simpan sebagai atribut instance
        pk = kwargs.get('pk')
        self.kategori = KategoriPenilaian.objects.get(id=pk, deleted_at__isnull=True)
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Evaluation'
        context['card_title'] = 'Evaluation'
        context['kategori_form'] = KategoriPenilaianForm(instance=self.kategori)
        context['pertanyaan_form'] = PertanyaanForm
        context['jawaban_form'] = JawabanForm

        # Ambil semua pertanyaan terkait kategori ini
        pertanyaan_terkait = Pertanyaan.objects.filter(
            kategori=self.kategori, deleted_at__isnull=True
        )

        # Cara 1
        """
        pertanyaan_forms = []
        for item in pertanyaan_terkait:
            pertanyaan_forms.append({
                'form': PertanyaanForm(instance=item),
                'jawaban_list': Jawaban.objects.filter(pertanyaan=item, deleted_at__isnull=True)
            })

        context['pertanyaan_forms'] = pertanyaan_forms
        """

        Cara 2
        context['pertanyaan_forms'] = [
            {
                'form_pertanyaan': PertanyaanForm(instance=pertanyaan),
                # 'jawaban_list': Jawaban.objects.filter(pertanyaan=pertanyaan, deleted_at__isnull=True)
                'jawaban_forms': [
                    JawabanForm(instance=jawaban)
                    for jawaban in Jawaban.objects.filter(pertanyaan=pertanyaan, deleted_at__isnull=True)
                ],

                'buttons_action' : [
                f"""
                <div class="bs-component">
                    <div class="btn-group" role="group" aria-label="Basic example">
                        <div class="btn-group" role="group" aria-label="Basic example">
                            <button class="btn btn-sm btn-danger" type="button" data-bs-toggle='modal' data-bs-target='#modal-second-{pertanyaan.id}' title="Delete"><i class="bi bi-trash3-fill"></i></button>
                        </div>
                    </div>
                </div>
                """
                ]
            }
            for pertanyaan in pertanyaan_terkait
        ]

        # Pertanyaan dan jawaban sebagai initial (bukan lewat form Django langsung)
        # context['pertanyaan_terkait'] = Pertanyaan.objects.filter(kategori=self.kategori, deleted_at__isnull=True).prefetch_related('jawaban_set')
        return context
'''

class CreateKategori(TemplateView):
    template_name = 'pages/create_evaluation.html'

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
    template_name = 'pages/create_evaluation.html'

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
            kategori_form = KategoriPenilaianForm(request.POST, instance=self.kategori)
            if kategori_form.is_valid():
                kategori_form.save()
            else:
                return redirect(self.request.META.get('HTTP_REFERER'))
            
            # Update existing pertanyaan & jawaban
            pertanyaans = Pertanyaan.objects.filter(kategori=self.kategori, deleted_at__isnull=True)
            for pertanyaan in pertanyaans:
                prefix = f'pertanyaan-{pertanyaan.id}'
                p_form = PertanyaanForm(request.POST, instance=pertanyaan, prefix=prefix)

                if p_form.is_valid():
                    p_form.save()
                else:
                    return redirect(self.request.META.get('HTTP_REFERER'))

                # Update jawaban untuk pertanyaan ini
                jawaban_list = Jawaban.objects.filter(pertanyaan=pertanyaan, deleted_at__isnull=True)
                for jawaban in jawaban_list:
                    jawaban_prefix = f'jawaban-{jawaban.id}'
                    j_form = JawabanForm(request.POST, instance=jawaban, prefix=jawaban_prefix)
                    
                    if j_form.is_valid():
                        j_form.save()
                        print(f"Jawaban {jawaban.id} saved successfully.")
                    else:
                        print(f"Jawaban {jawaban.id} form errors:", j_form.errors)

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


    

    