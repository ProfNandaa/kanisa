from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from kanisa.forms.documents import DocumentForm, DocumentFormSimple
from kanisa.models import Document
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaDeleteView)


class DocumentBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Storing documents on your site allows people to have '
                   'easy access to the files they need.')
    kanisa_root_crumb = {'text': 'Documents',
                         'url': reverse_lazy('kanisa_manage_documents')}
    permission = 'kanisa.manage_documents'
    kanisa_nav_component = 'documents'


class DocumentIndexView(DocumentBaseView,
                        KanisaListView):
    model = Document
    queryset = Document.objects.all()

    template_name = 'kanisa/management/documents/index.html'
    kanisa_title = 'Manage Documents'
    kanisa_is_root_view = True
    paginate_by = 20
document_management = DocumentIndexView.as_view()


class DocumentCreateView(DocumentBaseView,
                         KanisaCreateView):
    kanisa_title = 'Upload a Document'
    success_url = reverse_lazy('kanisa_manage_documents')

    def get_form_class(self):
        if self.is_popup():
            return DocumentFormSimple
        return DocumentForm
document_create = DocumentCreateView.as_view()


class DocumentUpdateView(DocumentBaseView,
                         KanisaUpdateView):
    form_class = DocumentForm
    model = Document
    success_url = reverse_lazy('kanisa_manage_documents')
document_update = DocumentUpdateView.as_view()


class DocumentDeleteView(DocumentBaseView,
                         KanisaDeleteView):
    model = Document

    def get_cancel_url(self):
        return reverse('kanisa_manage_documents')

    def get_success_url(self):
        message = '%s deleted.' % self.object
        messages.success(self.request, message)
        return reverse('kanisa_manage_documents')
document_delete = DocumentDeleteView.as_view()
