from bs4 import BeautifulSoup

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from wakfustrat.common.md import generate_html
from wakfustrat.common.models import Zone
from wakfustrat.wiki.forms import BossForm, DungeonForm, QuestForm
from wakfustrat.wiki.models import Boss, Content, Dungeon, Image, Quest


BOSS = 'boss-ultimes'
DUNGEON = 'donjons'
QUEST = 'quêtes'


class WikiPageMixin(object):

    part = None
    klass = None
    form_klass = None
    template_part = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.part = self.kwargs['part']
            self.klass = {
                DUNGEON: Dungeon,
                BOSS: Boss,
                QUEST: Quest
            }[self.part]
            self.form_klass = {
                DUNGEON: DungeonForm,
                BOSS: BossForm,
                QUEST: QuestForm
            }[self.part]
            self.template_part = {
                DUNGEON: 'dungeon',
                BOSS: 'boss',
                QUEST: 'quest'
            }[self.part]
            part_name = {
                DUNGEON: 'Donjons',
                BOSS: 'Boss Ultimes',
                QUEST: 'Quêtes'
            }[self.part]
            self.extra_context = {
                'part': self.part,
                'part_name': part_name
            }
        except KeyError:
            raise Http404('Part not found')
        return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def save_content(obj, markdown, user, previous=None):
        content = Content()
        content.markdown = markdown
        content.html, content.toc = generate_html(markdown)
        if previous is not None:
            content.version = previous.version + 1
            content.diff_count = len(markdown) - len(previous.markdown)
        else:
            content.version = 0
        content.by = user
        content.content_object = obj
        content.save()

        obj.images.set(Image.objects.none())
        soup = BeautifulSoup(content.html, 'html.parser')
        for image in soup.find_all('img'):
            try:
                image_obj = Image.objects.get(image=image.get('src').replace('/media/', ''))
                obj.images.add(image_obj)
            except Image.DoesNotExist:
                pass


# Generic


class WikiHistoryView(WikiPageMixin, ListView):
    """
    Display the history of a page.
    """
    context_object_name = 'versions'
    template_name = 'wiki/history.html'

    def get_queryset(self):
        obj = get_object_or_404(self.klass, slug=self.kwargs.get('slug'))
        self.extra_context.update({'page': obj})
        return obj.contents.order_by('-version').select_related('by')


class WikiImagesView(WikiPageMixin, ListView):
    """
    Display images linked to a page.
    """
    context_object_name = 'images'
    template_name = 'wiki/images.html'

    def get_queryset(self):
        obj = get_object_or_404(self.klass, slug=self.kwargs.get('slug'))
        self.extra_context.update({'page': obj})
        return obj.images.all()


class ImageUploadView(LoginRequiredMixin, View):
    """
    Upload an image.
    """
    def post(self, request, *args, **kwargs):
        image = Image(image=request.FILES.get('file'), by=request.user)
        image.save()
        return JsonResponse({'url': image.image.url})


class PageCreateView(LoginRequiredMixin, WikiPageMixin, CreateView):

    template_name = 'wiki/create.html'

    def get_form_class(self):
        return self.form_klass

    def form_valid(self, form):
        # TODO : vérifier que slug != management
        data = form.cleaned_data
        obj = form.save()
        self.save_content(obj, data.get('content'), self.request.user)

        return HttpResponseRedirect(obj.get_absolute_url())


class PageDetailView(WikiPageMixin, DetailView):
    """
    View a dungeon.
    """
    context_object_name = 'page'

    def get_queryset(self):
        queryset = self.klass._default_manager
        if self.part in [DUNGEON, BOSS]:
            queryset = queryset.select_related('zone', 'subzone')
        return queryset.all()

    def get_template_names(self):
        return 'wiki/{0}/detail.html'.format(self.template_part)


class PageListView(WikiPageMixin, ListView):
    """
    List all pages in a part.
    """
    def get_queryset(self):
        queryset = self.klass._default_manager

        if self.part in [DUNGEON, BOSS]:
            queryset = queryset.order_by('-level').select_related('zone')

        if self.part == DUNGEON and self.request.GET.get('zone') is not None:
            zone = get_object_or_404(Zone, slug=self.request.GET.get('zone'))
            queryset = queryset.filter(zone=zone)

        return queryset.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.part == DUNGEON:
            dungeons = Dungeon.objects
            context['published_count'] = dungeons.filter(status='published').count()
            context['draft_count'] = dungeons.filter(status='draft').count()
            context['zones'] = Zone.objects.filter(dungeon__in=dungeons.all()).order_by('slug').distinct()
            context['zone'] = self.request.GET.get('zone')
        return context

    def get_template_names(self):
        return 'wiki/{0}/list.html'.format(self.template_part)


class PageUpdateView(LoginRequiredMixin, WikiPageMixin, UpdateView):
    """
    Update a page.
    """
    context_object_name = 'page'
    template_name = 'wiki/update.html'

    def get_form_class(self):
        return self.form_klass

    def get_queryset(self):
        return self.klass._default_manager.all()

    def get_initial(self):
        initial = super().get_initial()
        initial['content'] = self.object.content.markdown
        return initial

    def form_valid(self, form):
        # TODO : vérifier que slug != management

        data = form.cleaned_data
        obj = form.save()

        self.save_content(obj, data.get('content'), self.request.user, previous=obj.content)

        return HttpResponseRedirect(obj.get_absolute_url())
