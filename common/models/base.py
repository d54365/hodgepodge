from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ForeignKey(models.ForeignKey):
    def __init__(
        self,
        to,
        on_delete=models.SET_NULL,
        related_name=None,
        related_query_name=None,
        limit_choices_to=None,
        parent_link=False,
        to_field=None,
        db_constraint=False,
        **kwargs,
    ):
        kwargs["null"] = True
        super().__init__(
            to,
            on_delete,
            related_name,
            related_query_name,
            limit_choices_to,
            parent_link,
            to_field,
            db_constraint,
            **kwargs,
        )


class ManyToManyField(models.ManyToManyField):
    def __init__(
        self,
        to,
        related_name=None,
        related_query_name=None,
        limit_choices_to=None,
        symmetrical=None,
        through=None,
        through_fields=None,
        db_constraint=False,
        db_table=None,
        swappable=True,
        **kwargs,
    ):
        super().__init__(
            to,
            related_name,
            related_query_name,
            limit_choices_to,
            symmetrical,
            through,
            through_fields,
            db_constraint,
            db_table,
            swappable,
            **kwargs,
        )


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._include_deleted_filtering = False

    def with_deleted_filtering(self, enable=True):
        self._include_deleted_filtering = not enable
        return self

    def get_queryset(self):
        if self._include_deleted_filtering:
            return super().get_queryset()

        return super().get_queryset().filter(is_delete=False)
