from django.contrib import admin

from .models import (
    Group,
    GroupInfo,
    Post,
    Survey,
    SurveyQuestion,
    SurveyResult
)


class GroupInfoAdmin(admin.TabularInline):

    exclude = ['activity_score']
    list_display = ['group_name', 'created']
    model = GroupInfo

class GroupAdmin(admin.ModelAdmin):

    inlines = [GroupInfoAdmin]

    class Meta:
        model = GroupInfoAdmin


class SurveyQuestionAdmin(admin.StackedInline):

    model = SurveyQuestion
    exclude = []


class SurveyAdmin(admin.ModelAdmin):

    inlines = [SurveyQuestionAdmin]
    exclude = []

    class Meta:
        model = Survey


admin.site.register(Post)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyResult)
admin.site.register(GroupInfo)
admin.site.register(Group, GroupAdmin)