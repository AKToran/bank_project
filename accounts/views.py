from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from transactions.views import send_transaction_email


class UserRegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    #* reverse_lazy loads the page when clicked on the link not before. This function returns a lazy object, which is not evaluated until it's actually needed.

    def form_valid(self, form): 
        user = form.save()
        login(self.request, user)
        return super().form_valid(form) #* form_valid call hobe jodi sob thik thake
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
        return render(request, self.template_name, {'form': form})
    
class PasswordUpdateView(PasswordChangeView, LoginRequiredMixin):
    template_name = 'accounts/passchange.html'

    def form_valid(self, form):
        messages.success(self.request, 'Changed password successfully.')
        send_transaction_email(self.request.user, 0, "Changed Password", 'accounts/passchange_mail.html')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profile') 
   
