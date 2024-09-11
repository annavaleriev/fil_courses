from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class UserManager(BaseUserManager):
    """Класс для создания пользователей"""

    use_in_migrations = True  # Переменная для использования в миграциях

    def _create_user(
        self, email, password, **extra_fields
    ):  # Метод для создания пользователя
        if not email:  # Если email не указан
            raise ValueError(
                "У пользователя должен быть адрес электронной почты"
            )  # Выводим ошибку
        email = self.normalize_email(email)  # Нормализуем email
        user = self.model(email=email, **extra_fields)  # Создаем пользователя
        user.set_password(password)  # Хешируем пароль
        user.save(using=self._db)  # Сохраняем пользователя
        return user  # Возвращаем пользователя

    def create_user(
        self, email, password=None, **extra_fields
    ):  # Метод для создания пользователя
        extra_fields.setdefault(
            "is_staff", False
        )  # Устанавливаем значение по умолчанию
        extra_fields.setdefault(
            "is_superuser", False
        )  # Устанавливаем значение по умолчанию
        return self._create_user(
            email, password, **extra_fields
        )  # Создаем пользователя

    def create_superuser(
        self, email, password=None, **extra_fields
    ):  # Метод для создания суперпользователя
        extra_fields.setdefault("is_staff", True)  # Устанавливаем значение по умолчанию
        extra_fields.setdefault(
            "is_superuser", True
        )  # Устанавливаем значение по умолчанию

        if (
            extra_fields.get("is_staff") is not True
        ):  # Если пользователь не является сотрудником
            raise ValueError(
                "Суперпользователь должен иметь is_staff=True"
            )  # Выводим ошибку
        if (
            extra_fields.get("is_superuser") is not True
        ):  # Если пользователь не является суперпользователем
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True."
            )  # Выводим ошибку

        return self._create_user(
            email, password, **extra_fields
        )  # Создаем пользователя


class User(AbstractUser):
    """Класс для создания пользователей"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Введите адрес электронной почты"
    )
    phone = models.CharField(
        max_length=150,
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=150, verbose_name="Город", **NULLABLE, help_text="Введите город"
    )
    avatar = models.ImageField(
        upload_to="users/",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # Объект для работы с пользователями

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return f"Пользователь {self.email} {self.phone or ''}"


class Payment(models.Model):
    """Модель для платежей"""

    class Method(models.TextChoices):
        CASH = "cash", "Наличные"
        CARD = "card", "Перевод на счет"

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # удаление пользователя не приведет к удалению платежа
        **NULLABLE,
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")

    paid_course = models.ForeignKey(
        "materials.Course",
        **NULLABLE,
        on_delete=models.SET_NULL,  # удаление курса не приведет к удалению платежа
        verbose_name="Оплаченный курс",
    )

    paid_lesson = models.ForeignKey(
        "materials.Lesson",
        **NULLABLE,
        on_delete=models.SET_NULL,  # удаление урока не приведет к удалению платежа
        verbose_name="Оплаченный урок",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")

    payment_method = models.CharField(
        max_length=10, choices=Method.choices, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]  # Сортировка по убыванию даты платежа

    def __str__(self):
        return f"Платеж {self.amount} от {self.user.email}"
