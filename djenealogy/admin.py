from django.contrib import admin
from django.core.urlresolvers import reverse
from .models import *


class GedcomAdmin(admin.ModelAdmin):
    def start_parse(self, request, queryset):
        from .importer import GedcomParser
        
        for g in queryset:
            GedcomParser(g).parse()
        
    start_parse.short_description = 'Parse Gedcom file'
    
    fieldsets = (
        (None, {
            'fields': ('file', ('name', 'slug'))
        }),
    )
    list_display = ('name', 'slug', 'created_on', 'modified_on')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    actions = ('start_parse',)
admin.site.register(Gedcom, GedcomAdmin)


class NoteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Gedcom', {
            'fields': (('gedcom', 'level'), ('xref', 'tag'), 'value')
        }),
        (None, {
             'fields': ('full_text',)
         })
    )
    list_display = ('__unicode__', 'gedcom', 'created_on', 'modified_on')
    list_select_related = ('gedcom',)
    search_fields = ('full_text',)
admin.site.register(Note, NoteAdmin)


def ind_link(obj, app):
    return '<a href="%s">%s</a>' % (reverse(app, args=(obj.id,)), obj)


class IndividualAdmin(admin.ModelAdmin):
    def mother(self, obj):
        return ind_link(obj.mother, 'admin:djenealogy_individual_change')
    
    def father(self, obj):
        return ind_link(obj.father, 'admin:djenealogy_individual_change')
    
    def parents_list(self, obj):
        txt = ''
        for x in obj.parent_families.all():
            txt += '<li>%s</li>' % ind_link(x, 'admin:djenealogy_family_change')
        return '<ul>%s</ul>' % txt
    parents_list.short_description = 'Parent families'
    
    def families_list(self, obj):
        txt = ''
        for x in obj.families.all():
            txt += '<li>%s</li>' % ind_link(x, 'admin:djenealogy_family_change')
        return '<ul>%s</ul>' % txt
    families_list.short_description = 'Families'
    
    def children_list(self, obj):
        txt = ''
        for x in obj.children:
            txt += '<li>%s</li>' % ind_link(x, 'admin:djenealogy_individual_change')
        return '<ul>%s</ul>' % txt
    children_list.short_description = 'Children'
    
    def spouses_list(self, obj):
        txt = ''
        for x in obj.spouses:
            txt += '<li>%s</li>' % ind_link(x, 'admin:djenealogy_individual_change')
        return '<ul>%s</ul>' % txt
    spouses_list.short_description = 'Spouses'
    
    def events_list(self, obj):
        txt = ''
        for x in obj.events.all():
            txt += '<li>%s</li>' % ind_link(x, 'admin:djenealogy_individualevent_change')
        return '<ul>%s</ul>' % txt
    events_list.short_description = 'Events'
    
    fieldsets = (
        ('Gedcom', {
            'fields': (('gedcom', 'level'), ('xref', 'tag'), 'value')
        }),
        (None, {
            'fields': (('given_name', 'surname',), ('prefix', 'suffix',), ('nickname', 'sex',), 'notes')
        }),
        ('Events', {
            'fields': (('birth_year', 'death_year',), 'events_list',)
        }),
        ('Relationships', {
            'fields': (('relate1', 'relate2'), ('mother', 'father',), 'parents_list', ('families_list', 'spouses_list'), 'children_list',)
        })
    )
    list_display = ('given_name', 'surname', 'sex', 'gedcom', 'created_on', 'modified_on')
    list_display_links = ('given_name', 'surname')
    list_select_related = ('gedcom',)
    list_filter = ('gedcom', 'sex',)
    search_fields = ('xref', 'surname', 'given_name',)
    readonly_fields = ('mother', 'father', 'parents_list', 'families_list', 'children_list', 'spouses_list', 'events_list',)
admin.site.register(Individual, IndividualAdmin)


class IndividualEventAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Gedcom', {
            'fields': ('gedcom', ('level', 'value'))
        }),
        (None, {
            'fields': (('type', 'individual'), ('date', 'date_parsed'), 'place', 'notes',)
        })
    )
    list_display = ('individual', 'type', 'date', 'place', 'gedcom', 'created_on', 'modified_on',)
    list_select_related = ('gedcom', 'individual',)
    list_filter = ('gedcom', 'type',)
    search_fields = ('date', 'place', 'individual__given_name', 'individual__surname')
    readonly_fields = ('date_parsed',)
admin.site.register(IndividualEvent, IndividualEventAdmin)

class FamilyEventAdmin(admin.ModelAdmin):
    # change the queryset to select related fields
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['family'].queryset = Family.objects.all().select_related('husband', 'wife')
         return super(FamilyEventAdmin, self).render_change_form(request, context, args, kwargs)      
    
    fieldsets = (
        ('Gedcom', {
            'fields': ('gedcom', ('level', 'value'))
        }),
        (None, {
            'fields': (('type', 'family'), ('date', 'date_parsed'), 'place', 'notes',)
        })
    )
    list_display = ('family', 'type', 'date', 'place', 'gedcom', 'created_on', 'modified_on',)
    list_select_related = ('gedcom', 'family', 'family__husband', 'family__wife',)
    list_filter = ('gedcom', 'type',)
    search_fields = ('date', 'place', 'family__husband__surname', 'family__husband__given_name', 'family__wife__surname', 'family__wife__given_name',)
    readonly_fields = ('date_parsed',)
admin.site.register(FamilyEvent, FamilyEventAdmin)


class FamilyAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Gedcom', {
            'fields': (('gedcom', 'level'), ('xref', 'tag'), 'value')
        }),
        (None, {
            'fields': (('husband', 'wife',), 'children', 'notes')
        }),
    )
    list_display = ('husband', 'wife', 'gedcom', 'created_on', 'modified_on')
    list_display_links = ('husband', 'wife')
    list_select_related = ('husband', 'wife', 'gedcom')
    list_filter = ('gedcom',)
    filter_horizontal = ('children',)
    search_fields = ('husband__given_name', 'husband__surname', 'wife__given_name', 'wife__surname', 'xref',)
admin.site.register(Family, FamilyAdmin)
