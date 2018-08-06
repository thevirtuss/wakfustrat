from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from wakfustrat.common.md import generate_html
from wakfustrat.wiki.forms import DungeonForm
from wakfustrat.wiki.models import Boss, Content, Dungeon, Image


# Generic


class WikiHistoryView(ListView):

    context_object_name = 'versions'
    template_name = 'wiki/history.html'

    def get_queryset(self):
        try:
            klass = {
                'donjons': Dungeon,
                'boss-ultimes': Boss
            }[self.kwargs.get('part')]
        except KeyError:
            raise Http404
        obj = get_object_or_404(klass, slug=self.kwargs.get('slug'))
        self.extra_context = {'wiki_obj': obj}
        return obj.contents.order_by('-version')


class ImageUploadView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        image = Image(image=request.FILES.get('file'), by=request.user)
        image.save()
        return JsonResponse({'url': image.image.url})


# Dungeon


class NewDungeonView(LoginRequiredMixin, CreateView):

    form_class = DungeonForm
    template_name = 'wiki/new.html'

    def form_valid(self, form):
        # TODO : vérifier que slug != management
        data = form.cleaned_data
        dungeon = Dungeon()
        dungeon.name = data.get('name')
        dungeon.slug = slugify(data.get('name'))
        dungeon.boss = data.get('boss')
        dungeon.level = data.get('level')
        dungeon.difficulty = data.get('difficulty')
        dungeon.zone = data.get('zone')
        dungeon.subzone = data.get('subzone')
        dungeon.image = data.get('image')
        dungeon.save()
        content = Content()
        content.markdown = data.get('content')
        content.html, content.toc = generate_html(data.get('content'))
        content.version = 0
        content.by = self.request.user
        content.content_object = dungeon
        content.save()

        return HttpResponseRedirect(dungeon.get_absolute_url())


class DungeonUpdateView(LoginRequiredMixin, UpdateView):
    """

    """
    context_object_name = 'article'
    form_class = DungeonForm
    model = Dungeon
    template_name = 'wiki/update.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['content'] = self.object.content.markdown
        return initial

    def form_valid(self, form):
        # TODO : vérifier que slug != management

        data = form.cleaned_data
        obj = form.save()

        previous = obj.content

        content = Content()
        content.markdown = data.get('content')
        content.html, content.toc = generate_html(data.get('content'))
        content.version = previous.version + 1
        content.by = self.request.user
        content.diff_count = len(data.get('content')) - len(previous.markdown)
        content.content_object = obj
        content.save()

        return HttpResponseRedirect(obj.get_success_url())


class DungeonListView(ListView):

    model = Dungeon
    template_name = 'wiki/dungeon/list.html'

    def get_queryset(self):
        return Dungeon.objects.filter(status__in=['published', 'draft']).order_by('-level').all()


class DungeonDetailView(DetailView):
    """
    View a dungeon.
    """
    model = Dungeon
    template_name = 'wiki/dungeon/detail.html'
