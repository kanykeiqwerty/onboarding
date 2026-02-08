from rest_framework import serializers
from django.utils import timezone
from .models import OnboardingDay, OnboardingMedia, DailyReport


class OnboardingMediaSerializer(serializers.ModelSerializer):
    """Сериализатор для медиа-материалов"""
    media_type_display = serializers.CharField(source='get_media_type_display', read_only=True)

    class Meta:
        model = OnboardingMedia
        fields = ['id', 'media_type', 'media_type_display', 'title', 'link', 'file', 'order']
        read_only_fields = ['id']


class OnboardingDayListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка дней онбординга"""

    class Meta:
        model = OnboardingDay
        fields = ['id', 'day_number', 'title', 'deadline_time', 'is_active']
        read_only_fields = ['id']


class OnboardingDayDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор дня онбординга с материалами"""
    media_materials = OnboardingMediaSerializer(many=True, read_only=True)

    class Meta:
        model = OnboardingDay
        fields = [
            'id', 'day_number', 'title', 'description', 'instructions',
            'deadline_time', 'media_materials', 'is_active'
        ]
        read_only_fields = ['id']


class DailyReportSerializer(serializers.ModelSerializer):
    """Сериализатор для отчётов стажёра"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    intern_email = serializers.EmailField(source='intern.email', read_only=True)
    intern_name = serializers.SerializerMethodField()
    day_title = serializers.CharField(source='onboarding_day.title', read_only=True)
    day_number = serializers.IntegerField(source='onboarding_day.day_number', read_only=True)

    class Meta:
        model = DailyReport
        fields = [
            'id', 'intern', 'intern_email', 'intern_name',
            'onboarding_day', 'day_number', 'day_title',
            'what_done', 'what_will_do', 'problems',
            'attachment_link', 'attachment_file',
            'status', 'status_display',
            'created_at', 'submitted_at',
            'reviewer', 'reviewer_comment', 'reviewed_at'
        ]
        read_only_fields = [
            'id', 'intern', 'status', 'created_at', 'submitted_at',
            'reviewer', 'reviewer_comment', 'reviewed_at'
        ]

    def get_intern_name(self, obj):
        return f"{obj.intern.first_name} {obj.intern.last_name}".strip() or obj.intern.email

    def validate(self, data):
        """Валидация при создании/обновлении"""
        # Проверяем, что не пытаются изменить отчёт не в статусе draft
        if self.instance and self.instance.status != 'draft':
            raise serializers.ValidationError(
                'Можно редактировать только отчёты в статусе "Черновик"'
            )
        return data


class DailyReportCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отчёта"""

    class Meta:
        model = DailyReport
        fields = [
            'onboarding_day', 'what_done', 'what_will_do', 'problems',
            'attachment_link', 'attachment_file'
        ]

    def create(self, validated_data):
        # Автоматически привязываем к текущему пользователю
        validated_data['intern'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        """Проверка на дубликат отчёта"""
        request = self.context.get('request')
        onboarding_day = data.get('onboarding_day')

        if DailyReport.objects.filter(
            intern=request.user,
            onboarding_day=onboarding_day
        ).exists():
            raise serializers.ValidationError(
                'Вы уже создали отчёт для этого дня. Отредактируйте существующий.'
            )

        return data


class DailyReportSubmitSerializer(serializers.Serializer):
    """Сериализатор для отправки отчёта на проверку"""

    def validate(self, data):
        report = self.instance

        if report.status != 'draft':
            raise serializers.ValidationError('Можно отправить только черновик')

        if report.is_empty():
            raise serializers.ValidationError(
                'Все три поля отчёта (что сделал, что буду делать, проблемы) обязательны'
            )

        return data

    def save(self):
        self.instance.submit()
        return self.instance


class DailyReportReviewSerializer(serializers.Serializer):
    """Сериализатор для проверки отчёта администратором"""
    action = serializers.ChoiceField(
        choices=['accept', 'revision', 'reject'],
        required=True,
        help_text='accept - принять, revision - на доработку, reject - отклонить'
    )
    comment = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Комментарий (обязателен для revision)'
    )

    def validate(self, data):
        action = data.get('action')
        comment = data.get('comment', '')

        # Комментарий обязателен для "на доработку"
        if action == 'revision' and not comment.strip():
            raise serializers.ValidationError({
                'comment': 'Комментарий обязателен при отправке на доработку'
            })

        # Проверяем статус отчёта (если instance существует)
        if self.instance and self.instance.status not in ['submitted', 'revision']:
            raise serializers.ValidationError(
                'Можно проверить только отправленные отчёты или отчёты на доработке'
            )

        return data

    def save(self):
        if not self.instance:
            raise serializers.ValidationError('Отчёт не найден')

        action = self.validated_data['action']
        comment = self.validated_data.get('comment', '')
        reviewer = self.context['request'].user

        if action == 'accept':
            self.instance.accept(reviewer, comment)
        elif action == 'revision':
            self.instance.request_revision(reviewer, comment)
        elif action == 'reject':
            self.instance.reject(reviewer, comment)

        return self.instance


