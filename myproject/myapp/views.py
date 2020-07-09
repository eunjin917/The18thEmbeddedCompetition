from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, FileUploadForm
from .models import Register, FileUpload

# Create your views here.

def mainpage(request):
    return render(request, 'mainpage.html')

def register(request):
    regiform = RegisterForm(request.POST)
    context = {'regiform':regiform}

    if request.method == 'POST':
        if regiform.is_valid():
            regiform.save()  
            return redirect('mainpage')

    return render(request, 'register.html', context)

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

def foruser(request):
    try:
        # 읽기
        myfileitem = FileUpload.objects.last()
        data = myfileitem.myfile.file.read()
        data = data.decode("utf-8")
        # 삭제
        myfileitem.delete()  
        # 가공
        lst = data.split('\r\n')
        # print(lst)
        count = len(lst)
        # 출력
        context = {'count':count}
    except:
        return redirect('error')

    return render(request, 'foruser.html', context)

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

def forpoli(request):
    try:
        # 읽기
        myfileitem = FileUpload.objects.last()
        data = myfileitem.myfile.file.read()
        data = data.decode("utf-8")
        # 삭제
        myfileitem.delete()  
        # 가공
        lst = data.split('\r\n')
        mylst = []
        infos = Register.objects.all()
        for mac in lst:
            info = infos.filter(MAC=mac).get()
            mylst.append((info.VIN, info.name, info.tel))
        # 출력
        context = {'mylst':mylst}
    except:
        return redirect('error')

    return render(request, 'forpoli.html', context)

def error(request):
    return render(request, 'error.html')