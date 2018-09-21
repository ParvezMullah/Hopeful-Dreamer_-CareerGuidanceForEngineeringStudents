from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from msguide.models import UserProfile
# Create your views here.


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    fields = [f.name for f in UserProfile._meta.get_fields()]
    fields.remove('email')
    template_name = "msguide/UserProfile.html"
    success_message = 'Data updated successfully.'
    success_url = '/userhome/2'

    def form_valid(self, form):
        form_valid = super(UserProfileUpdateView, self).form_valid(form)
        return form_valid
