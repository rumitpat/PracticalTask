from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from .froms import UserUpdateForm, ProfileUpdateForm
from .services import RegisterService
from cwp.constants import ACCOUNT_REGISTER_PAGE


class RegisterView(View):
    """
    description: This is user register view.
    GET request will display Register Form in register.html page.
    POST request will make user registered if details is valid else register
    form with error is displayed.
    """
    template_name = ACCOUNT_REGISTER_PAGE

    def get(self, request):
        context = RegisterService.get_context_data()
        return render(request, RegisterView.template_name, context=context)

    def post(self, request):
        return RegisterService.is_forms_valid(request=request, template_name=RegisterView.template_name)


class UserProfileView(View):
    pass


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'account/profile.html', context)
