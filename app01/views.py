from django.shortcuts import render,HttpResponse,redirect
from app01 import models
import hashlib
# Create your views here.    #changed  top
import  Cryptodome
import os
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import  PKCS1_v1_5
import base64
from urllib import parse
from django.shortcuts import render
from django.http import *
from app01.forms import UserForm
from captcha.models import CaptchaStore
# 当前路径钥匙地址
curr_dir = os.path.dirname(os.path.realpath(__file__))
private_key_file = os.path.join(curr_dir, "private.pem") #密钥
public_key_file = os.path.join(curr_dir, "public.pem")  #公钥
private_key = ''
public_key = ''
with open(private_key_file,'r') as f:
    private_key = f.read()
    f.close()
with open(public_key_file,'r') as f:
    public_key = f.read()
    f.close()




#changed  below
def login_stu(request):
    print(request,type(request))
    print(request.method,type(request.method))
    # login_form = UserForm(request.POST)
    login_form = UserForm()
    if request.method =='GET':
        return render(request, 'login.html',{'public_key':public_key,'login_form':login_form}) #changed
    else:
        login_form = UserForm()
        # print(request.POST,type(request.POST))
        # print(request.POST['user'],type(request.POST['user']))
        # print(request.POST['pwd'], type(request.POST['pwd']))
        captchaHashkey = request.POST.get('captcha_0')
        code = request.POST.get("captcha_1")
        get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
        if get_captcha.response == code.lower():
            user = request.POST.get('user')
            pwd = request.POST.get('pwd')
            prikey = RSA.import_key(private_key)
            cipher_rsa = PKCS1_v1_5.new(prikey)
            pwd = cipher_rsa.decrypt(base64.b64decode(pwd), "error")
            md5 = hashlib.md5()
            # 进行加密，python2可以给字符串加密，python3只能给字节加密
            md5.update(pwd)
            #print(md5)
            pwd_md5 = md5.hexdigest()
            #print(type(pwd_md5),pwd_md5)
            if models.user.objects.filter(username= user,password=pwd_md5):
                student_=user
                # print(student_+"redirect")
                return student(request,student_)
                # return redirect('/student/',student=student_)
            else:
                return render(request, 'login.html',{'public_key':public_key,'login_form':login_form})#changed
        else:#验证码错误
            return render(request,'captcha_error.html')


def login_tea(request):
    print(request,type(request))
    print(request.method,type(request.method))
    if request.method =='GET':
        return render(request, 'login.html')
    else:
        print(request.POST,type(request.POST))
        print(request.POST['user'],type(request.POST['user']))
        print(request.POST['pwd'], type(request.POST['pwd']))
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        md5 = hashlib.md5()
        # 进行加密，python2可以给字符串加密，python3只能给字节加密
        md5.update(pwd.encode('utf-8'))
        #print(md5)
        pwd_md5 = md5.hexdigest()
        #print(type(pwd_md5),pwd_md5)
        if models.teacher.objects.filter(teachername= user,password= pwd_md5):
            teacher=user
            return redirect('/grade/')
        else:
            return render(request, 'login.html')


def student(request,student):
    all_grade = models.Grade.objects.all().order_by('username')
    # return render(request, 'student.html', {'all_grade': all_grade})
    # user = request.POST.get('user')
    # print(student)
    all_grade = models.Grade.objects.all().filter(username= student)
    # print("........")
    # print(all_grade)
    return render(request, 'student.html', {'user':student,'all_grade': all_grade})


def grade(request):
    # 查询全部学生的成绩
    all_grade = models.Grade.objects.all().order_by('username')
    # 查询指定学生的成绩

    return render(request, 'grade.html',{'all_grade':all_grade})

