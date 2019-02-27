from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from grumblr.models import *
from grumblr.forms import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse,Http404
from mimetypes import guess_type
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
import time
current_milli_time = lambda: int(round(time.time() * 1000))

def home(request):
    return render(request,'grumblr/welcome.html',{})

@login_required
def index(request):
    context={}
    try:
        posts    = UserPost.objects.all()
        comments = PostComment.objects.all()
        context['posts']     = posts  
        context['comments']  = comments
        context['user_view'] = UserProfile.objects.get(user=request.user)
        context['timestamp'] = current_milli_time()
        context['post_form'] = UserPostsForm()
        return render(request,'grumblr/index.html',context)
    except Exception as error:
        print(error)
        context['errors']='Invalid operation'
        return render(request,'grumblr/error.html',{})

@login_required
def update_post(request):
    context={}
    try:
        if request.method=='GET':
            timestamp = float(request.GET['timestamp'])
        else:
            timestamp = float(request.POST['timestamp'])
    except:
        timestamp =0.0
    posts=UserPost.get_changes(timestamp)
    context={'posts':posts,'user_view':UserProfile.objects.get(user=request.user),
             'timestamp':current_milli_time()}
    return render(request,'posts.json',context,content_type='application/json')


@login_required
def create_post(request):
    context={}
    try:
        if request.method== 'GET':
            return redirect(reverse('update_post'))
        user=request.user
        profile=UserProfile.objects.get(user=user)
        post_form=UserPostsForm(request.POST)
        if not post_form.is_valid():
            return redirect(reverse('index'))
        new_post=UserPost(user=user,profile=profile,username=user.username,text=post_form.cleaned_data['text'])
        new_post.save()
        posts=UserPost.objects.all()
        context['timestamp']=current_milli_time()
        return redirect(reverse('update_post'))
    except Exception as error:
        print(error)
        return render(request,'grumblr/error.html',{})

@login_required
def update_comment(request):
    context={}
    try:
        if request.method=='GET':
            timestamp = float(request.GET['timestamp'])
        else:
            timestamp = float(request.POST['timestamp'])
    except:
        timestamp =0.0
    comments = PostComment.get_changes(timestamp)
    context={'comments':comments,'user_view':UserProfile.objects.get(user=request.user),
             'timestamp':current_milli_time()}
    return render(request,'comments.json',context,content_type='application/json')

@login_required
def create_comment(request,post_id):
    context={}
    try:
        if request.method== 'GET':
            return redirect(reverse('update_comment'))
        user = UserProfile.objects.get(user=request.user)
        post = UserPost.objects.get(pk=post_id)
        
        comment_form=UserCommentForm(request.POST)
        if not comment_form.is_valid():
            return redirect(reverse('index'))
        new_comment =PostComment(user=user,post=post,comment=comment_form.cleaned_data['comment'])
        new_comment.save()
        context['timestamp']=current_milli_time()
        return redirect(reverse('update_comment'))
    except Exception as error:
        print(error)
        return render(request,'grumblr/error.html',{})


@login_required
def delete_post(request,post_id):
    errors = []
    # Deletes the item if present in the todo-list database.
    try:
        timestamp = float(request.GET['timestamp'])
    except:
        timestamp = 0.0
    try:
        post_to_delete = UserPost.objects.get(id=post_id)
        post_to_delete.delete()
        post = UserPost.objects.all()
        context = {'posts':students, 'errors':errors}
        return render(request, 'grumblr/index.html', context)
    except ObjectDoesNotExist:
        errors.append('The post did not exist in the system.')
        context = {'posts':students, 'errors':errors}
        return render(request, 'grumblr/index.html', context)

def register(request):
    context={}
    errors=[]
    context['errors']=errors
    try:
        if request.method =='GET':
            register_form=RegistrationForm()
            context={'register_form':register_form}
            return render(request,'grumblr/register.html',context)
        register_form=RegistrationForm(request.POST)
        if not register_form.is_valid():
            context={'register_form':register_form}
            return render(request, 'grumblr/register.html', context)

        new_user = User.objects.create_user(username  =register_form.cleaned_data['username'],
                                            password  =register_form.cleaned_data['password1'],
                                            email     =register_form.cleaned_data['email'],
                                            last_name =register_form.cleaned_data['last_name'],
                                            first_name=register_form.cleaned_data['first_name'])
        new_myuser=UserProfile(user=new_user,
                               username=new_user.username,
                               email=register_form.cleaned_data['email'],
                               last_name=register_form.cleaned_data['last_name'],
                               first_name=register_form.cleaned_data['first_name'],
                               )
        # If you wish to activate your account after clicking on the activation link, you should add 
        # new_user.is_active=False
        new_user.save()
        new_myuser.save()
        
        # Senging email part 
        token=default_token_generator.make_token(new_user)
        message="""Welcome to MS&F Club. Please click the link below to verify your email 
                   address and complete the registeration of your account:
                   http:// %s%s
                """ %(request.get_host(),reverse('confirm',args=(new_user.username,token)))
        send_mail(subject='Verify your email address',
                  message=message,
                  from_email='xinzez@andrew.cmu.edu',
                  recipient_list=[new_myuser.email],
                  fail_silently=False,
                 )
        message="An email has been sent to the email you entered when registeration,please click the link to confirm your account"
        context={'message':message}
        return render(request,'grumblr/register.html',context)
    except Exception as error:
        print(error)
        context['errors']='Invalid operation'
        return render(request,'grumblr/error.html',{})

def confirm_email(request,username,token):
    context={}
    try:
        user=User.objects.get(username=username)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            login(request,user)
            return redirect('index')
    except Exception as error:
        print(error)
        context['']=RegistrationForm()
        return render(request,'grumblr/register.html',context)

