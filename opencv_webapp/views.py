from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})
def simple_upload(request):
    if request.method == 'POST': # 사용자가 form 태그 내부의 submit 버튼을 클릭하여 데이터를 제출했을 시
        # print(request.POST)
        # print(request.FILES)
        form = SimpleUploadForm(request.POST, request.FILES) # 빈 양식을 만든 후 사용자가 업로드한 데이터를 채워, 채워진 양식을 만듦
        if form.is_valid():
            myfile = request.FILES['image'] # 'image' : HTML input tag의 name attribute의 값
            # print(myfile.name) # 경로명 포함 파일명
            # print(myfile)
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile) # 업로드된 이미지의 경로명 & 이미지 파일 객체 자체
            # print(filename) # 파일명 포함한 URL
            uploaded_file_url = fs.url(filename)
            # print(uploaded_file_url)
            context = {'form':form, 'uploaded_file_url':uploaded_file_url}
            return render(request, 'opencv_webapp/simple_upload.html', context)
    else: # request.method == 'GET'
        form = SimpleUploadForm() # 비어져있는 양식
        context = {'form':form}
        return render(request, 'opencv_webapp/simple_upload.html', context)

def detect_face(request):
    if request.method == 'POST' :
        # 비어있는 Form에 사용자가 업로드한 데이터를 넣고 검증합니다.
        form = ImageUploadForm(request.POST, request.FILES) # filled form
        if form.is_valid():
             # Form에 채워진 데이터를 DB에 실제로 저장하기 전에 변경하거나 추가로 다른 데이터를 추가할 수 있음
            post = form.save(commit=False)
            post.save() # DB에 실제로 Form 객체('form')에 채워져 있는 데이터를 저장
	    # post는 save() 후 DB에 저장된 ImageUploadModel 클래스 객체 자체를 갖고 있게 됨 (record 1건에 해당)

            imageURL = settings.MEDIA_URL + form.instance.document.name
	    # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            # print(form.instance, form.instance.document.name, form.instance.document.url)
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정

            return render(request, 'opencv_webapp/detect_face.html', {'form':form, 'post':post})

    else:
         form = ImageUploadForm() # empty form
         return render(request, 'opencv_webapp/detect_face.html', {'form':form})
