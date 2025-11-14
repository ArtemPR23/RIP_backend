# your_app/management/commands/load_analysis_requests.py
from django.core.management.base import BaseCommand
from app.models import AnalysisRequest, AnalysisArtifact, CulturalArtifact
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = 'Load initial analysis requests data'

    def handle(self, *args, **options):
        analysis_request_data = {
            "id": 123,
            "status": "DRAFT",
            "date_created": "12 сентября 2024г",
            "research_title": "Анализ влияния современных медиафеноменов",
            "researcher_name": "Иванов И.И.",
            "research_scope": "GLOBAL",
            "methodology": "CITATION_ANALYSIS",
            "total_influence_score": 3850,
            "artifacts": [
                {
                    "id": 1,
                    "weight": 0.3,
                    "analysis_depth": "EXTENDED"
                },
                {
                    "id": 2, 
                    "weight": 0.4,
                    "analysis_depth": "BASIC"
                },
                {
                    "id": 3,
                    "weight": 0.3,
                    "analysis_depth": "EXTENDED"
                }
            ]
        }

        # Создаем запрос анализа
        request_id = analysis_request_data.pop('id')
        artifacts_data = analysis_request_data.pop('artifacts')
        
        # Преобразуем дату (если нужно использовать конкретную дату)
        # Используем auto_now_add, но если нужна конкретная дата:
        custom_date = timezone.now()  # или timezone.make_aware(datetime(2024, 9, 12))

        analysis_request, created = AnalysisRequest.objects.update_or_create(
            id=request_id,
            defaults={
                **analysis_request_data,
                # 'date_created': custom_date,  #  если нужна конкретная дата
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Создан запрос анализа: {analysis_request.research_title}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Обновлен запрос анализа: {analysis_request.research_title}')
            )

        # Добавляем артефакты анализа
        artifacts_count = 0
        for artifact_data in artifacts_data:
            cultural_artifact_id = artifact_data['id']
            
            try:
                cultural_artifact = CulturalArtifact.objects.get(id=cultural_artifact_id)
                
                analysis_artifact, art_created = AnalysisArtifact.objects.update_or_create(
                    analysis_request=analysis_request,
                    cultural_artifact=cultural_artifact,
                    defaults={
                        'weight': artifact_data['weight'],
                        'analysis_depth': artifact_data['analysis_depth']
                    }
                )
                
                if art_created:
                    artifacts_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Добавлен артефакт: {cultural_artifact.title}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Обновлен артефакт: {cultural_artifact.title}')
                    )
                    
            except CulturalArtifact.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Культурный артефакт с id {cultural_artifact_id} не найден')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создан запрос анализа с {artifacts_count} артефактами'
            )
        )