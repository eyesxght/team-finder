from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .constants import ProjectStatus
from .forms import ProjectForm
from .models import Project
from .services import get_paginated_queryset


def project_list_view(request):
    """Главная страница - список всех проектов."""
    projects_qs = (
        Project.objects.all()
        .select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )
    page_obj = get_paginated_queryset(projects_qs, request)
    return render(request, 'projects/project_list.html', {'projects': page_obj})


def project_detail_view(request, pk):
    """Страница проекта."""
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        pk=pk,
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project_view(request):
    """Создание нового проекта."""
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': False,
    })


@login_required
def edit_project_view(request, pk):
    """Редактирование проекта."""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('projects:detail', pk=project.pk)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': True,
    })


@login_required
@require_POST
def complete_project_view(request, pk):
    """Завершение проекта (только владелец)."""
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.status == ProjectStatus.OPEN:
        project.status = ProjectStatus.CLOSED
        project.save()
        return JsonResponse({
            'status': 'ok',
            'project_status': ProjectStatus.CLOSED,
        })
    return JsonResponse({'status': 'error'}, status=HTTPStatus.BAD_REQUEST)


@login_required
@require_POST
def toggle_participate_view(request, pk):
    """Участие в проекте (добавить/удалить)."""
    project = get_object_or_404(Project, pk=pk)
    if is_participating := project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({
        'status': 'ok',
        'is_participating': not is_participating,
    })


@login_required
@require_POST
def toggle_favorite_view(request, pk):
    """Добавление/удаление из избранного."""
    project = get_object_or_404(Project, pk=pk)
    if is_favorited := project.interested_users.filter(pk=request.user.pk).exists():
        project.interested_users.remove(request.user)
    else:
        project.interested_users.add(request.user)
    return JsonResponse({
        'status': 'ok',
        'favorited': not is_favorited,
    })


@login_required
def favorite_projects_view(request):
    """Страница избранных проектов."""
    projects_qs = (
        request.user.favorites.all()
        .select_related('owner')
        .prefetch_related('participants')
        .order_by('-created_at')
    )
    page_obj = get_paginated_queryset(projects_qs, request)
    return render(request, 'projects/favorite_projects.html', {'projects': page_obj})
