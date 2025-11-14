from app.models import AnalysisArtifact, AnalysisRequest, CulturalArtifact
from django.db import connection
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone


def index(request):
    """Главная страница со списком артефактов"""
    search_query = request.GET.get("search", "")

    if search_query:
        artifacts = CulturalArtifact.objects.filter(
            Q(title__icontains=search_query)
            | Q(author__icontains=search_query)
            | Q(genre__icontains=search_query)
        ).filter(is_active=True)
    else:
        artifacts = CulturalArtifact.objects.filter(is_active=True)

    current_request = AnalysisRequest.objects.first()

    context = {
        "artifacts": artifacts,
        "search_query": search_query,
        "artifacts_count": current_request.artifacts.count() if current_request else 0,
        "current_request": current_request,
    }

    return render(request, "artifact_list.html", context)


def artifact_detail(request, artifact_id):
    """Детальная страница артефакта"""
    artifact = get_object_or_404(CulturalArtifact, id=artifact_id, is_active=True)

    # Получаем анализы, в которых участвует этот артефакт
    analysis_artifacts = AnalysisArtifact.objects.filter(
        cultural_artifact=artifact
    ).select_related("analysis_request")

    context = {"artifact": artifact, "analysis_artifacts": analysis_artifacts}

    return render(request, "artifact_detail.html", context)


def delete_artifact(request, artifact_id):
    if not CulturalArtifact.objects.filter(pk=artifact_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE app_culturalartifact SET is_active=False WHERE id = %s", [artifact_id])

    return redirect("/")


def add_artifact_to_draft_request(request, artifact_id):
    artifact = CulturalArtifact.objects.get(pk=artifact_id)

    draft_request = AnalysisRequest.objects.filter(status='DRAFT').first()

    if draft_request is None:
        draft_request = AnalysisRequest.objects.create()
        draft_request.owner = request.user
        draft_request.date_created = timezone.now()
        draft_request.save()

    if AnalysisArtifact.objects.filter(analysis_request=draft_request, cultural_artifact=artifact).exists():
        return redirect("/")

    item = AnalysisArtifact(
        analysis_request=draft_request, cultural_artifact=artifact
    )
    item.save()

    return redirect("/")

def del_artifact_to_draft_request(request, artifact_id):
    artifact = CulturalArtifact.objects.get(pk=artifact_id)

    draft_request = AnalysisRequest.objects.filter(status='DRAFT').first()
 

    if not AnalysisArtifact.objects.filter(analysis_request=draft_request, cultural_artifact=artifact).exists():
        return redirect("/")

    item = AnalysisArtifact.objects.filter(
        analysis_request=draft_request, cultural_artifact=artifact
    )
    item.delete()

    return redirect("/")


def request_detail(request, request_id):
    """Детальная страница запроса анализа"""
    analysis_request = get_object_or_404(AnalysisRequest, id=request_id)

    # Получаем артефакты с дополнительной информацией
    analysis_artifacts = AnalysisArtifact.objects.filter(
        analysis_request=analysis_request
    ).select_related("cultural_artifact")

    # Формируем список артефактов с весом и глубиной анализа
    artifacts_with_details = []
    for analysis_artifact in analysis_artifacts:
        artifacts_with_details.append(
            {
                "id": analysis_artifact.cultural_artifact.pk,
                "image": analysis_artifact.cultural_artifact.image,
                "cultural_artifact": analysis_artifact.cultural_artifact,
                "weight": analysis_artifact.weight,
                "analysis_depth": analysis_artifact.get_analysis_depth_display(),
                "calculated_score": analysis_artifact.calculated_score,
                "weighted_influence": analysis_artifact.weighted_influence,
            }
        )

    context = {
        "analysis_request": analysis_request,
        "artifacts": artifacts_with_details,
        "total_artifacts": analysis_artifacts.count(),
    }

    return render(request, "request_detail.html", context)



def request_list(request):
    """Список всех запросов анализа"""
    analysis_requests = AnalysisRequest.objects.all().prefetch_related("artifacts")

    context = {"analysis_requests": analysis_requests}

    return render(request, "request_list.html", context)
