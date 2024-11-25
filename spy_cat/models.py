from django.db import models


class SpyCat(models.Model):
    name = models.CharField(max_length=200)
    year_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Mission(models.Model):
    cat = models.OneToOneField(
        SpyCat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission {self.id}"


class Target(models.Model):
    mission = models.ForeignKey(
        Mission,
        related_name="targets",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
