from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from account.permission import IsAdmin
from .models import OnboardingDay, DailyReport
from .serializers import (
    OnboardingDayListSerializer,
    OnboardingDayDetailSerializer,
    DailyReportSerializer,
    DailyReportCreateSerializer,
    DailyReportSubmitSerializer,
    DailyReportReviewSerializer,
    DailyReportAdminSerializer
)


class OnboardingDayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для дней онбординга.

    GET /api/v1/onboarding/days/ - список активных дней
    GET /api/v1/onboarding/days/{id}/ - детали дня с материалами
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OnboardingDay.objects.filter(is_active=True).prefetch_related('media_materials')

    def get_serializer_class(self):
        if self.action == 'list':
            return OnboardingDayListSerializer
        return OnboardingDayDetailSerializer


class DailyReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet для ежедневных отчётов стажёров.

    Стажёры:
    - GET /api/v1/reports/my/ - мои отчёты
    - POST /api/v1/reports/ - создать отчёт
    - PUT/PATCH /api/v1/reports/{id}/ - обновить черновик
    - POST /api/v1/reports/{id}/submit/ - отправить на проверку

    Админы:
    - GET /api/v1/reports/all/ - все отчёты
    - PATCH /api/v1/reports/{id}/review/ - проверить отчёт
    """

    def get_permissions(self):
        # Просмотр всех отчётов и проверка - только админы
        if self.action in ['all_reports', 'review']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Для swagger генерации
        if getattr(self, 'swagger_fake_view', False):
            return DailyReport.objects.none()
        
        user = self.request.user
        
        # Админы видят все отчёты
        if user.is_staff or user.is_superuser:
            return DailyReport.objects.all().select_related(
                'intern', 'onboarding_day', 'reviewer'
            )
        
        # Стажёры видят только свои
        return DailyReport.objects.filter(intern=user).select_related(
            'onboarding_day', 'reviewer'
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return DailyReportCreateSerializer
        elif self.action == 'submit':
            return DailyReportSubmitSerializer
        elif self.action == 'review':
            return DailyReportReviewSerializer
        elif self.action == 'all_reports':
            return DailyReportAdminSerializer
        return DailyReportSerializer

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        """Обновление отчёта (только черновики)"""
        instance = self.get_object()

        # Проверяем права: стажёр может редактировать только свои отчёты
        if instance.intern != request.user and not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'Вы можете редактировать только свои отчёты'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Можно редактировать только черновики
        if instance.status != 'draft':
            return Response(
                {'error': 'Можно редактировать только черновики'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='my')
    def my_reports(self, request):
        """Мои отчёты (для стажёров)"""
        reports = self.get_queryset().filter(intern=request.user)
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='all', permission_classes=[IsAdmin])
    def all_reports(self, request):
        """Все отчёты (для админов)"""
        queryset = self.filter_queryset(self.get_queryset())

        # Фильтрация по статусу
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Фильтрация по стажёру
        intern_id = request.query_params.get('intern_id')
        if intern_id:
            queryset = queryset.filter(intern_id=intern_id)

        # Фильтрация по дню
        day_id = request.query_params.get('day_id')
        if day_id:
            queryset = queryset.filter(onboarding_day_id=day_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Отправить отчёт на проверку"""
        report = self.get_object()

        # Проверяем права
        if report.intern != request.user:
            return Response(
                {'error': 'Вы можете отправлять только свои отчёты'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(report, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Отчёт успешно отправлен на проверку',
            'report': DailyReportSerializer(report).data
        })

    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def review(self, request, pk=None):
        """Проверить отчёт (только админы)"""
        report = self.get_object()

        serializer = self.get_serializer(report, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        action_text = {
            'accept': 'принят',
            'revision': 'отправлен на доработку',
            'reject': 'отклонён'
        }

        return Response({
            'message': f'Отчёт {action_text.get(request.data.get("action"), "обработан")}',
            'report': DailyReportSerializer(report).data
        })

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """История изменений отчёта"""
        report = self.get_object()

        # Проверяем права
        if report.intern != request.user and not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {'error': 'Нет доступа'},
                status=status.HTTP_403_FORBIDDEN
            )

        history_data = {
            'report_id': report.id,
            'current_status': report.get_status_display(),
            'created_at': report.created_at,
            'submitted_at': report.submitted_at,
            'reviewed_at': report.reviewed_at,
            'reviewer': report.reviewer.email if report.reviewer else None,
            'reviewer_comment': report.reviewer_comment,
        }

        return Response(history_data)

