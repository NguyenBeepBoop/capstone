"""Class view for creating tags. Not commonly used especially is tag fixtures
are preloaded."""
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from tasks.forms import TagForm
from tasks.models import Tags
from braces.views import LoginRequiredMixin


class TagCreateView(LoginRequiredMixin, CreateView):
    """View for creating tags.

    Inherits:
        LoginRequiredMixin: gives site access to signed in users.
        CreateView: gives access to Django pre-built view methods.
    """
    model = Tags
    form_class = TagForm
    template_name = 'tag_create_template.html'
    success_url = reverse_lazy('tasks:tags')
    
    def get_context_data(self, **kwargs):
        """Gets the context for template rendering.

        Returns:
            Dictionary containing data needed to render variables in template.
        """
        context = super().get_context_data(**kwargs)
        context['tags'] = Tags.objects.all()
        return context