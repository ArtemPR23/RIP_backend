from django.contrib import admin
from .models import CulturalArtifact

@admin.register(CulturalArtifact)
class CulturalArtifactAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'author', 
        'publication_year', 
        'genre', 
        'base_influence_score',
        'influence_category'
    ]
    list_filter = ['genre', 'publication_year', 'is_active']
    search_fields = ['title', 'author', 'description']
    readonly_fields = ['created_at', 'updated_at', 'total_influence_score']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'description', 'publication_year', 'genre')
        }),
        ('Показатели влияния', {
            'fields': (
                'base_influence_score', 
                'citation_count', 
                'media_mentions', 
                'social_media_score', 
                'adaptation_count',
                'total_influence_score'
            )
        }),
        ('Дополнительно', {
            'fields': ('image', 'is_active', 'created_at', 'updated_at')
        }),
    )

    def total_influence_score(self, obj):
        return obj.total_influence_score()
    total_influence_score.short_description = 'Общий показатель влияния'


from django.contrib import admin
from .models import AnalysisRequest, AnalysisArtifact

class AnalysisArtifactInline(admin.TabularInline):
    model = AnalysisArtifact
    extra = 1
    readonly_fields = ['calculated_score']
    fields = ['cultural_artifact', 'weight', 'analysis_depth', 'calculated_score']

@admin.register(AnalysisRequest)
class AnalysisRequestAdmin(admin.ModelAdmin):
    list_display = [
        'research_title', 
        'researcher_name', 
        'status', 
        'research_scope',
        'get_artifacts_count',
        'total_influence_score',
        'date_created'
    ]
    list_filter = ['status', 'research_scope', 'methodology', 'date_created']
    search_fields = ['research_title', 'researcher_name', 'description']
    readonly_fields = ['date_created', 'get_artifacts_count', 'progress_percentage']
    inlines = [AnalysisArtifactInline]
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'research_title', 
                'researcher_name', 
                'status', 
                'research_scope', 
                'methodology'
            )
        }),
        ('Показатели', {
            'fields': (
                'total_influence_score', 
                'get_artifacts_count',
                'progress_percentage'
            )
        }),
        ('Дополнительно', {
            'fields': ('description', 'completion_date', 'is_active', 'date_created')
        }),
    )

    def get_artifacts_count(self, obj):
        return obj.get_artifacts_count()
    get_artifacts_count.short_description = 'Кол-во артефактов'

@admin.register(AnalysisArtifact)
class AnalysisArtifactAdmin(admin.ModelAdmin):
    list_display = [
        'cultural_artifact',
        'analysis_request', 
        'weight', 
        'analysis_depth',
        'weighted_influence',
 
    ]
    list_filter = ['analysis_depth' ]
    search_fields = [
        'cultural_artifact__title', 
        'analysis_request__research_title'
    ]
    readonly_fields = ['calculated_score', 'weighted_influence']