def grade_add(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        subject_name = request.POST.get('subject_name')
        grade = request.POST.get('grade')
        if not user_name:
            return render(request, 'grade_add.html', {'error': '学号不能为空'})
        if not subject_name:
            return render(request, 'grade_add.html', {'error': '科目不能为空'})
        if not grade:
            return render(request, 'grade_add.html', {'error': '成绩不能为空'})
        if models.Grade.objects.filter(username=user_name,subject=subject_name,Grade=grade):
            return render(request,'grade_add.html',{'error':'该信息已存在'})
        models.Grade.objects.create(username=user_name,subject=subject_name,Grade=grade)
        return redirect('/grade/')
    return render(request,'grade_add.html')
def grade_del(request):
    pk = request.GET.get('pk')
    print(pk)
    models.Grade.objects.filter(pk=pk).delete()
    return redirect('/grade/')

def grade_edit(request):
    pk = request.GET.get('pk')
    grade_obj = models.Grade.objects.get(pk=pk)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        subject_name = request.POST.get('subject_name')
        grade = request.POST.get('grade')
        models.Grade.objects.filter(pk=pk).update(username=user_name,subject = subject_name,Grade = grade)
        return redirect('/grade/')
    return render(request, 'grade_edit.html', {'grade_obj': grade_obj})

def regist(request):
    if request.method == 'GET':
        return render(request, 'change.html')
    if request.method == 'POST':
            # 注册
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        models.user.objects.create(username=user,password=pwd)
        return redirect('/login/')
def change(request):
    pk = request.GET.get('pk')
    user_obj = models.user.objects.get(pk=pk)
    if request.method == 'POST':
        password = request.POST.get('password')
        models.user.objects.filter(pk=pk).update(password=password)
        return redirect('/change/')
    return render(request, 'change.html')


def index(request):
    return render(request, 'index.html',{'public_key':public_key}) #changed

def stud_register(request):
    # 定义一个错误提示为空
    error_name = ''
    if request.method=='POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        #email = request.POST.get('email')
        user_list = models.user.objects.filter(username=user)
        if user_list :
            # 注册失败
            error_name = 并且把错误信息报出来
            return  render(r'%s用户名已经存在了' % user)
            # 返回到注册页面，equest, 'stud_register.html', {'error_name':error_name})
        else :
            # 数据保存在数据库中，并返回到登录页面
            # 密码加密md5散列值存入数据库
            md5 = hashlib.md5()
            # 进行加密，python2可以给字符串加密，python3只能给字节加密
            md5.update(password.encode('utf-8'))
            password_md5 = md5.hexdigest()
            user = models.user.objects.create(username=user,
                                       password=password_md5)
            user.save()
            # 同ip下跳转
            return redirect('/login/')
    return render(request, 'stud_register.html')

def teac_register(request):
    # 定义一个错误提示为空
    error_name = ''
    if request.method=='POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        #email = request.POST.get('email')
        user_list = models.teacher.objects.filter(teachername=user)
        if user_list :
            # 注册失败
            error_name = '%s用户名已经存在了' % user
            # 返回到注册页面，并且把错误信息报出来
            return  render(request, 'stud_register.html', {'error_name':error_name})
        else:
            # 数据保存在数据库中，并返回到登录页面
            # 密码加密md5散列值存入数据库
            md5 = hashlib.md5()
            # 进行加密，python2可以给字符串加密，python3只能给字节加密
            md5.update(password.encode('utf-8'))
            password_md5 = md5.hexdigest()
            user = models.teacher.objects.create(teachername=user,
                                       password=password_md5)
            user.save()
            # 同ip下跳转
            return redirect('/login/')
    return render(request, 'teac_register.html')

# 防护xss代码
def comment(request):
  if request.method == "GET":
    return render(request,"comment.html")
  else:
    v = request.POST.get("content")
    if "script" in v:
      return render(request, "comment.html",{'error':'小比崽子'})
    else:
      msg.append(v)
      return render(request,'comment.html')

# 防护SQL注入
class Database:
    hostname = '127.0.0.1'
    user = 'root'
    password = '123456'
    db = 'search'
    charset = 'utf8'
    def __init__(self):
        self.connection = MySQLdb.connect(self.hostname, self.user, self.password, self.db, charset=self.charset)
        self.cursor = self.connection.cursor()
    def insert(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()
    def query(self, query, params):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        return cursor.fetchall()
    def __del__(self):
        self.connection.close()
    # 格式化查询
    def database(self,MySQLdb):
        injectdata = "1"
        xcmd = "select * from user where id = %s"  # 格式化处理
        conn = MySQLdb.connect(database="test", user="post", password=self.password, host=self.hostname, port="3306")
        cur = conn.cursor()
        cur.execute(xcmd, injectdata)   #**    # or [injectdata] or (injectdata) ,官网给出安全操作sql的调用方法，用传参数的方法调用。**
        res = cur.fetchall()
        conn.commit()
        conn.close()
