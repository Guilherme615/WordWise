#importações
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Word, Request
from django.shortcuts import get_object_or_404
from braces.views import GroupRequiredMixin
from .forms import UserForm, RequestForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import AddTeacherForm
from django.core.exceptions import ObjectDoesNotExist

#sidebar


#logout
def logout_view(request):
    logout(request)
    return redirect('login')

#importações ajax
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import WordForm
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q

#função pra exibição:
def home(request):
    words = Word.objects.all()
    return render(request, 'cadastro_palavras/home.html', {'words': words})


def save_form(request, form, template_name):
    data = {}  # Dicionário para os dados de resposta

    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            data['form_is_valid'] = True
            words = Word.objects.filter(user=request.user)
            data['html_list'] = render_to_string('lists/parcial_list.html', {'object_list': words})
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)

    return JsonResponse(data)
    ########## A galera abaixo será executada mesmo se o form seja válido ou não ##########

    context = {'form': form} # Pega o form e salva dentro do dicionário "context" (Sendo válido ou não)
    data['html_form'] = render_to_string(template_name, context, request=request) # Pega o nome do template, o dicionário que guarda o form, a request e retorna dentro do HTML em questão

    return JsonResponse(data) # Retorna dentro do arquivo HTML os elementos do dicionário "data", que serão utilizados no javascript

    #função que não permite que um user apaguem ou editem conteúdo adicionado por outros users, se não ele.(não poder ver)
    def get_queryset(self):
        # Verificar se o usuário é um administrador
        is_admin = self.request.user.groups.filter(name='Administrador').exists()
        # Se o usuário é um administrador, permitir que ele veja/liste todas as palavras
        if is_admin:
            return Word.objects.all()
        else:
            # Se o usuário é um professor, permitir que ele veja/liste apenas suas próprias palavras
            is_prof = self.request.user.groups.filter(name='Professor').exists()
            if is_prof:
                return Word.objects.filter(user=self.request.user)
            else:
                # Se o usuário não é nem administrador nem professor, retornar uma queryset vazia
                return Word.objects.none()


def word_create(request):
    if request.method == "POST": # Se o formulário for preenchido e enviado (requisição POST),
        form = WordForm(request.POST) # Pega as informações contidas na requisição POST e salva no formulário, criando um objeto (uma nova word)
    else: # Se for GET,
        form = WordForm() # Salva o formulário vazio para ser preenchido
    return save_form(request, form, "lists/parcial_create.html")


#indexView:
class IndexView(TemplateView):
    template_name = "index.html"
# Crud de palavras
# Create
class WordCreate(GroupRequiredMixin,CreateView):
    group_required = [u"Administrador", u"Professor"]
    login_url = reverse_lazy('login')
    model = Word
    fields = ['word', 'description']
    template_name = 'lists/forms/form.html'
    success_url = reverse_lazy('list-words')
#função que não permite que um user apaguem ou editem conteúdo adicionado por outros users, se não ele.
    def form_valid(self, form):
        form.instance.user = self.request.user

        # Verifica se a palavra já existe no banco de dados
        existing_word = Word.objects.filter(word=form.instance.word)
        if existing_word.exists():
            form.add_error('word', 'Esta palavra já existe no banco de dados.')
            return self.form_invalid(form)

        return super().form_valid(form)
#Update
class WordUpdate(GroupRequiredMixin,UpdateView):
    group_required = [u"Administrador", u"Professor"]
    login_url = reverse_lazy('login')
    model = Word
    fields = ['word', 'description']
    template_name = 'lists/forms/form.html'
    success_url = reverse_lazy('list-words')
    
