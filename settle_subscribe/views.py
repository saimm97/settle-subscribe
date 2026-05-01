from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from settle_subscribe.models import *
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required

@csrf_exempt
def login_page(request):

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email)
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            print("hello")
            login(request, user)
            print("correct password")
            return redirect("/dashboard")
        elif user is None:
            print("wrong password")
            messages.error(request, "Invalid Password")
            return redirect("/sign_in/")

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        user = User.objects.filter(email=email)
        if user.exists():
            messages.info(request, "Email Already Exists!")
            return redirect("/sign_up/")
        elif password == confirm_password:
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, email=email
            )
            user.set_password(password)
            user.save()
            messages.success(request, "Account created Successfully!")
            return redirect("/sign_up/")
        else:
            messages.info(request, "Account not created. Passwords don't match")

    return render(request, "signup.html")


def dashboard(request):
    if request.user.is_authenticated:
        print("user_logged in: ", request.user.id)
        total_subscriptions = UserExpenses.objects.filter(
            user_id=request.user.id
        ).count()
        upcoming_subscriptions = UserSubscriptions.objects.filter(
            user_id=request.user.id
        )

        print("User Expenses: ", total_subscriptions)
        print(
            "upcoming_subscriptions: ",
            upcoming_subscriptions.select_related("subscriptions", "user"),
        )

        return render(
            request,
            "dashboard.html",
            {
                "total_subscriptions": total_subscriptions,
                "upcoming_subscriptions": upcoming_subscriptions,
            },
        )
    else:
        messages.error(request, "You need to login Before Viewing Dashboard.")
        return redirect("login")


def subscription(request):
    if request.user.is_authenticated:
        print("user_logged in: ", request.user.id)
        all_subscriptions = UserSubscriptions.objects.filter(user_id=request.user.id)
        subscriptions = Subscriptions.objects.all()

        print(
            "upcoming_subscriptions: ",
            all_subscriptions.select_related("subscriptions", "user"),
        )
        return render(
            request,
            "subscription.html",
            {"all_subscriptions": all_subscriptions, "subscriptions": subscriptions},
        )

    else:
        messages.error(request, "You need to login Before Viewing Dashboard.")
        return redirect("login")


@login_required
def create_subscription(request):
    if request.method == "POST" and request.user.is_authenticated:
        print("request data: ", request.POST["subscription_type"])

        new_user_subscription = UserSubscriptions.objects.create(
            subscriptions_id=request.POST["subscription_type"],
            user_id=request.user.id,
            amount=request.POST["amount"],
            due_date=request.POST["due_date"],
        )
        new_user_subscription.save()
        messages.success(request, "New Subscription Created Successfully!")

        return redirect("/subscription")

    else:
        messages.error(request, "You need to login Before Viewing Dashboard.")
        return redirect("login")


@login_required
def delete_subscription(request,subscription_id):
    try:
        if request.method == 'POST':
            UserSubscriptions.objects.filter(id=subscription_id).delete()
            messages.success(request, "Subscription Deleted Successfully!")
            return redirect("/subscription")
        else:
            messages.error(request, "Something went wrong")
            return redirect("login")
    except Exception as e:        
            return e


def logout_view(request):
    logout(request)
    return render(request, "login.html")
