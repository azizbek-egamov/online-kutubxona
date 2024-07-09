from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import wikipedia
from django.core.paginator import Paginator
import re
import time


def check_password(password):
    pattern = r"(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"

    if re.match(pattern, password):
        return True
    else:
        return False


def uniqid(prefix="", more_entropy=False):
    m_time = time.time()
    base = "%8x%05x" % (int(m_time), int((m_time - int(m_time)) * 10000000))

    if more_entropy:
        import random

        base += "%.8f" % random.random()

    return prefix + base


# Create your views here.


def kitoblar_list(request):
    kitoblar = Kitob.objects.all()
    paginator = Paginator(kitoblar, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "p.html", {"page_obj": page_obj})


def HomePage(request):

    if request.method == "POST":
        return SearchPage(request)

    else:
        
        from django.contrib.auth.hashers import check_password
        from django.contrib.auth.models import User

        def CheckPassword(user, password):
            if check_password(password, user.password):
                return True
            else:
                return False

        try:
            user = User.objects.get(username="admin")
            password = "admin"
            CheckPassword(user, password)
        except User.DoesNotExist:
            print("User not found")
        
        all = Category.objects.all()
        down = BookDownloads.objects.filter(id=1)
        kitob = Kitob.objects.order_by("-created")
        # kitob = Kitob.objects.all()
        paginator = Paginator(kitob, 8)
        page_number = 1
        page_obj = paginator.get_page(page_number)

        kitob2 = Kitob.objects.order_by("-view")
        # kitob = Kitob.objects.all()
        paginator2 = Paginator(kitob2, 8)
        page_number2 = 1
        page_obj2 = paginator2.get_page(page_number2)

        paginator3 = Paginator(all, 3)
        page_number3 = 1
        page_obj3 = paginator3.get_page(page_number3)
        return render(
            request,
            "index.html",
            {
                "category": all if all.exists() else False,
                "kitob_soni": Kitob.objects.count(),
                "down": down,
                "books": kitob if kitob.exists() else False,
                "page_obj": page_obj,
                "page_obj2": page_obj2,
                "page_obj3": page_obj3,
            },
        )


def BooksPageSite(request):
    if request.method == "POST":
        return SearchPage(request)
    else:
        all = Category.objects.all()
        down = BookDownloads.objects.filter(id=1)
        view = request.GET.get("type")
        page_number = request.GET.get("page")
        # kitob = Kitob.objects.all()

        paginator3 = Paginator(all, 3)
        page_number3 = 1
        page_obj3 = paginator3.get_page(page_number3)
        if str(view) == "created":
            kitob = Kitob.objects.order_by("-created")
            paginator = Paginator(kitob, 8)
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                "books-page.html",
                {
                    "category": all if all.exists() else False,
                    "kitob_soni": Kitob.objects.count(),
                    "down": down,
                    "holat": view,
                    "books": kitob if kitob.exists() else False,
                    "page_obj": page_obj,
                    "page_obj3": page_obj3,
                },
            )
        elif str(view) == "view":
            kitob = Kitob.objects.order_by("-view")
            paginator = Paginator(kitob, 8)
            page_obj = paginator.get_page(page_number)
            return render(
                request,
                "books-page.html",
                {
                    "category": all if all.exists() else False,
                    "kitob_soni": Kitob.objects.count(),
                    "down": down,
                    "holat": view,
                    "books": kitob if kitob.exists() else False,
                    "page_obj": page_obj,
                    "page_obj3": page_obj3,
                },
            )
        else:
            return redirect("/books/?type=created&page=1")


def SearchPage(request):
    if request.method == "POST":
        text = request.POST.get("Search")
        results = Kitob.objects.filter(name__icontains=text)
        print(results)

        all = Category.objects.all()
        down = BookDownloads.objects.filter(id=1)

        paginator3 = Paginator(all, 3)
        page_number3 = 1
        page_obj3 = paginator3.get_page(page_number3)

        return render(
            request,
            "search.html",
            {
                "result": results,
                "results": results if results.exists() else False,
                "txt": text,
                "category": all if all.exists() else False,
                "kitob_soni": Kitob.objects.count(),
                "down": down,
                "page_obj3": page_obj3,
            },
        )
    else:
        return redirect("home")


def CategorysPage(request):
    if request.method == "POST":
        return SearchPage(request)

    else:

        category = Category.objects.all()
        paginator = Paginator(category, 3)
        page_number = 1
        page_obj3 = paginator.get_page(page_number)

        categ_paginator = Paginator(category, 6)
        page_number2 = request.GET.get("page")
        page_object = categ_paginator.get_page(page_number2)
        return render(
            request,
            "category.html",
            {
                "category": category if category.exists() else False,
                "page_obj3": page_obj3,
                "page_categ": page_object,
            },
        )


def BooksPage(request, slug):

    if request.method == "POST":
        return SearchPage(request)

    else:

        categ = Category.objects.all()
        # book = Kitob.objects.filter(category__slug=slug)
        book = get_list_or_404(Kitob, category__slug=slug)
        print(book)

        paginator3 = Paginator(categ, 3)
        page_number3 = 1
        page_obj3 = paginator3.get_page(page_number3)

        return render(
            request,
            "books.html",
            {
                "slug": slug,
                "category": categ,
                "books": book,
                "page_obj3": page_obj3,
            },
        )


