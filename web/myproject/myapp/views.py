from django.shortcuts import render, redirect
from .forms import RegisterForm, FileUploadForm, UserForm, LoginForm
from .models import Register, FileUpload, User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def mainpage(request):
    user = request.user
    context = {'user':user}
    return render(request, 'mainpage.html', context)

def register(request):
    regiform = RegisterForm
    if request.method == 'POST':
        regiform = RegisterForm(request.POST)
        if regiform.is_valid():
            if len(regiform.cleaned_data['VIN']) != 17:
                messages.info(request, '차대번호 17자리를 정확하게 입력해주세요.')
            elif len(regiform.cleaned_data['MAC']) != 12:
                messages.info(request, 'MAC주소 12자리를 정확하게 입력해주세요.')
            elif len(regiform.cleaned_data['tel']) not in [12, 13] or regiform.cleaned_data['tel'].count('-') != 2:
                messages.info(request, '연락처 12자리 또는 13자리를 -를 포함하여 정확하게 입력해주세요.')
            else:
                regiform.save()  
                return redirect('mainpage')
        else:
            messages.info(request, '이미 등록된 정보입니다. 다시 확인해 주세요')

    context = {'regiform':regiform}
    return render(request, 'register.html', context)

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loginform'] = LoginForm
        return context

    def form_valid(self, form):
        user = form.get_user()
        auth.login(self.request, user)
        return redirect('mainpage')

def signup(request):
    user = request.user
    if user.is_authenticated:
        auth.logout(request)

    if request.method == 'POST':
        signup_form = UserForm(request.POST)
        if signup_form.is_valid():
            print("JJJJJJJJ")
            user = signup_form.save()
            auth.login(request, user)
            return redirect('mainpage')
    else:
        signup_form = UserForm()
    
    return render(request, 'registration/signup.html', {'signup_form':signup_form})

def userfile(request):
    if request.method == 'POST':
        fileform = FileUploadForm(request.POST, request.FILES)  # Do not forget to add: request.FILES
        if fileform.is_valid():
            # 저장
            fileform.save()
            return redirect('foruser')

    fileform = FileUploadForm()
    context = {'fileform':fileform}
    return render(request, 'userfile.html', context)

@login_required
def polifile(request):
    if request.method == 'POST':
        fileform = FileUploadForm(request.POST, request.FILES)  # Do not forget to add: request.FILES
        if fileform.is_valid():
            # 저장
            fileform.save()
            return redirect('forpoli')

    fileform = FileUploadForm()
    context = {'fileform':fileform}
    return render(request, 'polifile.html', context)

def foruser(request):
    try:
        # 읽기
        myfileitem = FileUpload.objects.last()
        data = myfileitem.myfile.file.read()
        data = data.decode("utf-8")
        # 삭제
        myfileitem.delete()  
        # 가공
        datas = data.split('\r\n/')
        infos = Register.objects.all()

        # 1. 내 차량
        mycarstr = datas[0]
        del datas[0]
        mycar = infos.filter(MAC=mycarstr).get()

        # 2. 사고 단위
        accidents = []
        for item in datas:
            acci = []
            item = item.split('\r\n')
            acci.append(item[0]) # 사고시간
            del item[0]

            carcount = 0
            for carmac in item:
                if infos.filter(MAC=carmac).get() is not None:
                    carcount += 1
            acci.append(carcount)
            accidents.append(acci)

        context = {'mycar':mycar, 'accidents':accidents}
    except:
        return redirect('error')

    return render(request, 'foruser.html', context)

@login_required
def forpoli(request):
    try:
        # 읽기
        myfileitem = FileUpload.objects.last()
        data = myfileitem.myfile.file.read()
        data = data.decode("utf-8")
        # 삭제
        myfileitem.delete()  
        # 가공
        datas = data.split('\r\n/')
        infos = Register.objects.all()

        # 1. 내 차량
        mycarstr = datas[0]
        del datas[0]
        mycar = infos.filter(MAC=mycarstr).get()
        print(mycar.VIN, mycar.name)

        # 2. 사고 단위
        accidents = []
        for item in datas:
            acci = []
            item = item.split('\r\n')
            acci.append(item[0]) # 사고시간
            del item[0]

            carinfo = []
            for carmac in item:
                info = infos.filter(MAC=carmac).get()
                carinfo.append((info.VIN, info.name, info.tel))
            acci.append(carinfo)
            accidents.append(acci)

        context = {'mycar':mycar, 'accidents':accidents}
    except:
        return redirect('error')

    return render(request, 'forpoli.html', context)

def error(request):
    return render(request, 'error.html')