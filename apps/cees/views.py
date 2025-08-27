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
        
        '''
        context['act_modal'] = {
            'Delete Item': {
                'modal_id': f'modal-first',
                'action_button': f'<button type="submit" name="action" value="delete" class="btn btn-danger" id="delete-modal-button">Delete</button>',
            }
        }
        
        # context['additionals_button'] = f"<button type='button' class='btn ms-2 btn-secondary' onclick='window.location.href=\"{reverse('key_create')}\"'><i class='fa fa-plus me-2'></i>Private Key</button>"
        
        # Tambah tombol ke tiap baris data
        for item in items:
            item.form_update = DepartemenForm(instance=item)
            item.buttons_action = [
                f"<button type='button' data-bs-toggle='modal' data-bs-target='#modal-first-{item.id}' class='btn btn-danger w-100'><i class='fas fa-trash me-2'></i>Delete</button>"
                f"<button type='button' data-bs-toggle='modal' data-bs-target='#modal-second-{item.id}' class='mt-1 btn btn-info w-100' id='' ><i class='fas fa-pen me-2'></i>Edit</button>"
                ]

            # Content modal
            item.modals_form = {
                'Delete Item': {
                    'modal_id': f'modal-first-{item.id}',
                    'action_button': f'<button type="submit" name="action" value="delete_one" class="btn btn-danger">Delete</button>',
                    'info': f'<p class="fw-bolder text-secondary">Invoice {item.invoice_number}</p>'
                },
                'Update Item': {
                    'modal_id': f'modal-second-{item.id}',
                    'action_button': f'<button type="submit" name="action" value="edit" class="btn btn-secondary">Submit</button>',
                    'info': (
                        f"""<p class="text-muted mb-1">
                        <label>Created by:</label><br>
                        {item.created_by}<br>
                        <small>{item.created_at.strftime("%d-%m-%Y %H:%M")}</small>
                        </p>"""
                    )
                }
            }

        
        '''
        items = Departemen.objects.all()
        context['items'] = items
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('action') == 'save':
            department_names = self.request.POST.getlist('nama_departemen')

            for department_name in department_names:
                Departemen.objects.create(
                    nama_departemen=department_name
                )

            # messages.success(self.request, 'Invoice added successfully!')

        return redirect(self.request.META.get('HTTP_REFERER'))

    def form_invalid(self, form):
        response = super().form_invalid(form)
        # messages.error(self.request, 'There was an error creating the Invoice. Please check the form and try again.')
        return response

    # Optional: You can define success_url to redirect after form submission
    '''def get_success_url(self):
        # Redirect to a specific page after a successful form submission
        return reverse_lazy('invoice_create_manual')  # Replace with the name of the URL for your list page or another page.'''
