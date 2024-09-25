from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms

# Create your views here.

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Info has been updated!!!")
            return redirect('ecommercial:home')

        return render(request, "ecommercial/update_info.html", {"form": form})
    else:
        messages.success(request, "You Must be Logged In to Access That Page!!!")
        return redirect('ecommercial:home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form.
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated!')
                # login(request, current_user)
                return redirect('ecommercial:login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('ecommercial:update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, "ecommercial/update_password.html", {'form': form})
    else:
        messages.success(request, "You Must be Logged in to Access That Page!!!")
        return redirect('ecommercial:home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Profile has been updated!!!")
            return redirect('ecommercial:home')

        return render(request, "ecommercial/update_user.html", {"user_form": user_form})
    else:
        messages.success(request, "You Must be Logged in to Access That Page!!!")
        return redirect('ecommercial:home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'ecommercial/category_summary.html', {"categories": categories})

def category(request, foo):
    # Replace Hyphens with spaces.
    #foo = foo.replace("-", " ")
    # Grab the category from the url.
    try:
        # Look up the Category.
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'ecommercial/category.html', {'products': products, 'category': category})

    except:
        messages.success(request, 'This Category Does not Exist')
        return redirect('ecommercial/home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'ecommercial/product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'ecommercial/home.html', {'products': products})


def about(request):
    return render(request, 'ecommercial/about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('ecommercial:home')
        else:
            messages.success(request, 'The username and password do not match!')
            return redirect('ecommercial:login')

    else:
        return render(request, 'ecommercial/login.html', {} )


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out.'))
    return redirect("ecommercial:home")


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login user.
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Username created successfully- Please fill in your user info below...'))
            return redirect('ecommercial:update_info')
        else:
            messages.success(request, ('There was a problem during the registration, please try again!.'))
            return redirect('ecommercial:register')
    else:
        return render(request, 'ecommercial/register.html', {'form':form})


def search(request):
    return render(request, 'ecommercial/search.html', {})