def Book(request, category, slug):

    if request.method == "POST":
        # return SearchPage(request)
        if request.POST.get("comment"):
            comment = request.POST.get("comment")
            b = Kitob.objects.filter(id=slug)
            for i in b:
                Comments.objects.create(
                    user_id=request.user, book_id=i, comment=comment
                )

            return redirect(f"/book/{category}/{slug}/")
        elif request.POST.get("Search"):
            return SearchPage(request)
        else:
            redirect("home")
    else:

        categ = Category.objects.all()
        book = Kitob.objects.filter(category__slug=category)
        print(book)
        izohsoni = Comments.objects.filter(book_id__id=slug).count()
        comment = Comments.objects.order_by("-created")

        paginator3 = Paginator(categ, 3)
        page_number3 = 1
        page_obj3 = paginator3.get_page(page_number3)
        # try:
        #     for i in book:
        #         a = i.name
        #     wikipedia.set_lang("uz")
        #     haqida = wikipedia.summary(f"{a} haqida")
        # except:
        #     haqida = "Hozircha mavjud emas"

        haqida = "Ma'lumot yo'q"

        for i in book:
            t = int(i.view) + 1
            book.update(view=t)
        g = book.filter(id=slug)
        g = get_list_or_404(book, id=slug)
        u = False
        if g != False:
            for p in g:
                u = str(p.more_info).split("\n")
        return render(
            request,
            "book.html",
            {
                "haqida": haqida,
                "slug": slug,
                "categ": category,
                "category": categ,
                "bookx": book if book.exists() else False,
                "books": g,
                "disc": u,
                "izohsoni": izohsoni,
                "comment": comment if comment.exists() else False,
                "page_obj3": page_obj3,
            },
        )


def LogoutPage(request):
    logout(request)
    return redirect("home")


def LoginPage(request):
    all = Category.objects.all()

    paginator3 = Paginator(all, 3)
    page_number3 = 1
    page_obj3 = paginator3.get_page(page_number3)
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("user")
            password = request.POST.get("pass")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(
                    request,
                    "login.html",
                    {
                        "text": "Login yoki parol noto'g'ri",
                        "color": "red",
                        "v1": username,
                        "v2": password,
                        "login": "true",
                        "category": all if all.exists() else False,
                        "page_obj3": page_obj3,
                    },
                )

        return render(
            request,
            "login.html",
            {
                "text": "Kirish uchun kirish ma'lumotlarini kiriting",
                "login": "true",
                "category": all if all.exists() else False,
                "page_obj3": page_obj3,
            },
        )


def SignupPage(request):
    if request.POST.get("update"):
        return redirect("signup")
    else:
        all = Category.objects.all()

        paginator3 = Paginator(all, 3)
        page_number3 = 1
        page_obj3 = paginator3.get_page(page_number3)
        if request.user.is_authenticated:
            return redirect("home")
        else:
            if request.method == "POST":
                username = request.POST.get("username")
                lname = request.POST.get("lname")
                fname = request.POST.get("fname")
                pass1 = request.POST.get("pass1")
                pass2 = request.POST.get("pass2")
                email = request.POST.get("email")
                if pass1 == pass2:
                    if check_password(pass1) == True:
                        if User.objects.filter(username=username).exists():
                            return render(
                                request,
                                "signup.html",
                                {
                                    "text": "Ushbu user band, boshqa o'ylab toping",
                                    "color": "red",
                                    "fn": fname,
                                    "ln": lname,
                                    "em": email,
                                    "us": username,
                                    "p1": pass1,
                                    "p2": pass2,
                                    "sign": "true",
                                    "category": all if all.exists() else False,
                                    "page_obj3": page_obj3,
                                },
                            )
                        elif User.objects.filter(email=email).exists():
                            return render(
                                request,
                                "signup.html",
                                {
                                    "text": "Ushbu email band, boshqa email kiriting",
                                    "color": "red",
                                    "fn": fname,
                                    "ln": lname,
                                    "em": email,
                                    "us": username,
                                    "p1": pass1,
                                    "p2": pass2,
                                    "sign": "true",
                                    "category": all if all.exists() else False,
                                    "page_obj3": page_obj3,
                                },
                            )
                        else:
                            user = User.objects.create_user(
                                username=username, email=email, password=pass1
                            )
                            user.save()
                            login(request, user)
                            return redirect("home")
                    else:
                        return render(
                            request,
                            "signup.html",
                            {
                                "text": "Parolda kamida bitta katta harf (A-Z), bitta belgi va bitta raqam qatnashishi kerak. Minimal 8 ta belgi.",
                                "color": "red",
                                "fn": fname,
                                "ln": lname,
                                "em": email,
                                "us": username,
                                "p1": pass1,
                                "p2": pass2,
                                "sign": "true",
                                "category": all if all.exists() else False,
                                "page_obj3": page_obj3,
                            },
                        )
                else:
                    return render(
                        request,
                        "signup.html",
                        {
                            "text": "Parollar mos kelmayabdi",
                            "color": "red",
                            "fn": fname,
                            "ln": lname,
                            "em": email,
                            "us": username,
                            "p1": pass1,
                            "p2": pass2,
                            "sign": "true",
                            "category": all if all.exists() else False,
                            "page_obj3": page_obj3,
                        },
                    )
            return render(
                request,
                "signup.html",
                {
                    "text": "Ro'yxatdan o'tish uchun shaxsiy ma'lumotlaringizni kiriting",
                    "page_obj3": page_obj3,
                    "sign": "true",
                    "category": all if all.exists() else False,
                },
            )