#função que não permite que um user apaguem ou editem conteúdo adicionado por outros users, se não ele.
    def get_object(self, query=None):
        self.object = get_object_or_404(Word, pk=self.kwargs['pk'])
        # Verificar se o usuário é um administrador
        is_admin = self.request.user.groups.filter(name='Administrador').exists()
        # Verificar se o usuário é um professor e se é o mesmo usuário que criou a palavra
        is_prof = self.request.user.groups.filter(name='Professor').exists()
        is_same_Professor = self.object.user == self.request.user
        # Condições para permitir a edição
        if is_admin or (is_prof and is_same_Professor):
            return self.object
        else:
            raise Http404("Você não tem permissão para editar esta palavra.")

#Delete
class WordDelete(GroupRequiredMixin,DeleteView):
    group_required = [u"Administrador", u"Professor"]
    login_url = reverse_lazy('login')
    model = Word
    template_name = 'lists/forms/delete-form.html'
    success_url = reverse_lazy('list-words')

#função que não permite que um user apaguem ou editem conteúdo adicionado por outros users, se não ele.
    def get_object(self, query=None):
        # Obter a palavra com base no ID (pk)
        self.object = get_object_or_404(Word, pk=self.kwargs['pk'])
        
        # Verificar se o usuário é um administrador
        is_admin = self.request.user.groups.filter(name='Administrador').exists()
        
        # Verificar se o usuário é um professor e se é o mesmo usuário que criou a palavra
        is_prof = self.request.user.groups.filter(name='Professor').exists()
        is_same_Professor = self.object.user == self.request.user
        
        # Condições para permitir a exclusão
        if is_admin or (is_prof and is_same_Professor):
            return self.object
        else:
            raise Http404("Você não tem permissão para apagar esta palavra.")

#List
#função de IF pro admin ter recursos especiais.
def is_admin(user):
    return user.groups.filter(name='Administrador').exists()
#função de IF pro prof ter recursos especiais.
def is_prof(user):
    return user.groups.filter(name='Professor').exists()

def word_list(request):
    context = {
        'words': Word.objects.all(),
        'is_admin': is_admin(request.user),
    }
    return render(request, 'lists/words.html', context)

class WordList(ListView):
    model = Word
    template_name = 'lists/words.html'
    paginate_by = 10

    def get_queryset(self):
        if not is_admin(self.request.user):
            return Word.objects.filter(user=self.request.user).order_by('-created_at')
        word = self.request.GET.get('word')
        if word:
            word = Word.objects.filter(word__icontains=word).order_by('-created_at')
        else:
            word = Word.objects.all().order_by('-created_at')
        return word

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


#users:
class UserCreate(CreateView):
    form_class = UserForm
    template_name = 'users/form-users.html'
    success_url = reverse_lazy('login')
#palavras para usuarios não cadastrados
class UserWordList(ListView):
    model = Word
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        word = self.request.GET.get('word')
        if word:
            words = Word.objects.filter(word__icontains=word)
        else:
            words = Word.objects.all()
        return words



#Crud de solicitações:
#Create
class RequestCreate(LoginRequiredMixin, CreateView):
    model = Request
    fields = ['word_req']
    template_name = 'lists/forms/request_form.html'
    success_url = reverse_lazy('list-requests')

    #função de preencher o usuário automaticamente:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#Update:
class RequestUpdate(LoginRequiredMixin, UpdateView):
    model = Request
    fields = ['word_req']
    template_name = 'lists/forms/request_form.html'
    success_url = reverse_lazy('list-requests')

    #função de preencher o usuário automaticamente:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    #função anti delete:
    def get_object(self, query=None):
        # Obter a palavra com base no ID (pk)
        self.object = get_object_or_404(Request, pk=self.kwargs['pk'])
        
        # Verificar se o usuário é um administrador
        is_admin = self.request.user.groups.filter(name='Administrador').exists()
        
        # Verificar se o usuário é um professor
        is_prof = self.request.user.groups.filter(name='Professor').exists()
        
        # Condições para permitir a exclusão
        if is_admin or is_prof:
            return self.object
        else:
            raise Http404("Você não tem permissão para editar esta Socilitação.")

