from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from tasks.forms import TagForm
from tasks.models import Tags
from braces.views import LoginRequiredMixin

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tags
    form_class = TagForm
    template_name = 'tag_create_template.html'
    success_url = reverse_lazy('tasks:tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tags.objects.all()
        return context