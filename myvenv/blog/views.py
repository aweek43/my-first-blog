from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Post, Portalhtml
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, UserForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.template import RequestContext

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def portalhtml(request):
    portalhtmls = Portalhtml.objects.all() #모든 portalhtml의 객체 가져옴
    context = {'portalhtmls':portalhtmls}
    return render(request, 'blog/myportal.html', context)

#회원가입
def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            # 회원가입 하면 초기화면 html을 자동 저장
            html = Portalhtml(author = request.user, text = '   <div class=\"page-header\" style=\"text-align: center\">        <h1>MyPortal</h1>   </div>  <button id=\"openmenu\" style=\"display: none;\" onclick=\"openmenu();\"> &lt; </button>    <button id=\"closemenu\" style=\"display: inline-block;\" onclick=\"closemenu();\"> &gt; </button>  <br>    <div id=\"wrapper\">        <div class=\"linkbox\" id=\"googlebox\" >           <div class=\"linkboxheader\" id=\"googleboxheader\">                <button class=\"Xbutton\" onclick=\"closeDiv(\'googlebox\');\">X</button>           </div>          <a href=\"https://www.google.co.kr/\" target=\"_blank\">                <img width=\"200\" height=\"100\" src=\"../../static/images/Google.JPG\"><br>Let\'s go Google!          </a>            <input id=\"googleInput\" type=\"text\">            <button id=\"googleButton\" onclick=\'window.open(\"https://www.google.com/search?q=\" + google())\'>Search on Google</button>      </div>      <div class=\"linkbox\" id=\"backjoonbox\">          <div class=\"linkboxheader\" id=\"backjoonboxheader\">              <button class=\"Xbutton\" onclick=\"closeDiv(\'backjoonbox\');\">X</button>             </div>          <a href=\"https://www.acmicpc.net/\" target=\"_blank\">                 <img width=\"200\" height=\"100\" src=\"../../static/images/backjoon.JPG\"><br>Let\'s go BackJoon!          </a>            <input id=\"backjoonInput\" type=\"text\">          <button id=\"backjoonButton\" onclick=\'window.open(\"https://www.acmicpc.net/problem/\" + backjoon())\'>Go to Problem Number</button>      </div>      <br><br>        <div class=\"linkbox\" id=\"naverbox\">             <div class=\"linkboxheader\" id=\"naverboxheader\">                 <button class=\"Xbutton\" onclick=\"closeDiv(\'naverbox\');\">X</button>            </div>          <a href=\"https://www.naver.com/\" target=\"_blank\">               <img width=\"200\" height=\"100\" src=\"../../static/images/naver.JPG\"><br>Let\'s go NAVER!            </a>            <input id=\"naverInput\" type=\"text\">             <button id=\"naverButton\" onclick=\'window.open(\"https://search.naver.com/search.naver?query=\" + naver())\'>Search on NAVER</button>         </div>      <div class=\"linkbox\" id=\"calculatebox\">             <div class=\"linkboxheader\" id=\"calculateboxheader\">                 <button class=\"Xbutton\" onclick=\"closeDiv(\'calculatebox\');\">X</button>            </div>          <a href=\"http://www.wolframalpha.com/\" target=\"_blank\">                 <img width=\"200\" height=\"100\" src=\"../../static/images/calculate.JPG\"><br>Let\'s do Infinitesimal Calculus!           </a>        </div>      <br><br>        <div class=\"linkbox\" id=\"klasbox\">          <div class=\"linkboxheader\" id=\"klasboxheader\">              <button class=\"Xbutton\" onclick=\"closeDiv(\'klasbox\');\">X</button>             </div>          <a href=\"https://klas.khu.ac.kr/\" target=\"_blank\">              <img width=\"200\" height=\"100\" src=\"../../static/images/KLAS.JPG\"><br>Let\'s go KLAS!          </a>        </div>      <br><br>        <div class=\"linkbox\" id=\"youtubebox\" >          <div class=\"linkboxheader\" id=\"youtubeboxheader\">               <button class=\"Xbutton\" onclick=\"closeDiv(\'youtubebox\');\">X</button>          </div>          <a href=\"https://www.youtube.com/\" target=\"_blank\">                 <img width=\"200\" height=\"100\" src=\"../../static/images/YouTube.JPG\"><br>Let\'s go YouTube!            </a>            <input id=\"youtubeInput\" type=\"text\">           <button id=\"youTubeButton\" onclick=\'window.open(\"https://www.youtube.com/results?search_query=\" + youtube())\'>Search on YouTube</button>      </div>      <br><br>        <div class=\"linkbox\" id=\"makeitbox\">            <div class=\"linkboxheader\" id=\"makeitboxheader\">                <button class=\"Xbutton\" onclick=\"closeDiv(\'makeitbox\');\">X</button>           </div>          <button width=\"200px\" height=\"100px\" id=\"makeitbutton\" onclick=\"gomakeit();\">Created Page</button>          <br>            이름: <input type=\"text\" id=\"makeitname\">             <input type=\"hidden\" id=\"hiddenmakeitname\">             <br>            URL: <input type=\"text\" id=\"makeiturl\">             <input type=\"hidden\" id=\"hiddenmakeiturl\">      </div>  </div>')
            html.save()
            return redirect('myportal')
    else:
        form = UserForm()
        return render(request, 'blog/adduser.html', {'form': form})

