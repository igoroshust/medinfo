from django.db import models


class People(models.Model):
    """Основная таблица с персональными данными"""

    enp = models.CharField(max_length=16, unique=True, verbose_name="ЕНП (полис)")
    fam = models.CharField(max_length=40, verbose_name="Фамилия")
    im = models.CharField(max_length=40, verbose_name="Имя")
    ot = models.CharField(max_length=40, blank=True, verbose_name="Отчество")
    w = models.SmallIntegerField(verbose_name="Пол (1-м, 2-ж)")
    dr = models.DateField(verbose_name="Дата рождения")

    # Поля прикрепления — ССЫЛКИ на справочники
    lpu = models.ForeignKey(
        "Lpu",
        on_delete=models.SET_NULL,  # при удалении ЛПУ — станет NULL
        null=True,
        blank=True,
        related_name="patients",
        verbose_name="Мед.организация",
    )
    lpuuch = models.ForeignKey(
        "T007",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients",
        verbose_name="Участок",
    )
    lpudt = models.DateField(null=True, blank=True, verbose_name="Дата прикрепления")  # Просто даты (не справочники), связь не нужна
    lpudx = models.DateField(null=True, blank=True, verbose_name="Дата открепления")

    def __str__(self):
        return f"{self.fam} {self.im} {self.ot}"


class HistLpu(models.Model):
    """История прикрепления"""

    pid = models.ForeignKey(
        People, on_delete=models.CASCADE, related_name="history"
    )  # многие записи HistLpu могут ссылаться на одного `People`
    lpu = models.ForeignKey(
        "Lpu", on_delete=models.SET_NULL, null=True, blank=True, related_name="history_lpu"
    )
    lpudt = models.DateField(null=True, blank=True, verbose_name="Дата прикрепления")
    lpudx = models.DateField(null=True, blank=True, verbose_name="Дата открепления")
    district = models.ForeignKey(
        "T001",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="history_districts",
        verbose_name="Подразделение",
    )
    subdiv = models.ForeignKey(
        "T007",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="history_subdivs",
        verbose_name="Участок",
    )

    def __str__(self):
        return f"{self.pid} — {self.lpu}"


class Lpu(models.Model):
    """Справочник мед.организаций"""

    code = models.CharField(max_length=6, unique=True)
    caption = models.CharField(max_length=100, verbose_name="Название")
    bossname = models.CharField(max_length=150, verbose_name="Главврач")

    def __str__(self):
        return f"{self.caption}"


class T001(models.Model):
    """Справочник подразделений"""

    mcod = models.ForeignKey(
        "Lpu",
        on_delete=models.CASCADE,
        related_name="subdivisions",
        verbose_name="Мед.организация",
    )
    nam_mo = models.CharField(max_length=100, verbose_name="Наименование подразделения")
    nom_podr = models.CharField(max_length=10, verbose_name="Код подразделения в мед.орг.")

    def __str__(self):
        return f"{self.mcod} — {self.nam_mo}"


class T007(models.Model):
    """Справочник участков"""

    code_mo = models.ForeignKey(
        "Lpu",
        on_delete=models.CASCADE,
        related_name="districts",
        verbose_name="Мед.организация",
    )
    name_depth = models.CharField(max_length=100, verbose_name="Наименование участка")
    nom_podr = models.CharField(max_length=10, verbose_name="Код подразделения в мед.орг.")
    depth = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code_mo} — {self.name_depth}"
