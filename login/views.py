from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Main login page
def main(request: HttpRequest) -> HttpResponse:
    return render(request, 'login/login.html')


# Login view
def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            print('correct')
            login(request, user)
            return redirect("/data_schemas")
        else:
            error = "Wrong username/password"
            return render(request, "login/login.html", {"error": error})
    else:
        error = ""
    #
    return render(request, "login/login.html", {"error":error})


# Logout view
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)

    return redirect('login')