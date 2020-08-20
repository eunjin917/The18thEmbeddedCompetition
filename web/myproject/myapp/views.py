from django.shortcuts import render, redirect
from .forms import RegisterForm, FileUploadForm, UserForm, LoginForm
from .models import Register, FileUpload, User, Accident
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
    context = {'user': user}
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
                messages.info(
                    request, '연락처 12자리 또는 13자리를 -를 포함하여 정확하게 입력해주세요.')
            else:
                regiform.save()
                return redirect('mainpage')
        else:
            messages.info(request, '이미 등록된 정보입니다. 다시 확인해 주세요')

    context = {'regiform': regiform}
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
            user = signup_form.save()
            auth.login(request, user)
            return redirect('mainpage')
    else:
        signup_form = UserForm()

    context = {'signup_form': signup_form}

    if signup_form.errors:
        for field in signup_form:
            if field.errors:
                context['error'] = field.errors
                break

    return render(request, 'registration/signup.html', context)


def fileupload(request):
    if request.method == 'POST':
        # Do not forget to add: request.FILES
        fileform = FileUploadForm(request.POST, request.FILES)
        if fileform.is_valid():
            fileform.save()
            return redirect('accidentcheck')

    fileform = FileUploadForm()
    context = {'fileform': fileform}
    return render(request, 'fileupload.html', context)


def accidentcheck(request):
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
        try:
            mycar = infos.filter(MAC=mycarstr).get()
        except:
            return redirect('error')

        # 2. 사고 단위로
        accimoum = []
        for item in datas:
            acci = []
            item = item.split('\r\n')
            time = item[0]
            del item[0]
            acci.append(time)  # 사고시간

            try: # 이미 등록돼있는 경우
                accidents = Accident.objects.filter(mycar_date=mycar.VIN+'_'+time).get()
            except: # 등록X경우 저장해서 올리기
                accidents = Accident.objects.create(
                    mycar_date=mycar.VIN+'_'+time, mycar=mycar, date=time)

                noregilst = []
                for carmac in item:
                    try:
                        info = infos.filter(MAC=carmac).get()
                        accidents.othercars.add(info)
                    except:
                        noregilst.append(carmac)
                Accident.objects.filter(mycar_date=mycar.VIN+'_'+time).update(carcount=len(item), noregicar = noregilst)
                accidents = Accident.objects.filter(mycar_date=mycar.VIN+'_'+time).get()

            accimoum.append(accidents) # 사고 객체 저장

        context = {'mycar': mycar, 'accimoum': accimoum}
    except:
        return redirect('fileupload')

    return render(request, 'accidentcheck.html', context)

@login_required
def alldata(request):
    infos = Accident.objects.all()
    search = request.GET.get('search', '')
    if search:
        infos = infos.filter(mycar_date__icontains=search)

    context = {'infos': infos, 'search': search}

    return render(request, 'alldata.html', context)


@login_required
def searchdata(request, id):
    infos = Register.objects.all()
    acci = Accident.objects.get(pk=id)
    noregicar = eval(acci.noregicar)

    # 등록안된 경우 있으면 다 찾아오기
    if noregicar is not '[]':
        noregilst = []
        for mac in noregicar:
            try:
                info = infos.filter(MAC=mac).get()
                acci.othercars.add(info)
            except:
                noregilst.append(mac)
        Accident.objects.filter(pk=id).update(noregicar = noregilst)
        acci = Accident.objects.get(pk=id)
        noregicar = eval(acci.noregicar)

    mycar = acci.mycar
    othercars = acci.othercars
    carcount = acci.carcount
    
    context = {'mycar':mycar, 'othercars': othercars, 'noregicar':noregicar, 'carcount':carcount}

    return render(request, 'searchdata.html', context)


def error(request):
    return render(request, 'error.html')
