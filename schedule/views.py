from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, date
from calendar import monthcalendar
from .models import WorkScheduleType, UserSchedule, Holiday
from .serializers import (
    WorkScheduleTypeSerializer,
    UserScheduleSerializer,
    MyScheduleSerializer,
    HolidaySerializer
)


class WorkScheduleTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для типов графиков работы.

    GET /api/v1/schedule/types/ - список активных графиков
    GET /api/v1/schedule/types/{id}/ - детали графика
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkScheduleTypeSerializer

    def get_queryset(self):
        return WorkScheduleType.objects.filter(is_active=True)


class MyScheduleViewSet(viewsets.ViewSet):
    """
    ViewSet для просмотра и изменения своего графика работы.

    GET /api/v1/schedule/my/ - мой график
    PUT /api/v1/schedule/my/ - изменить график
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Получить свой график"""
        try:
            schedule = UserSchedule.objects.select_related('schedule_type').get(user=request.user)
            serializer = MyScheduleSerializer(schedule)
            return Response(serializer.data)
        except UserSchedule.DoesNotExist:
            # Если графика нет, возвращаем график по умолчанию
            default_schedule = WorkScheduleType.objects.filter(is_default=True).first()
            if default_schedule:
                return Response({
                    'message': 'График не назначен. Используется график по умолчанию.',
                    'schedule_details': WorkScheduleTypeSerializer(default_schedule).data
                })
            return Response({
                'message': 'График работы не назначен'
            }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request):
        """Изменить свой график"""
        schedule_type_id = request.data.get('schedule_type')

        if not schedule_type_id:
            return Response(
                {'error': 'Укажите schedule_type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            schedule_type = WorkScheduleType.objects.get(id=schedule_type_id, is_active=True)
        except WorkScheduleType.DoesNotExist:
            return Response(
                {'error': 'График не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        schedule, created = UserSchedule.objects.update_or_create(
            user=request.user,
            defaults={'schedule_type': schedule_type}
        )

        serializer = MyScheduleSerializer(schedule)
        return Response({
            'message': 'График успешно обновлён' if not created else 'График успешно назначен',
            'schedule': serializer.data
        })


class HolidayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для праздников.

    GET /api/v1/schedule/holidays/ - список праздников
    GET /api/v1/schedule/holidays/?year=2026&month=2 - фильтр по месяцу
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HolidaySerializer
    queryset = Holiday.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')

        if year:
            queryset = queryset.filter(date__year=year)
        if month:
            queryset = queryset.filter(date__month=month)

        return queryset


class CalendarViewSet(viewsets.ViewSet):
    """
    ViewSet для календаря.

    GET /api/v1/schedule/calendar/?year=2026&month=2 - календарь месяца
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Получить календарь месяца"""
        year = request.query_params.get('year', datetime.now().year)
        month = request.query_params.get('month', datetime.now().month)

        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return Response(
                {'error': 'Неверный формат year или month'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем календарь месяца
        cal = monthcalendar(year, month)

        # Получаем праздники месяца
        holidays = Holiday.objects.filter(
            date__year=year,
            date__month=month
        )
        holiday_dict = {h.date.day: h for h in holidays}

        # Получаем график пользователя
        try:
            user_schedule = UserSchedule.objects.select_related('schedule_type').get(user=request.user)
            work_days = user_schedule.schedule_type.work_days
        except UserSchedule.DoesNotExist:
            # Используем график по умолчанию
            default = WorkScheduleType.objects.filter(is_default=True).first()
            work_days = default.work_days if default else [1, 2, 3, 4, 5]

        # Формируем календарь
        calendar_data = {
            'year': year,
            'month': month,
            'weeks': [],
            'holidays': HolidaySerializer(holidays, many=True).data
        }

        for week in cal:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append(None)
                else:
                    day_date = date(year, month, day)
                    day_of_week = day_date.isoweekday()  # 1=Пн, 7=Вс

                    holiday = holiday_dict.get(day)

                    day_info = {
                        'day': day,
                        'is_working': day_of_week in work_days,
                        'is_weekend': day_of_week not in work_days,
                        'is_holiday': holiday is not None,
                        'holiday_name': holiday.name if holiday else None
                    }

                    # Если это праздник с флагом "рабочий день"
                    if holiday and holiday.is_working_day:
                        day_info['is_working'] = True
                        day_info['is_weekend'] = False

                    week_data.append(day_info)

            calendar_data['weeks'].append(week_data)

        return Response(calendar_data)

