from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
from django.urls import reverse_lazy
from account.models import USER

from movie.views import convert_TMDB_to_id,get_movie,get_movie_info,save_movie
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

import json

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
		context['profile_image']=account.profile_image.url
		context['favorites'] = []
		if account.favorite:
			for favorite in account.favorite:
				try:
					_ = get_movie(int(favorite))
				except:
					_ = get_movie_info(int(favorite))
					save_movie(favorite, _)
					_ = get_movie(favorite)
				context['favorites'].append(_)

	context['BASE_URL'] = settings.BASE_URL

	return render(request,"account/profile.html",context)


class Custom_Password_Change(PasswordChangeView):
	@property
	def success_url(self):
		return reverse_lazy('profile:password_change_done')

def profile_settings_view(request, *args, **kwargs):
	account = USER.objects.get(id=request.user.id)
	form = AccountUpdateForm(instance=account)
	if request.method == 'POST':
		form = AccountUpdateForm(request.POST, instance=account)
		if form.is_valid():
			form.save()
			return redirect('profile:edit')
	return render(request, 'account/settings.html', {'form': form})

def profile_delete(request):
	if request.user.is_authenticated:
		if request.POST:
			id = request.user.id
			try:
				logout(request)
				USER.objects.get(id=id).delete()
				return redirect("home")
			except USER.DoesNotExist:
				return HttpResponse('Error 404')
		else:
			return render(request, 'account/delete.html')



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


def add_favorite(request,movieid, *args, **kwargs):
	user_id = request.user.id
	if request.POST:
		try:
			favorite = USER.objects.get(pk=user_id).favorite
			if favorite:
				if movieid in favorite:
					return HttpResponse('Already Exist')
				else:
					favorite.append(movieid)
			else:
				favorite = [movieid]
			USER.objects.filter(pk=user_id).update(favorite=favorite)
		except USER.DoesNotExist :
			return HttpResponse("Error 404")
		return HttpResponse(json.dumps({"status":"Added","movieid":movieid}), content_type="application/json")
	return HttpResponse('Error 404')


def remove_favorite(request,movieid, *args, **kwargs):
	user_id = request.user.id
	if request.POST:
		try:
			favorite = USER.objects.get(pk=user_id).favorite
			if favorite:
				if movieid in favorite:
					favorite.remove(movieid)
				else:
					return HttpResponse('Movie Not Found')
			else:
				return HttpResponse('Favorite List Empty')
			USER.objects.filter(pk=user_id).update(favorite=favorite)
		except USER.DoesNotExist :
			return HttpResponse("Error 404")
		return HttpResponse(json.dumps({"status":"Removed","movieid":movieid}), content_type="application/json")
	return HttpResponse('Error 404')


