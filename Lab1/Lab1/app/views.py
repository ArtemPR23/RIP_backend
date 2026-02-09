from django.shortcuts import render

cultural_artifacts = [
    {
        "id": 1,
        "title": "Метро 2033",
        "author": "Дмитрий Глуховский",
        "description": "Постапокалиптический роман, породивший медиафраншизу и оказавший значительное влияние на современную русскую фантастику",
        "publication_year": "2005",
        "genre": "Постапокалиптическая фантастика",
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
        "genre": "Фэнтези, драма",
        "base_influence_score": 920,
        "citation_count": 320,
        "media_mentions": 450,
        "social_media_score": 380,
        "adaptation_count": 1,
        "image": "http://localhost:9000/images/got.png",
        "video": "http://localhost:9000/images/got.png",
    },
    {
        "id": 3,
        "title": "Оно",
        "author": "Стивен Кинг",
        "description": "Культовый роман ужасов, образ Пеннивайза стал одним из самых узнаваемых в поп-культуре",
        "publication_year": "1986",
        "genre": "Хоррор",
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
        "genre": "Новые медиа",
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
        "genre": "Юмористическое шоу",
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
        "genre": "Ситком",
        "base_influence_score": 890,
        "citation_count": 210,
        "media_mentions": 190,
        "social_media_score": 670,
        "adaptation_count": 8,
        "image": "http://localhost:9000/images/office.png",
        "video": "http://localhost:9000/images/office.mp4",
    }
]


citation_request = {
    "id": 123,
    "status": "Черновик",
    "date_created": "12 сентября 2024г",
    "research_title": "Анализ влияния современных медиафеноменов",
    "researcher_name": "Иванов И.И.",
    "research_scope": "глобальный",
    "methodology": "комплексный анализ цитирований",
    "total_influence_score": 3850,
    "artifacts": [
        {
            "id": 1,
            "weight": 0.3,
            "analysis_depth": "расширенный"
        },
        {
            "id": 2, 
            "weight": 0.4,
            "analysis_depth": "базовая"
        },
        {
            "id": 3,
            "weight": 0.3,
            "analysis_depth": "расширенный"
        }
    ]
}


def get_artifact_by_id(artifact_id):
    for artifact in cultural_artifacts:
        if artifact["id"] == artifact_id:
            return artifact


def get_artifacts():
    return cultural_artifacts


def search_artifacts(search_query):
    res = []
    
    for artifact in cultural_artifacts:
        if (search_query.lower() in artifact["title"].lower() or 
            search_query.lower() in artifact["author"].lower() or
            search_query.lower() in artifact["genre"].lower()):
            res.append(artifact)
    
    return res


def get_citation_request():
    return citation_request


def get_citation_request_by_id(request_id):
    return citation_request


def index(request):
    search_query = request.GET.get("search", "")
    artifacts = search_artifacts(search_query) if search_query else get_artifacts()
    current_request = get_citation_request()
    
    context = {
        "artifacts": artifacts,
        "search_query": search_query,
        "artifacts_count": len(current_request["artifacts"]),
        "current_request": current_request
    }
    
    return render(request, "artifact_list.html", context)


def artifact_detail(request, artifact_id):
    context = {
        "id": artifact_id,
        "artifact": get_artifact_by_id(artifact_id),
    }
    
    return render(request, "artifact_detail.html", context)


def request_detail(request, request_id):
    citation_request = get_citation_request_by_id(request_id)
    artifacts = [
        {**get_artifact_by_id(artifact["id"]), 
         "weight": artifact["weight"],
         "analysis_depth": artifact["analysis_depth"]}
        for artifact in citation_request["artifacts"]
    ]
    
    context = {
        "citation_request": citation_request,
        "artifacts": artifacts
    }
    
    return render(request, "request_detail.html", context)