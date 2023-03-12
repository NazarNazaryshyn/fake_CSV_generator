from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def main(request):
    return render(request, 'login/login.html')


def login_view(request):
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


def logout_view(request):
    logout(request)

    return redirect('login')