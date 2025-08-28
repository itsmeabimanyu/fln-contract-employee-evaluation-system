from django.shortcuts import render
from django.views.generic import (
    CreateView, TemplateView, View, ListView,
    DetailView, UpdateView
)
from .models import Departemen
from .forms import DepartemenForm
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
class ListDepartemen(TemplateView):
    template_name = 'pages/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Department'
        context['card_title'] = 'Department'
        context['form'] = DepartemenForm
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
        
        items = Departemen.objects.filter(deleted_at__isnull=True)
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
