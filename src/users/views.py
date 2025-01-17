from django.shortcuts import render, redirect
from .forms import RegisterForm, UserUpadateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import profile
from django.contrib.auth.models import User

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            instance = User.objects.get(username = user)
            image = profile.objects.create(user=instance)
            image.save()
            messages.success(request, f'Account created by name \'{user}\', Now you can login')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form':form})
    
@login_required
def ProfileView(request):
    if request.method == 'POST':
        u_form = UserUpadateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('home')
    else:
        u_form = UserUpadateForm(instance=request.user)
        p_form = ProfileUpdateForm()
        
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'users/profile.html', context)