# app/management/commands/load_cultural_artifacts.py
# python manage.py load_cultural_artifacts

from django.core.management.base import BaseCommand
from app.models import CulturalArtifact

class Command(BaseCommand):
    help = 'Load initial cultural artifacts data'

    def handle(self, *args, **options):
        cultural_artifacts = [
            {
                "id": 1,
                "title": "Метро 2033",
                "author": "Дмитрий Глуховский",
                "description": "Постапокалиптический роман, породивший медиафраншизу и оказавший значительное влияние на современную русскую фантастику",
                "publication_year": "2005",
                "genre": "POST_APOCALYPTIC",
                "base_influence_score": 410,
                "citation_count": 150,
                "media_mentions": 95,
                "social_media_score": 85,
                "adaptation_count": 3,
                "image": "http://localhost:9000/images/metro2033.png",
                "video": "http://localhost:9000/images/metro2033.mp4",
            },
            {
                "id": 2,
                "title": "Игра престолов", 
                "author": "Джордж Р.Р. Мартин",
                "description": "Эпический фэнтези-сериал, ставший глобальным культурным феноменом и изменивший телевизионную индустрию",
                "publication_year": "2011",
                "genre": "FANTASY",
                "base_influence_score": 920,
                "citation_count": 320,
                "media_mentions": 450,
                "social_media_score": 380,
                "adaptation_count": 1,
                "image": "http://localhost:9000/images/got.png",
                "video": "http://localhost:9000/images/got.mp4",
            },
            {
                "id": 3,
                "title": "Оно",
                "author": "Стивен Кинг",
                "description": "Культовый роман ужасов, образ Пеннивайза стал одним из самых узнаваемых в поп-культуре",
                "publication_year": "1986",
                "genre": "OTHER",
                "base_influence_score": 900,
                "citation_count": 280,
                "media_mentions": 320,
                "social_media_score": 410,
                "adaptation_count": 2,
                "image": "http://localhost:9000/images/it.png",
                "video": "http://localhost:9000/images/it.mp4",
            },
            {
                "id": 4,
                "title": "MrBeast",
                "author": "Джимми Дональдсон", 
                "description": "YouTube-создатель, изменивший подход к созданию контента и филантропии в цифровой среде",
                "publication_year": "2012",
                "genre": "OTHER",
                "base_influence_score": 950,
                "citation_count": 45,
                "media_mentions": 280,
                "social_media_score": 890,
                "adaptation_count": 0,
                "image": "http://localhost:9000/images/mrbeast.png",
                "video": "http://localhost:9000/images/mrbeast.mp4",
            },
            {
                "id": 5,
                "title": "Comedy Club",
                "author": "Гарик Мартиросян, Артур Джанибекян",
                "description": "Юмористическое шоу, сформировавшее язык и юмор целого поколения в России",
                "publication_year": "2005", 
                "genre": "OTHER",
                "base_influence_score": 780,
                "citation_count": 120,
                "media_mentions": 310,
                "social_media_score": 290,
                "adaptation_count": 15,
                "image": "http://localhost:9000/images/comedyclub.png",
                "video": "http://localhost:9000/images/comedyclub.mp4",
            },
            {
                "id": 6,
                "title": "Офис (The Office)",
                "author": "Грег Дэниелс",
                "description": "Ситком, определивший формат мокьюментари и ставший источником бесчисленных мемов",
                "publication_year": "2005",
                "genre": "OTHER",
                "base_influence_score": 890,
                "citation_count": 210,
                "media_mentions": 190,
                "social_media_score": 670,
                "adaptation_count": 8,
                "image": "http://localhost:9000/images/office.png",
                "video": "http://localhost:9000/images/office.mp4",
            }
        ]

        created_count = 0
        updated_count = 0

        for artifact_data in cultural_artifacts:
            # Удаляем id из данных, так как Django сам управляет первичными ключами
            artifact_id = artifact_data.pop('id')
            
            obj, created = CulturalArtifact.objects.update_or_create(
                id=artifact_id,
                defaults=artifact_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создан артефакт: {obj.title}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Обновлен артефакт: {obj.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно загружено {created_count} новых и обновлено {updated_count} существующих артефактов'
            )
        )