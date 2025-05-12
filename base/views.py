from datetime import date # datetime modülünden date sınıfını içe aktar
from django.shortcuts import render, redirect # render ve redirect fonksiyonlarını içe aktar
from django.views.generic.list import ListView # ListView sınıfını içe aktar
from django.views.generic.detail import DetailView # DetailView sınıfını içe aktar
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView  # FormView sınıfını içe aktar
from django.urls import reverse_lazy # reverse_lazy fonksiyonunu içe aktar
from django.contrib.auth.decorators import login_required # login_required dekoratörünü içe aktar

from django.contrib.auth.forms import PasswordChangeForm # şifre değiştirme formunu içe aktar
from django.contrib.auth import update_session_auth_hash # oturum güncelleme fonksiyonunu içe aktar
from django.contrib import messages # mesajları içe aktar

from django.contrib.auth.views import LoginView # giriş yapma fonksiyonunu içe aktar
from django.contrib.auth.mixins import LoginRequiredMixin # giriş yapma karışımı
from django.contrib.auth.forms import UserCreationForm # kullanıcı oluşturma formunu içe aktar
from django.contrib.auth import login # giriş yapma fonksiyonunu içe aktar

# Imports for Reordering Feature
from django.views import View # View sınıfını içe aktar
from django.db import transaction # transaction modülünü içe aktar

from .models import Task # Task modelini içe aktar
from .forms import PositionForm # PositionForm sınıfını içe aktar
from .forms import TaskForm # TaskForm sınıfını içe aktar

from django.utils import translation # dil çevirisi için gerekli

class CustomLoginView(LoginView):
    template_name = 'base/login.html' # giriş sayfası
    fields = '__all__'  # tüm alanları doldurumak zorunludur
    redirect_authenticated_user = True # giriş yapmış kullanıcıyı yönlendir

    def get_success_url(self): # giriş başarılı olduğunda yönlendirilecek url
        return reverse_lazy('tasks') # görevler sayfasına yönlendir


class RegisterPage(FormView):
    template_name = 'base/register.html' # kayıt sayfası
    form_class = UserCreationForm # kullanıcı kayıt formu
    redirect_authenticated_user = True # giriş yapmış kullanıcıyı yönlendir
    success_url = reverse_lazy('tasks') # görevler sayfasına yönlendir

    def form_valid(self, form): # formun geçerli olduğu durum
        user = form.save() # formu kaydet
        if user is not None: # eğer kullanıcı kaydedildiyse
            login(self.request, user) # kullanıcıyı giriş yapmış olarak işaretle
        return super(RegisterPage, self).form_valid(form) # formu kaydet

    def get(self, *args, **kwargs): # get isteği geldiğinde
        if self.request.user.is_authenticated: # eğer kullanıcı giriş yapmışsa
            return redirect('tasks') # görevler sayfasına yönlendir
        return super(RegisterPage, self).get(*args, **kwargs) # formu göster


class TaskList(LoginRequiredMixin, ListView):
    template_name = 'base/tasks.html' # görevlerin listeleneceği sayfa
    model = Task # görevlerin listeleneceği model
    context_object_name = 'tasks' 
    def get_context_data(self, **kwargs): # context verileri
        context = super().get_context_data(**kwargs) # üst sınıfın context verilerini al
        context['tasks'] = context['tasks'].filter(user=self.request.user) # kullanıcının görevlerini al
        for task in context['tasks']: # görevlerin bitiş tarihlerini kontrol et
            if task.deadline:  
                task.days_left = (task.deadline.date() - date.today()).days # gün sayısını hesapla
            else:
                task.days_left = None
                
        context['count'] = context['tasks'].filter(complete=False).count() # tamamlanmamış görev sayısını al
        search_input = self.request.GET.get('search-area') or '' # arama inputunu al
        if search_input: # eğer arama inputu varsa
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input # Arama çubuğuna yazılan kelimeyi al

        return context

def toggle_language(request): # Dil değiştirme fonksiyonu
    current_language = translation.get_language()  # Mevcut dil kodunu al
    new_language = 'en' if current_language == 'tr' else 'tr'  # Eğer TR ise EN, EN ise TR
    translation.activate(new_language) # Aktif dili değiştir
    request.session['django_language'] = new_language  # 'django_language' anahtarı kullanılıyor
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Aynı sayfaya yönlendir

class TaskDetail(LoginRequiredMixin, DetailView): # görev detay sayfası
    model = Task 
    context_object_name = 'task'
    template_name = 'base/task.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task # görev oluşturma sayfası
    form_class = TaskForm  
    template_name = 'base/task_form.html' # görev oluşturma sayfası
    success_url = reverse_lazy('tasks') 
    
    def form_valid(self, form): # formun geçerli olduğu durumda
        form.instance.user = self.request.user # formun kullanıcısını ayarla
        return super(TaskCreate, self).form_valid(form) # formu kaydet


class TaskUpdate(LoginRequiredMixin, UpdateView): # görev güncelleme sayfası
    model = Task # görev güncelleme sayfası
    fields = ['title', 'description', 'complete', 'branch'] # görevin güncellenebilecek alanları
    success_url = reverse_lazy('tasks') # görev güncelleme sayfası
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object() # görevi al
        if task.deadline: # eğer görevin bitiş tarihi varsa
            today = date.today() # bugün tarihi al
            days_left = (task.deadline.date() - today).days # gün sayısını hesapla
            context['deadline_text'] = task.deadline.strftime("%d %B %Y") # bitiş tarihini formatla
            context['days_left'] = days_left # gün sayısını al
        else:
            context['deadline_text'] = "Bitiş tarihi ayarlanmadı" # bitiş tarihi ayarlanmadı
            context['days_left'] = None # gün sayısını o olarak ayarla

        return context


class DeleteView(LoginRequiredMixin, DeleteView): # görev silme sayfası
    model = Task 
    context_object_name = 'task' 
    success_url = reverse_lazy('tasks') 
    def get_queryset(self): # görev silme sayfası
        owner = self.request.user # görev sahibini al
        return self.model.objects.filter(user=owner) # görev sahibine ait görevleri al

class TaskReorder(View): # görev sıralama sınıfı
    def post(self, request): # görev sıralama fonksiyonu
        form = PositionForm(request.POST) # görev sıralama formu

        if form.is_valid(): # formun geçerli olduğu durumda
            positionList = form.cleaned_data["position"].split(',') # görev sıralamasını al
            with transaction.atomic(): # görev sıralamasını kaydet
                self.request.user.set_task_order(positionList)
        return redirect(reverse_lazy('tasks'))

@login_required
def update_user_info(request): # kullanıcı bilgilerini güncelleme fonksiyonu
    if request.method == 'POST': # eğer post isteği geldiyse
        user = request.user # kullanıcıyı al
        user.username = request.POST.get('username') # kullanıcı adını güncelle
        user.email = request.POST.get('email') # e-posta adresini güncelle
        user.save() # kullanıcıyı kaydet
        messages.success(request, "Bilgiler güncellendi.") # başarı mesajı
    return redirect('tasks')  

@login_required
def change_password_modal(request): # şifre değiştirme fonksiyonu
    if request.method == 'POST': # eğer post isteği geldiyse
        form = PasswordChangeForm(user=request.user, data=request.POST) # şifre değiştirme formu
        if form.is_valid(): # formun geçerli olduğu durumda
            form.save() # formu kaydet
            update_session_auth_hash(request, form.user) # oturumu güncelle
            messages.success(request, 'Şifre güncellendi.') # başarı mesajı
        else:
            messages.error(request, 'Hata oluştu.') # hata mesajı
    return redirect('tasks')