class DailyReportAdminSerializer(serializers.ModelSerializer):
    """Расширенный сериализатор для админ-панели"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    intern_email = serializers.EmailField(source='intern.email', read_only=True)
    intern_name = serializers.SerializerMethodField()
    reviewer_email = serializers.EmailField(source='reviewer.email', read_only=True)
    day_title = serializers.CharField(source='onboarding_day.title', read_only=True)

    class Meta:
        model = DailyReport
        fields = '__all__'

    def get_intern_name(self, obj):
        return f"{obj.intern.first_name} {obj.intern.last_name}".strip() or obj.intern.email
from rest_framework import serializers
from django.utils import timezone
from .models import OnboardingDay, OnboardingMedia, DailyReport


class OnboardingMediaSerializer(serializers.ModelSerializer):
    """Сериализатор для медиа-материалов"""
    media_type_display = serializers.CharField(source='get_media_type_display', read_only=True)

    class Meta:
        model = OnboardingMedia
        fields = ['id', 'media_type', 'media_type_display', 'title', 'link', 'file', 'order']
        read_only_fields = ['id']


class OnboardingDayListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка дней онбординга"""

    class Meta:
        model = OnboardingDay
        fields = ['id', 'day_number', 'title', 'deadline_time', 'is_active']
        read_only_fields = ['id']


class OnboardingDayDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор дня онбординга с материалами"""
    media_materials = OnboardingMediaSerializer(many=True, read_only=True)

    class Meta:
        model = OnboardingDay
        fields = [
            'id', 'day_number', 'title', 'description', 'instructions',
            'deadline_time', 'media_materials', 'is_active'
        ]
        read_only_fields = ['id']


class DailyReportSerializer(serializers.ModelSerializer):
    """Сериализатор для отчётов стажёра"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    intern_email = serializers.EmailField(source='intern.email', read_only=True)
    intern_name = serializers.SerializerMethodField()
    day_title = serializers.CharField(source='onboarding_day.title', read_only=True)
    day_number = serializers.IntegerField(source='onboarding_day.day_number', read_only=True)

    class Meta:
        model = DailyReport
        fields = [
            'id', 'intern', 'intern_email', 'intern_name',
            'onboarding_day', 'day_number', 'day_title',
            'what_done', 'what_will_do', 'problems',
            'attachment_link', 'attachment_file',
            'status', 'status_display',
            'created_at', 'submitted_at',
            'reviewer', 'reviewer_comment', 'reviewed_at'
        ]
        read_only_fields = [
            'id', 'intern', 'status', 'created_at', 'submitted_at',
            'reviewer', 'reviewer_comment', 'reviewed_at'
        ]

    def get_intern_name(self, obj):
        return f"{obj.intern.first_name} {obj.intern.last_name}".strip() or obj.intern.email

    def validate(self, data):
        """Валидация при создании/обновлении"""
        # Проверяем, что не пытаются изменить отчёт не в статусе draft
        if self.instance and self.instance.status != 'draft':
            raise serializers.ValidationError(
                'Можно редактировать только отчёты в статусе "Черновик"'
            )
        return data


class DailyReportCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отчёта"""

    class Meta:
        model = DailyReport
        fields = [
            'onboarding_day', 'what_done', 'what_will_do', 'problems',
            'attachment_link', 'attachment_file'
        ]

    def create(self, validated_data):
        # Автоматически привязываем к текущему пользователю
        validated_data['intern'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        """Проверка на дубликат отчёта"""
        request = self.context.get('request')
        onboarding_day = data.get('onboarding_day')

        if DailyReport.objects.filter(
            intern=request.user,
            onboarding_day=onboarding_day
        ).exists():
            raise serializers.ValidationError(
                'Вы уже создали отчёт для этого дня. Отредактируйте существующий.'
            )

        return data


class DailyReportSubmitSerializer(serializers.Serializer):
    """Сериализатор для отправки отчёта на проверку"""

    def validate(self, data):
        report = self.instance

        if not report:
            raise serializers.ValidationError('Отчёт не найден')

        if report.status != 'draft':
            raise serializers.ValidationError('Можно отправить только черновик')

        if report.is_empty():
            raise serializers.ValidationError(
                'Все три поля отчёта (что сделал, что буду делать, проблемы) обязательны'
            )

        return data

    def save(self):
        if self.instance:
            self.instance.submit()
        return self.instance


class DailyReportReviewSerializer(serializers.Serializer):
    """Сериализатор для проверки отчёта администратором"""
    action = serializers.ChoiceField(
        choices=['accept', 'revision', 'reject'],
        required=True,
        help_text='accept - принять, revision - на доработку, reject - отклонить'
    )
    comment = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Комментарий (обязателен для revision)'
    )

    def validate(self, data):
        action = data.get('action')
        comment = data.get('comment', '')

        # Комментарий обязателен для "на доработку"
        if action == 'revision' and not comment.strip():
            raise serializers.ValidationError({
                'comment': 'Комментарий обязателен при отправке на доработку'
            })

        # Проверяем статус отчёта
        if self.instance.status not in ['submitted', 'revision']:
            raise serializers.ValidationError(
                'Можно проверить только отправленные отчёты или отчёты на доработке'
            )

        return data

    def save(self):
        action = self.validated_data['action']
        comment = self.validated_data.get('comment', '')
        reviewer = self.context['request'].user

        if action == 'accept':
            self.instance.accept(reviewer, comment)
        elif action == 'revision':
            self.instance.request_revision(reviewer, comment)
        elif action == 'reject':
            self.instance.reject(reviewer, comment)

        return self.instance


class DailyReportAdminSerializer(serializers.ModelSerializer):
    """Расширенный сериализатор для админ-панели"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    intern_email = serializers.EmailField(source='intern.email', read_only=True)
    intern_name = serializers.SerializerMethodField()
    reviewer_email = serializers.EmailField(source='reviewer.email', read_only=True)
    day_title = serializers.CharField(source='onboarding_day.title', read_only=True)

    class Meta:
        model = DailyReport
        fields = '__all__'

    def get_intern_name(self, obj):
        return f"{obj.intern.first_name} {obj.intern.last_name}".strip() or obj.intern.email

