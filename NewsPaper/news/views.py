from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from django.shortcuts import render
from .forms import PostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'


class PostSearch(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# def create_news(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         form.select = Post.news
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#     return render(request, 'news_edit.html', {'form': form})


class NewsCreate(PermissionRequiredMixin, CreateView):

    permission_required = ('news.add_post', )

    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.select = Post.news
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):

    permission_required = ('news.change_post', )

    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_form(self):
        form = super(UpdateView, self).get_form()
        if self.object.select != Post.news:
            self.template_name = 'message.html'
            return None
        return form


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):

    permission_required = ('news.add_post', )

    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.select = Post.article
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, UpdateView):

    permission_required = ('news.change_post', )

    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def get_form(self):
        form = super(UpdateView, self).get_form()
        if self.object.select != Post.article:
            self.template_name = 'message.html'
            return None
        return form


# from django.shortcuts import render
# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin
#
# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'index.html'
