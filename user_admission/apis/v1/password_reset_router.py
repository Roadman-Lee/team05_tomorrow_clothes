from pyexpat.errors import messages

from allauth.account.forms import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, resolve_url, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from user_admission.models import User


class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get('email')).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'password_reset_done_fail.html')

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


# 새 비밀번호 설정
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)


# 새 비밀번호 설정 완료
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url('sign_in_and_up.html')
        return context

#
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:

                        return HttpResponse('Invalid header found.')

                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("main:homepage")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})