#로그인
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('myportal')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})

def savehtml(request):
    if request.method == "POST":
        try:
            html = Portalhtml.objects.get(author = request.user) #현재유저의 객체 가져옴 못가져올경우 except
            html.text = request.POST['htmlname']
            html.save()
        except:
            # 회원가입 시 저장하지만 혹시나 저장 안될경우 초기화면 저장
            html = Portalhtml(author = request.user, text = '   <div class=\"page-header\" style=\"text-align: center\">        <h1>MyPortal</h1>   </div>  <button id=\"openmenu\" style=\"display: none;\" onclick=\"openmenu();\"> &lt; </button>    <button id=\"closemenu\" style=\"display: inline-block;\" onclick=\"closemenu();\"> &gt; </button>  <br>    <div id=\"wrapper\">        <div class=\"linkbox\" id=\"googlebox\" >           <div class=\"linkboxheader\" id=\"googleboxheader\">                <button class=\"Xbutton\" onclick=\"closeDiv(\'googlebox\');\">X</button>           </div>          <a href=\"https://www.google.co.kr/\" target=\"_blank\">                <img width=\"200\" height=\"100\" src=\"../../static/images/Google.JPG\"><br>Let\'s go Google!          </a>            <input id=\"googleInput\" type=\"text\">            <button id=\"googleButton\" onclick=\'window.open(\"https://www.google.com/search?q=\" + google())\'>Search on Google</button>      </div>      <div class=\"linkbox\" id=\"backjoonbox\">          <div class=\"linkboxheader\" id=\"backjoonboxheader\">              <button class=\"Xbutton\" onclick=\"closeDiv(\'backjoonbox\');\">X</button>             </div>          <a href=\"https://www.acmicpc.net/\" target=\"_blank\">                 <img width=\"200\" height=\"100\" src=\"../../static/images/backjoon.JPG\"><br>Let\'s go BackJoon!          </a>            <input id=\"backjoonInput\" type=\"text\">          <button id=\"backjoonButton\" onclick=\'window.open(\"https://www.acmicpc.net/problem/\" + backjoon())\'>Go to Problem Number</button>      </div>      <br><br>        <div class=\"linkbox\" id=\"naverbox\">             <div class=\"linkboxheader\" id=\"naverboxheader\">                 <button class=\"Xbutton\" onclick=\"closeDiv(\'naverbox\');\">X</button>            </div>          <a href=\"https://www.naver.com/\" target=\"_blank\">               <img width=\"200\" height=\"100\" src=\"../../static/images/naver.JPG\"><br>Let\'s go NAVER!            </a>            <input id=\"naverInput\" type=\"text\">             <button id=\"naverButton\" onclick=\'window.open(\"https://search.naver.com/search.naver?query=\" + naver())\'>Search on NAVER</button>         </div>      <div class=\"linkbox\" id=\"calculatebox\">             <div class=\"linkboxheader\" id=\"calculateboxheader\">                 <button class=\"Xbutton\" onclick=\"closeDiv(\'calculatebox\');\">X</button>            </div>          <a href=\"http://www.wolframalpha.com/\" target=\"_blank\">                 <img width=\"200\" height=\"100\" src=\"../../static/images/calculate.JPG\"><br>Let\'s do Infinitesimal Calculus!           </a>        </div>      <br><br>        <div class=\"linkbox\" id=\"klasbox\">          <div class=\"linkboxheader\" id=\"klasboxheader\">              <button class=\"Xbutton\" onclick=\"closeDiv(\'klasbox\');\">X</button>             </div>          <a href=\"https://klas.khu.ac.kr/\" target=\"_blank\">              <img width=\"200\" height=\"100\" src=\"../../static/images/KLAS.JPG\"><br>Let\'s go KLAS!          </a>        </div>      <br><br>        <div class=\"linkbox\" id=\"youtubebox\" >          <div class=\"linkboxheader\" id=\"youtubeboxheader\">               <button class=\"Xbutton\" onclick=\"closeDiv(\'youtubebox\');\">X</button>          </div>          <a href=\"https://www.youtube.com/\" target=\"_blank\">                 <img width=\"200\" height=\"100\" src=\"../../static/images/YouTube.JPG\"><br>Let\'s go YouTube!            </a>            <input id=\"youtubeInput\" type=\"text\">           <button id=\"youTubeButton\" onclick=\'window.open(\"https://www.youtube.com/results?search_query=\" + youtube())\'>Search on YouTube</button>      </div>      <br><br>        <div class=\"linkbox\" id=\"makeitbox\">            <div class=\"linkboxheader\" id=\"makeitboxheader\">                <button class=\"Xbutton\" onclick=\"closeDiv(\'makeitbox\');\">X</button>           </div>          <button width=\"200px\" height=\"100px\" id=\"makeitbutton\" onclick=\"gomakeit();\">Created Page</button>          <br>            이름: <input type=\"text\" id=\"makeitname\">             <input type=\"hidden\" id=\"hiddenmakeitname\">             <br>            URL: <input type=\"text\" id=\"makeiturl\">             <input type=\"hidden\" id=\"hiddenmakeiturl\">      </div>  </div>')
            html.save()
    return redirect('myportal')
