from django.db import models


class RealEstateAgent(models.Model):
    # Основная информация об агентстве
    agency_id = models.CharField(max_length=255, unique=True)  # Уникальный ID агентства
    agent_name = models.CharField(max_length=255, null=True, blank=True)  # Имя агента
    agency_phone = models.CharField(max_length=100, null=True, blank=True)  # Телефон агентства
    agency_email = models.EmailField(null=True, blank=True)  # Email агентства
    agency_email_address = models.EmailField(null=True, blank=True)  # Альтернативный email
    website_url = models.URLField(null=True, blank=True)  # Сайт агентства
    image = models.URLField(null=True, blank=True)  # URL изображения
    image_logo = models.URLField(null=True, blank=True)  # URL логотипа

    # Адрес и описание агентства
    agency_address = models.TextField(null=True, blank=True)  # Адрес агентства
    agency_description = models.TextField(null=True, blank=True)  # Описание агентства
    agency_association = models.CharField(max_length=255, null=True, blank=True)  # Ассоциации агентства
    agency_customer_reviews = models.TextField(null=True, blank=True)  # Отзывы клиентов
    customer_reviews = models.TextField(null=True, blank=True)  # Альтернативные отзывы

    # Рейтинг агентства
    rating = models.CharField(max_length=50, null=True, blank=True)  # Рейтинг
    rating_points = models.CharField(max_length=50, null=True, blank=True)  # Рейтинговые баллы
    number_of_reviews = models.IntegerField(null=True, blank=True)  # Количество отзывов

    # Сотрудники
    total_employees = models.CharField(max_length=50, null=True, blank=True)  # Общее количество сотрудников
    colleagues = models.TextField(null=True, blank=True)  # Коллеги (можно использовать JSON для структурированных данных)

    # Сертификаты и языки
    certificates = models.JSONField(null=True, blank=True)  # Сертификаты (хранятся в виде списка)
    languages = models.JSONField(null=True, blank=True)  # Языки, на которых говорит агентство

    # Социальные сети
    link_facebook = models.URLField(null=True, blank=True)  # Ссылка на Facebook
    link_instagram = models.URLField(null=True, blank=True)  # Ссылка на Instagram
    link_linkedin = models.URLField(null=True, blank=True)  # Ссылка на LinkedIn

    # Дополнительная информация
    association = models.TextField(null=True, blank=True)  # Ассоциации агентства
    affiliation = models.TextField(null=True, blank=True)  # Партнёрства или аффиляции

    def __str__(self):
        return f"{self.agent_name} ({self.agency_id})"