def ShortnerPage(request, code):
    u = Shortner.objects.filter(code=code)
    if u.exists() == False:
        return HttpResponse("salom")
    else:
        for x in u:
            return render(request, "shortner.html", {"URL": x.url})


def change_password(request):
    user = User.objects.get(username="admin")
    user.set_password("admin")
    user.save()
    return redirect("home")


def EmailSend(email, username, code):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    from_email = "mmaqsad004@gmail.com"
    from_password = "spfd vubt yvgs odoj"
    to_email = f"{email}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Parolni tiklash"
    msg['From'] = 'Onlayn Kutubxona'
    msg["To"] = to_email
    user = f"{username}"

    html = f"""\
        <div style="color: black !important;">
            <h2>Salom {user}</h2>
            <p>Siz saytda parolingizni tiklash uchun so'rov yubordingiz, parolni tiklash uchun pastdagi tugma orqali saytda kiring.</p>
            <a href="http://127.0.0.1:8000/resetpassword/{code}" target="_blank" style="display: inline-block; width: 150px; height: 50px; background-color: aqua; text-align: center; line-height: 50px; text-decoration: none; color: black; font-size: 35px">Kirish</a>
        </div>
    """

    part2 = MIMEText(html, "html")

    msg.attach(part2)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        s = smtplib.SMTP(smtp_server, smtp_port)
        s.starttls()
        s.login(from_email, from_password)
        s.sendmail(from_email, to_email, msg.as_string())
        return True
    except Exception as e:
        print(e)
        return False


def PasswordResetPage(request):
    all = Category.objects.all()

    paginator3 = Paginator(all, 3)
    page_number3 = 1
    page_obj3 = paginator3.get_page(page_number3)
    if request.user.is_authenticated == False:
        if request.method == "POST":
            em = request.POST.get("email")
            email = User.objects.filter(email=em)
            s = uniqid()
            if email.exists() == True:
                for i in email:
                    try:
                        EmailSend(i.email, i.username, s)
                        ResetPassword.objects.create(user=i, code=s)
                        break
                    except Exception as e:
                        print(e)
                        return render(
                            request,
                            "reset-password.html",
                            {
                                "color": "red",
                                "sign": "true",
                                "text": "Emailga xabar yuborishda xatolik yuz berdi, iltimos keyinroq urinib ko'ring.",
                                "category": page_obj3 if page_obj3.exists() else False,
                            },
                        )
                return render(
                    request,
                    "reset-password.html",
                    {
                        "color": "red",
                        "sign": "true",
                        "text": "Parolni tiklash uchun xabar elektron pochtangizga yuborildi.",
                        "page_obj3": page_obj3,
                    },
                )
            else:
                return render(
                    request,
                    "reset-password.html",
                    {
                        "color": "red",
                        "sign": "true",
                        "text": "Siz kiritga email orqali xech kim ro'yhatdan o'tmagan.",
                        "page_obj3": page_obj3,
                    },
                )

        else:
            return render(
                request,
                "reset-password.html",
                {
                    "color": "black",
                    "sign": "true",
                    "text": "Parolingizni tiklash uchun elektron pochta manzilingizni kiriting.",
                    "page_obj3": page_obj3,
                },
            )
            
    else:
        return redirect("home")
        
def ResetPasswordConfirmPage(request, code):
    all = Category.objects.all()

    paginator3 = Paginator(all, 3)
    page_number3 = 1
    page_obj3 = paginator3.get_page(page_number3)
    
    x = ResetPassword.objects.filter(code=code)
    if request.method == "POST":
        p1 = request.POST.get("p1")
        p2 = request.POST.get("p2")
        if p1 == p2:
            user = User.objects.get(username=x[0].user.username)
            user.set_password(p2)
            user.save()
            userc = User.objects.get(email=x[0].user.email)
            ResetPassword.objects.filter(user=userc).delete()
            return redirect("home")
        else:
            return render(
                    request,
                    "reset-password-confirm.html",
                    {
                        "color": "red",
                        "sign": "true",
                        "text": f"Parollar bir biriga mos emas.",
                        "page_obj3": page_obj3,
                    },
                )
    else:
        if x.exists() == True:
            for i in x:
                return render(
                    request,
                    "reset-password-confirm.html",
                    {
                        "color": "black",
                        "sign": "true",
                        "text": f"User: {i.user.username}. Yangi parolni kiriting.",
                        "page_obj3": page_obj3,
                    },
                )
        else:
            return redirect("home")


