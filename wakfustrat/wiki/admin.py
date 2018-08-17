from django.contrib import admin

from wakfustrat.wiki.models import Boss, Content, Dungeon, Image, FeaturedPage, QuestCategory, Quest


admin.site.register(Content)
admin.site.register(Boss)
admin.site.register(Dungeon)
admin.site.register(Image)
admin.site.register(FeaturedPage)
admin.site.register(Quest)


@admin.register(QuestCategory)
class QuestCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