@login_required
def profile(request,user_username):
    context={}
    try:
        posts       = UserPost.objects.filter(username=user_username)
        comments    = PostComment.objects.all()
        user_viewed = UserProfile.objects.get(username=user_username)
        user_view   = UserProfile.objects.get(user    =request.user)
        follow=[]
        for follower in user_view.follow.all():
            follow.append(UserProfile.objects.get(user=follower))
        context={'posts':posts,'comments':comments,'user_view':user_view,'user_viewed':user_viewed,'follow':follow,'timestamp':current_milli_time() } 
        return render(request,'grumblr/profile.html',context)
    except Exception as error:
        print(error)
        context['errors']='Invalid operation'
        return render(request,'grumblr/error.html',{})

@login_required
def get_photo(request,user_username):
    try:
        user_view  = UserProfile.objects.get(username=user_username)
        if not user_view.image:
            raise Http404
        content_type=guess_type(user_view.image.name)
        return HttpResponse(user_view.image,content_type=content_type)
    except Exception as e:
        return render(request,'grumblr/error.html',{})

@login_required
def edit_profile(request):
    try:
        profile_to_edit=UserProfile.objects.get(user=request.user)
        if request.method=='GET':
            form=ProfileForm(instance=profile_to_edit)
            context={'form':form}
            return render(request,'grumblr/editprofile.html',context)
        form=ProfileForm(request.POST,request.FILES,instance=profile_to_edit)
        if not form.is_valid:
            context={'form':form}
            return render(request,'grumblr/editprofile.html',context)
        form.save()
        return redirect('index')
    except Exception as error:
        print(error)
        context['errors']='Invalid operation'
        return render(request,'grumblr/error.html',{})

@login_required
def follow(request,user_username):
    try:
        user_view   = UserProfile.objects.get(user=request.user)
        user_viewed = User.objects.get(username=user_username)
        user_view.follow.add(user_viewed)
        user_view.save()
        return redirect('profile',user_username=user_viewed.username)
    except Exception as e:
        return render(request,'grumblr/error.html',{})

@login_required
def unfollow(request,user_username):
    try:
        user_view   = UserProfile.objects.get(user=request.user)
        user_viewed = User.objects.get(username=user_username)
        user_view.follow.remove(user_viewed)
        user_view.save()
        return redirect('profile',user_username=user_viewed.username)
    except Exception as e:
        return render(request,'grumblr/error.html',{})

@login_required
def followstream(request):
    context={}
    try:
        user        = UserProfile.objects.get(user=request.user)
        follow      = user.follow
        posts       = UserPost.objects.all()
        comments    = PostComment.objects.all()
        context     = {'posts':posts,'follow':follow.all(),'comments':comments,'timestamp':current_milli_time()}
        return render(request,'grumblr/followstream.html',context)
    except Exception as e:
        print(error)
        return render(request,'grumblr/error.html',{})

@login_required
def change_password(request):
    try:
        if request.method == 'GET':
            Form = PasswordChangeForm(request.user)
            context={'Form':Form}
            return render(request,'grumblr/change_password.html',context)
        Form = PasswordChangeForm(request.user, request.POST)
        context={'Form':Form}
        if Form.is_valid():
            Form.save()
            update_session_auth_hash(request,Form.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request,'grumblr/change_password.html',context)
    except Exception as e:
        return render(request,'grumblr/error.html',{})

def reset_password(request):
    try:
        if request.method == 'GET':
            Form = PasswordResetForm()
            context={'Form':Form}
            return render(request,'grumblr/reset_password.html',context)
        Form = PasswordResetForm(request.POST)
        if not Form.is_valid():
            context['Form']=Form
            return render(request,'grumblr/reset_password.html',context)
        context={'Form':Form}
        user=User.objects.get(email=Form.cleaned_data['email'])
        if user:
            token=default_token_generator.make_token(user)
            message="""Welcome to MS&F Club. Please click the link below to reset your password:
                       http:// %s%s""" %(request.get_host(),reverse('reset_password_confirm',args=(user.username,token)))
            send_mail(subject='Reset your password',
                      message=message,
                   from_email='xinzez@andrew.cmu.edu',
               recipient_list=[user.email],
                fail_silently=False,
                  )
        context['message']="An email has been sent to your registeration email ,please click the link to reset your password. "
        return render(request,'grumblr/reset_password.html',context)
    except Exception as e:
        return render(request,'grumblr/error.html',{})

def reset_password_confirm(request,username,token):
    context={}
    try:
        user=User.objects.get(username=username)
        if default_token_generator.check_token(user,token):
            return redirect(reverse('set_password',args=[username]))
        context['Form'] = PasswordResetForm()
        context['message'] = "The link does not work,please try to get another one "
        return render(request, 'grumblr/reset_password.html', context)
    except Exception as e:
        return render(request,'grumblr/error.html',{})

def set_password(request,username):
    context={}
    try:
        user=User.objects.get(username=username)
        if request.method == 'GET':    
            Form = SetPasswordForm(user)
            context={'Form':Form,'username':username}
            return render(request,'grumblr/set_password.html',context)
        Form = SetPasswordForm(user,request.POST)
        if Form.is_valid():
            Form.save()
            return redirect('login')
        context={'Form':Form,'username':username}
        return render(request,'grumblr/set_password.html',context)
    except Exception as e:
        return render(request,'grumblr/error.html',{})

@login_required
def logout(request):
    try:
        logout(request)
        return render(request,'grumblr/welcome.html',{})
    except Exception as e:
        return render(request,'grumblr/error.html',{})

def error(request):
    return render(request,'grumblr/error.html',{})


