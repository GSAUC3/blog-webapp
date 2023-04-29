from django.shortcuts import render,redirect,get_object_or_404
from .models import Post
from .forms import  UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView 
    )



class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'post_confirm.delete.html'
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False


class UserPostListView(ListView):
    model = Post
    template_name = 'userpost.html'
    context_object_name = 'posts'
    

    def get_queryset(self):
        user = get_object_or_404(User,username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'

    def form_valid(self,form):
        # setting the author 
        form.instance.author = self.request.user 
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'post_form.html'

    def form_valid(self,form):
        # setting the author 
        form.instance.author = self.request.user 
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False


def home(request):
    return render(request,'home.html',context={"posts":Post.objects.all()})

def about(request):
    return render(request,'about.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Acount Created {username}!')
            return redirect('login')
        else: 
            return render(request,'register.html',{'form':form})

    else: 
        form = UserRegisterForm()
        

    return render(request,'register.html',{'form':form})

@login_required
def profile(request):
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES     
                                   ,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'uform': u_form,
               'pform': p_form}
    return render(request,'profile.html',context)