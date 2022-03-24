from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
from django.urls import reverse_lazy
from account.models import USER

from account.forms import RegistrationForm, AccountAuthenticationForm

# Create your views here.
def profile_view(request, *args, **kwargs):
	context = {}
	user_id = request.user.id
	try:
		account = USER.objects.get(pk=user_id)
	except USER.DoesNotExist :
		return HttpResponse("Error 404")

	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['bio'] = account.bio

	context['BASE_URL'] = settings.BASE_URL

	return render(request,"account/profile.html",context)


class Custom_Password_Change(PasswordChangeView):
	@property
	def success_url(self):
		return reverse_lazy('profile:password_change_done')

def profile_settings_view(request, *args, **kwargs):
	context = {}
	user_id = request.user.id
	try:
		account = USER.objects.get(pk=user_id)
	except USER.DoesNotExist :
		return HttpResponse("Error 404")
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['bio'] = account.bio
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url

	if request.POST:
		pass

	context['BASE_URL'] = settings.BASE_URL

	return render(request,"account/settings.html",context)




def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated:
		return HttpResponse("You are already authenticated as " + str(user.email))

	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)



def logout_view(request):
	logout(request)
	return redirect("home")


def login_view(request, *args, **kwargs):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")

	destination = get_redirect_if_exists(request)

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			remember_me =request.POST.get('remember_me')

			user = authenticate(email=email, password=password)

			if user:
				login(request, user)

				if not remember_me:
					request.session.set_expiry(3600)

				if destination:
					return redirect(destination)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "account/login.html", context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect


