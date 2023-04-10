from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from content.models import Content, SharePost


class ContentListView(LoginRequiredMixin, ListView):
    model = Content
    template_name = 'content/home.html'
    context_object_name = 'contents'
    ordering = ['-date_posted']
    paginate_by = 5


class ContentDraftListView(LoginRequiredMixin, ListView):
    model = Content
    template_name = 'content/draft_content.html'
    context_object_name = 'contents'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return Content.objects.filter(writer=self.request.user, is_submit=False).order_by('-date_posted')


class ReceiveContentListView(LoginRequiredMixin, ListView):
    model = Content
    template_name = 'content/content_receive.html'
    context_object_name = 'contents'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        return SharePost.objects.filter(receive_user=self.request.user).all()


@login_required()
def receive_content(request):
    share_post_contents_obj = SharePost.objects.filter(receive_user=request.user).all()
    print(share_post_contents_obj)
    return render(request, 'content/content_receive.html', {"share_post_contents_obj": share_post_contents_obj})


class ContentDetailView(LoginRequiredMixin, DetailView):
    model = Content


def about(request):
    return render(request, 'content/about.html', {'title': 'About'})


class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content
    fields = ['title', 'summary', 'is_submit']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def add_content(request):
    if request.method == "POST":
        if 'save-content' in request.POST:
            # ADD CONTENT IN SAVE MODE
            if request.POST['title'] and request.POST['summary']:
                content = Content(title=request.POST["title"], summary=request.POST["summary"],
                                  writer=request.user)
                content.is_submit = True
                content.save()
                messages.success(request, 'content created successfully.')
            else:
                messages.error(request, 'please fill the title or summary')
        elif 'draft-content' in request.POST:
            # ADD CONTENT IN DRAFT MODE
            content = Content(title=request.POST["title"], summary=request.POST["summary"],
                              writer=request.user)
            content.is_submit = False
            messages.success(request, 'content added successfully in draft.')
            content.save()
    return render(request, 'content/add_content.html', {"user": request.user})


@login_required()
def update_content(request, pk):
    content_obj = get_object_or_404(Content, id=pk)
    if request.method == "POST":
        if request.POST["title"] and request.POST["summary"]:
            content_obj.title = request.POST["title"]
            content_obj.summary = request.POST["summary"]
            content_obj.save()
            messages.success(request, 'content updated successfully.')
        else:
            messages.error(request, 'please fill the title or summary')
    return render(request, 'content/update_content.html', {"content_obj": content_obj})


@login_required()
def search_content(request, pk):
    if request.method == 'POST':
        if search_username := request.POST["search_username"]:
            if user_obj := User.objects.get(username=search_username):
                content_obj = get_object_or_404(Content, id=pk)
                share_post_obj = SharePost(content=content_obj, receive_user=user_obj)
                share_post_obj.save()
                messages.success(request, 'content share successfully.')
            else:
                messages.error(request, 'writer username not found!!')
    return render(request, 'content/content_search.html')


class ContentUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    fields = ['title', 'summary']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content
    success_url = '/content'