# Delete
class RequestDelete(LoginRequiredMixin, DeleteView):
    model = Request
    template_name = 'lists/forms/request_delete_form.html'
    success_url = reverse_lazy('list-requests')

    def get_object(self, query=None):
        # Obter a palavra com base no ID (pk)
        self.object = get_object_or_404(Request, pk=self.kwargs['pk'])
        
        # Verificar se o usuário é um administrador
        is_admin = self.request.user.groups.filter(name='Administrador').exists()
        
        # Verificar se o usuário é um professor e se é o mesmo usuário que criou a palavra
        is_prof = self.request.user.groups.filter(name='Professor').exists()
        # Condições para permitir a exclusão
        if is_admin or is_prof:
            return self.object
        else:
            raise Http404("Você não tem permissão para apagar esta solicitação.")

# List
class RequestList(ListView):
    model = Request
    template_name = 'lists/requests.html'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if is_admin(user) or is_prof(user):
            word_req = self.request.GET.get('word_req')
            queryset = Request.objects.all().order_by('-created_at')

            if word_req:
                queryset = queryset.filter(word__icontains=word_req)

            return queryset

        return Request.objects.filter(user=user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

@login_required(login_url='login')  # Certifica-se de que o usuário está autenticado
def admin_page(request):
    if not request.user.groups.filter(name='Administrador').exists():
        # Apenas permita que usuários com o grupo 'Administrador' acessem esta página
        return HttpResponseRedirect(reverse('login'))

    # Obtém todos os usuários que não fazem parte do grupo 'Professor'
    users = User.objects.exclude(groups__name='Professor')

    if request.method == 'POST':
        # Lógica para processar o formulário enviado
        selected_users = request.POST.getlist('selected_users')
        professors_group = Group.objects.get(name='Professor')

        # Adiciona os usuários selecionados ao grupo 'Professor'
        professors_group.user_set.add(*selected_users)

    context = {'users': users}
    return render(request, 'admin_page.html', context)

def admin_page(request):
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            professors_group = Group.objects.get(name='Professors')
            user.groups.add(professors_group)
            return redirect('admin_page')  # You can change this to your desired URL
    else:
        form = AddTeacherForm()

    return render(request, 'admin_page.html', {'form': form})



def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')  # Substitua 'admin' pelo nome da sua página de administração
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def admin_page(request):
    if request.method == 'POST':
        group, created = Group.objects.get_or_create(name='Professor')

def admin_page(request):
    if request.method == 'POST':
        try:
            group = Group.objects.get(name='Professor')
        except ObjectDoesNotExist:
            # Trate o caso em que o grupo não existe
            # Você pode criar o grupo ou redirecionar com uma mensagem de erro
            # Exemplo: Group.objects.create(name='Professor')
            return HttpResponse("Grupo não existe. Por favor, crie o grupo.")

        # Restante da lógica da sua visão aqui
        # ...
@login_required(login_url='login')
def admin_page(request):
    if not request.user.groups.filter(name='Administrador').exists():
        # Apenas permita que usuários com o grupo 'Administrador' acessem esta página
        return HttpResponseRedirect(reverse('login'))

    # Lógica para processar o formulário enviado
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                professors_group, created = Group.objects.get_or_create(name='Professor')
                user.groups.add(professors_group)
                return redirect('admin_page')  # Você pode alterar isso para a URL desejada
            except User.DoesNotExist:
                # Trate o caso em que o usuário não existe
                return HttpResponse("Usuário não existe. Por favor, crie o usuário.")
    else:
        form = AddTeacherForm()

    # Obtém todos os usuários que não fazem parte do grupo 'Professor'
    users = User.objects.exclude(groups__name='Professor')

    context = {'form': form, 'users': users}
    return render(request, 'admin_page.html', context)

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_page')  # Substitua 'admin_page' pelo nome da sua página de administração
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})