from django.shortcuts import render,redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ProfileForm, RequestForm
from .models import  Req
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .fusioncharts import FusionCharts
from collections import OrderedDict
# Create your views here.

def homepage(request):
    Reqs = Req.objects.all().filter(is_fulfilled=False) #make it true
    dataSource = OrderedDict()
    chartConfig = OrderedDict()
    chartConfig['caption'] = "Caption"
    chartConfig['subCaption'] = 'SubCaption'
    chartConfig['xAxisName'] = 'X-Axis'
    chartConfig['yAxisName'] = 'Y-Axis'
    chartConfig['theme'] = 'fusion'
    chartConfig['palettecolors'] = 'a6101e'
    chartConfig['usePlotGradientColor'] = 0
    dataSource['chart'] = chartConfig
    dataSource['data'] = []
    chartData = OrderedDict()
    for i in range(len(Reqs)):
        try:
            chartData[Reqs[i].req_for.profile.blood_group] += 1
        except KeyError:
            chartData[Reqs[i].req_for.profile.blood_group] = 1
        except:
            pass
    for key, value in chartData.items():
        data = dict()
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)
    column2d = FusionCharts("column2d", "ex1", "100%", "500", "chart-1", "json",
                            # The data is passed as a string in the `dataSource` as parameter.
                            dataSource)

    return render(request,'main/homepage.html',{'output':column2d.render()})

def signup(request):
    f = ProfileForm()
    f1 = UserCreationForm()
    if request.method=='POST':
        f1 = UserCreationForm(request.POST)
        f = ProfileForm(request.POST)
        if f1.is_valid() and f.is_valid():
            user = f1.save()
            profile = f.save(commit=False)
            profile.user = user
            username = f1.cleaned_data.get('username')
            password = f1.cleaned_data.get('password')
            user.set_password(password)
            profile.save()
            messages.success(request, "New account created: {username}".format(username=username))
            login(request,user)
            return redirect('main:homepage')
        else:
            for msg in f1.error_messages:
                messages.error(request, "{msg}: {form}[{msg}]".format(msg=msg,form=f1.error_messages))
            return render(request, 'main/signup.html',{'form': f,'form_user':f1})
    else:
        f1 = UserCreationForm()
        f = ProfileForm()
    return render(request, 'main/signup.html',{'form': f,'form_user':f1})

def login_(request):
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,'You have logged in as {}'.format(username))
                    return redirect('/')
                else:
                    messages.error(request, "Invalid username or password1")
            else:
                messages.error(request,'Invalid username or password2')
        form = AuthenticationForm()
        return render(request,'main/login.html',{'form':form})


def logout_(request):
    logout(request)
    messages.success(request,"You've logged out successfully!")
    return redirect('main:homepage')


def requests(request):
    if request.method == 'POST':
        f = RequestForm(request.POST)
        if f.is_valid():
            user1 = f.cleaned_data.get('username1')
            user2 = f.cleaned_data.get('username2')
            text = f.cleaned_data.get('text')
            try:
                req_by = User.objects.get(username=user1)
                req_for = User.objects.get(username=user2)
            except User.DoesNotExist:
                messages.error(request,"Username does not exist.")
                return redirect('/requests')
            req = Req()
            req.req_by = req_by
            req.req_for = req_for
            req.text = text
            req.save()
            messages.success(request,"Added")
            return redirect("main:homepage")
        else:
            messages.error(request,"Invalid field")
    f = RequestForm()
    if request.user.is_authenticated:
        return render(request, 'main/request.html', {'form':f})
    else:
        messages.error(request,"You must log in first!")
        return redirect("/login")

def donate(request):
    request_list = Req.objects.all()
    page = request.GET.get('page',1)
    paginator = Paginator(request_list,2)
    try:
        reqs = paginator.page(page)
    except PageNotAnInteger:
        reqs = paginator.page(1)
    except EmptyPage:
        reqs = paginator.page(paginator.num_pages)
    return render(request, 'main/donate.html', {'reqs': reqs})
