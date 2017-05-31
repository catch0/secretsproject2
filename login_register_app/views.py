from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse 
from django.db.models import Count
from .models import*
def index(request):
    print "Inside the index method."
    return render(request, 'login_register_app/index.html')
def register(request):
    print "Inside the register method"
    if request.method == 'POST':
        check = User.objects.validate(request.POST)
        if check['pass']:
            user = User.objects.createUser(request.POST)
            request.session['user_id'] = user.id
            return render(request, 'login_register_app/.html')

        for error in check['errors']:
            messages.error(request, error['message'], extra_tags=error['field'])  
    return redirect('/')
def login(request):
    print "Inside the login method."
    if request.method == 'POST':
        check = User.objects.login(request.POST)
        if check['pass']:
            user = check['user']
            request.session['user_id'] = user.id
            return redirect('/juice')
        for error in check['errors']:
            messages.error(request, error['message'], extra_tags=error['field'])
    return render(request,'login_register_app/home.html')
def juice(request):
    if 'user_id' in request.session:
        user= User.objects.findUser(request.session)
        all_secrets=Secret.objects.all().order_by('-id')[:10]
        all_content=[]
        all_times=[]
        for secret in all_secrets:
            all_content.append(secret)
            print secret.user.id
        context = {'all':all_content, 'name': user.first_name, 'id': user.id}
        return render(request, 'login_register_app/home.html', context)
    return redirect('/')
def spill(request):
    if request.method=='POST':
        user=User.objects.findUser(request.session)
        new=Secret.objects.create(content=request.POST['content'], user=user)
    return redirect('/juice')
def delete(request, find):
    Secret.objects.filter(id=find).delete()
    return redirect('/juice')
def like(request,find):
    user=User.objects.findUser(request.session)
    secret=Secret.objects.filter(id=find).first()
    secret.liked_by.add(user)
    return redirect('/juice')
def popular(request):
    #if request.method=='POST':
    if 'user_id' in request.session:
        user= User.objects.findUser(request.session)
        pop_secrets =Secret.objects.annotate(num_likes=Count('liked_by')).order_by('-num_likes')
        all_content=[]
        all_times=[]
        for secret in pop_secrets:
            all_content.append(secret)
            print secret.user.id
            context={"all": all_content, 'name': user.first_name, 'id':user.id}
            return render(request, 'login_register_app/popular.html', context)
def back(request):
    return redirect('/juice')
def logout(request):
    if request.POST:
        request.session.clear()
        return redirect('/')






