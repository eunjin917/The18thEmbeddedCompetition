from django.shortcuts import render, redirect
from .forms import DeviceForm, FileUploadForm, UserForm, LoginForm
from .models import Device, FileUpload, User, Accident
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def mainpage(request):
    user = request.user
    context = {'user': user}
    return render(request, 'mainpage.html', context)


def register(request):
    regiform = DeviceForm
    if request.method == 'POST':
        regiform = DeviceForm(request.POST)
        if regiform.is_valid():
            # 입력 정확한지 확인 및 메시지 띄우기
            if len(regiform.cleaned_data['VIN']) != 17:
                messages.info(request, '차대번호 17자리를 정확하게 입력해주세요.')
            elif len(regiform.cleaned_data['MAC']) != 12:
                messages.info(request, 'MAC주소 12자리를 정확하게 입력해주세요.')
            elif len(regiform.cleaned_data['tel']) not in [12, 13] or regiform.cleaned_data['tel'].count('-') != 2:
                messages.info(request, '연락처 12자리 또는 13자리를 -를 포함하여 정확하게 입력해주세요.')
            else:
                regiform.save() # 모두 정확하면 저장

                # 원래 사고정보-기기등록 안 된 차량에 해당되는 것이 있는지 확인 후, 사고 정보 업데이트
                acci = Accident.objects.all()
                myinfo = Device.objects.get(MAC=regiform.cleaned_data['MAC'])
                contain_acci = acci.filter(noregicar__icontains=regiform.cleaned_data['MAC']).all() # 해당되는 사고들 다 찾아오기
                for oneacci in contain_acci:
                    # 1. noregicar 수정
                    noregilst = eval(oneacci.noregicar)
                    noregilst.remove(regiform.cleaned_data['MAC'])
                    oneacci.noregicar = noregilst
                    # 2. othercars 수정
                    oneacci.othercars.add(myinfo)

                    oneacci.save()
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
            user = signup_form.save(commit=False)
            user.is_staff = True
            user.save()
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
        datas = data.split('\r\n')
        infos = Device.objects.all()

        # 1. 내 차량
        mycarMAC = datas[0]
        del datas[0]
        try:
            mycar = infos.filter(MAC=mycarMAC).get()
        except:
            return redirect('error')

        # 2. 모든 차량 정보 2차원배열에 넣기
        cardata = []
        for item in datas:
            cardata += [item.split('\t')]

        # 3. 사고 정보 뽑아내기
        isacci = 0
        accimoum = []
        accicar = []
        time = ''
        for item in cardata:
            # print(item)
            if item[3] == '1':
                isacci += 1
                if isacci == 1: # 첫 번째 사고주변 차량일 경우
                    time = item[1]+'_'+item[2] # 발생시간 확인
                accicar.append(item[0]) # 사고발생차량 리스트로 싹 저장
            elif item[3] == '0':
                if time != '':
                    # 4. DB와 대조 및 업데이트
                    try: # 이미 등록돼있는 경우 냅두고
                        accident = Accident.objects.filter(mycar_date=mycar.VIN+'_'+time).get()
                    except: # 등록X경우에는 저장해서 올려야함
                        accident = Accident.objects.create(mycar_date=mycar.VIN+'_'+time, mycar=mycar, date=time)
                        noregilst = []
                        for carmac in accicar:
                            try: # 기기등록한 차량일 경우 등록
                                info = infos.filter(MAC=carmac).get()
                                accident.othercars.add(info)
                            except: #기기등록X 차량일 경우 일단 list형식으로 저장
                                noregilst.append(carmac)
                        accident.carcount = isacci
                        accident.noregicar = noregilst
                        accident.save()

                    # 사고 객체 자체 (Accident객체)를 저장
                    accimoum.append(accident)
                    # 초기화
                    time = ''
                    accicar = []
                    isacci = 0

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
def detaildata(request, id):
    acci = Accident.objects.get(pk=id)

    mycar = acci.mycar
    othercars = acci.othercars
    noregicar = eval(acci.noregicar)
    carcount = acci.carcount
    
    context = {'mycar':mycar, 'othercars': othercars, 'noregicar':noregicar, 'carcount':carcount}

    return render(request, 'dataildata.html', context)


def error(request):
    return render(request, 'error.html')
