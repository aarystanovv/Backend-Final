from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.views import View

from .models import *
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.db import connection
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User



# Create your views here.
def about(request):
    admin = Admins.objects.all()
    products = Products.objects.all()
    return render(request, 'about.html', {'products':products, 'admin':admin})

def account(request):
    return render(request, 'account.html')

def cart(request):
    car = Cart.objects.all()
    return render(request, 'cart.html', {'car':car})

def product(request):
    products = Products.objects.all()
    return render(request, 'products.html', {'product':products})

def support(request):
    return render(request, 'support.html')

def home(request):
    admin = Admins.objects.all()
    products = Products.objects.all()
    return render(request, 'home.html', {'products':products, 'admin':admin})

def details(request, id):
    data = Details.objects.filter(id=id)
    prod = Products.objects.all()
    com = Comments.objects.filter(to_id=id)
    c = Details.objects.filter(id=id)
    return render(request, 'product-details.html', {'data':data, 'prod':prod, 'com':com, 'c':c})

@csrf_exempt
def comm(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        to_id = request.POST['to_id']
        if form.is_valid():
            try:
                form.save()
                return redirect('/details/' + str(to_id))
            except:
                pass
    return redirect('/products/')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        login = request.POST['login']
        em = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['ver_pass']
        email_subject = 'User activation'
        email_body = render_to_string('active.html')
        email = EmailMessage(subject=email_subject, body=email_body,
                             from_email='210103082@stu.sdu.edu.kz',
                             to=[em])
        if pass1 == pass2:
            if Users.objects.filter(login=login).exists():
                print("login name already used")
                return redirect('/')
            else:
                if form.is_valid():
                    try:
                        form.save()
                        print("user created")

                        email.send()
                        return redirect('/home/')
                    except:
                        pass

        else:
            print("invalid password")
            return redirect('/')
    return redirect('/')

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        form = UsersLog(request.POST)
        login = request.POST['login']
        password = request.POST['password']
        data = Users.objects.filter(login=login)
        for q in data:
            if q.password == password:
                return redirect('/products/')
    return redirect('/')

def delete(request, id):
    com = Comments.objects.get(id=id)
    to = com.to_id
    com.delete()
    return redirect("/details/" + str(to))

def edit(request, id):
    com = Comments.objects.get(id=id)
    return render(request, 'edit.html', {'com': com})

@csrf_exempt
def update(request, id):
    id = int(id)
    try:
        post_sel = Comments.objects.get(id=id)
    except Comments.DoesNotExist:
        return redirect('/products/')
    post_form = CommentForm(request.POST or None, instance=post_sel)
    if post_form.is_valid:
        post_form.save()
        return redirect('/products/')
    products = Products.objects.all()
    return render(request, 'products.html', {'product': products})


def admins(request, post_slug):
    post = get_object_or_404(Admins, slug=post_slug)
    context = {'post': post}
    return render(request, 'admins.html', context=context)


@csrf_exempt
def cart_buy(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        pr_id = request.POST['pr_id']
        if form.is_valid():
            try:
                form.save()
                return redirect('/details/' + str(pr_id))
            except:
                pass
    return redirect('/products/')

def dele(request, id):
    com = Cart.objects.get(id=id)
    com.delete()
    return redirect("/cart/")


def AdminUser(request):
    return render(request, 'AdminUser.html')


def allForClients(request):
    context = {
        "allForClientsItems": Products.objects.all()
    }
    return render(request, 'allForClients.html', context)


def all(request):
    context = {
        "allForClientsItems": Products.objects.all()
    }
    return render(request, 'all.html', context)

def allUsers(request):
    context = {
        "allForUsers": User.objects.all()
    }
    return render(request, 'allUsers.html', context)


def insert(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/all")
    else:
        form = ProductsForm()
    return render(request, 'media.html', {'form': form})


def insertUsers(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/allUsers")
    else:
        form = CustomerRegistrationForm()
    return render(request, 'insertUserMedia.html', {'form': form})


def allEdit(request):
    context = {
        "allForClientsItems": Products.objects.all()
    }
    return render(request, 'allEdit.html', context)




def updateItems(request, pk):
    if pk is not None:
        items = get_object_or_404(Products, pk=pk)
    else:
        items = None

    if request.method == "POST":
        form = ProductsForm(request.POST, instance=items)
        if form.is_valid():
            updated_items = form.save()
            return render(request, "AdminUser.html")
    else:
        form = ProductsForm(instance=items)

    return render(request, "Update.html",
                  {"form": form, "instance": items, "model_type": "Item"})

def deleteItems(request, pk=None):
    context = {}
    if pk is not None:
        items = get_object_or_404(Products, pk=pk)
    else:
        items = None

    if  request.method == "POST":
        items.delete()
        return HttpResponseRedirect('/allForClients')

    return render(request,'delete.html', context)


def profile(request):
    return render(request, 'profile1.html')

def edit1(request, pk):
    context = {}
    obj = get_object_or_404(User, pk=pk)
    form = CustomerRegistrationForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return render(request, 'home.html')
    context["form"] = form

    return render(request, "edit1.html", context)



def UU(request):
    context = {
        "allForUsers": User.objects.all()
    }
    return render(request, 'UU.html', context)


def updateOnlyUser(request, pk=None):
    context = {}
    if pk is not None:
        user = get_object_or_404(User, pk=pk)
    else:
        user = None

    if  request.method == "POST":
        user.delete()
        return HttpResponseRedirect('/allUsers')

    return render(request,'delete.html', context)


def detail(request, id):
    context = {}
    context["data"] = Products.objects.get(id=id)
    data = Products.objects.get(id=id)

    if request.user.is_authenticated:
        max_viewed_item_length = 10
        viewed_items = request.session.get('viewed_items', [])
        viewed_item = data.id, data.name
        if viewed_item in viewed_items:
            viewed_items.pop(viewed_items.index(viewed_item))
        viewed_items.insert(0, viewed_item)
        viewed_items = viewed_items[:max_viewed_item_length]
        request.session['viewed_items'] = viewed_items

    return render(request, "detail.html", context)


def search_books(request):
    name = request.GET.get('name', "")
    data = Products.objects.all().filter(name__contains=name).values()
    template = loader.get_template('search.html')

    context = {
        'data' : data,
        'name' : name
    }
    return render(request, "search.html", context)



def item_list(request):
    sort_option = request.GET.get('sort', 'asc')
    query = request.GET.get('q')

    if query and sort_option == 'asc':
        items = Products.objects.filter(name__icontains=query)
        items = items.order_by('price')

    elif query and sort_option == 'desc':
        items = Products.objects.filter(name__icontains=query)
        items = items.order_by('-price')
    else:
        items = Products.objects.all()

    if sort_option == 'asc':
        items = items.order_by('price')
    elif sort_option == 'desc':
        items = items.order_by('-price')


    return render(request, 'allForClients.html', {'items': items, 'sort_option': sort_option, 'query': query})



from django.shortcuts import render, HttpResponse
import wikipedia


# Create your views here.
def wiki(request):
    if request.method == "POST":
        search = request.POST['search']
        try:
            result = wikipedia.summary(search, sentences=20) # No of sentences that you want as output
        except:
            return HttpResponse("Wrong Input")
        return render(request, "wiki.html", {"result": result})
    return render(request, "wiki.html")


def contactsendmail(request):
    if request.method == "GET":
        form = contactformemail()
    else:
        form = contactformemail(request.POST)
        if form.is_valid():
            frommail = form.cleaned_data['fromemail']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, frommail, ['ttt.arystan@gmail.com', frommail])
    return render(request, 'Contactpage.html', {'form': form})


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "category.html", locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "category.html", locals())

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "productdetail.html", locals())