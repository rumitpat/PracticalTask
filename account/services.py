import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .froms import UserRegisterForm
from cwp.constants import ACCOUNT_REGISTER_SUCCESS, ACCOUNT_MODEL_BACKEND, \
    ACCOUNT_LOGIN_SUCCESS, ACCOUNT_LOGIN_FAILED, ACCOUNT_LOGIN_PAGE, \
    ACCOUNT_USER_PROFILE_SUCCESS
logger = logging.getLogger('info_log')


class RegisterService:

    @staticmethod
    def get_context_data():
        return {
            'user_form': UserRegisterForm(),
        }

    @staticmethod
    def is_forms_valid(request, template_name):
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, ACCOUNT_REGISTER_SUCCESS)
            print(user)
            print(user.email)
            logger.info(f'Registered new user. email: {user.email}')
            return redirect('login')
        return render(request, template_name, context={
            'user_form': user_form
        })


class LoginService:
    def __init__(self, request):
        self.request = request

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        if user := authenticate(username=username, password=password):
            login(self.request, user, backend=ACCOUNT_MODEL_BACKEND)
            messages.success(self.request, ACCOUNT_LOGIN_SUCCESS)
            return redirect('home')
        logger.error('Unwanted authentication error in authenticate()')
        messages.error(self.request, ACCOUNT_LOGIN_FAILED)
        return render(self.request, template_name=ACCOUNT_LOGIN_PAGE, context={'form': form})


class UserProfileService:
    def __init__(self, request):
        self.request = request

    def form_valid(self, form):
        form.save()
        messages.success(self.request, ACCOUNT_USER_PROFILE_SUCCESS)
        return redirect('profile')

    def get_form_kwargs(self, **kwargs):
        kwargs['instance'] = self.request.user
        return kwargs

    @staticmethod
    def get_context_data(context, request):
        user_profile_image = request.user.get_profile_pic()
        context.update(
            {'user_profile_image': user_profile_image})
        return context
