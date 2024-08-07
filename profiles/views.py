from django.views.generic.edit import FormView

from profiles.forms import ProfileForm


# Create your views here.


class ProfileView(FormView):
    template_name = "profile.html"
    form_class = ProfileForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

