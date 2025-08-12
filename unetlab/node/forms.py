from ui.forms import ObjectModelForm
from node.models import NodeTemplate
from repository.models import Repository
from django.core.exceptions import ValidationError


class NodeTemplateForm(ObjectModelForm):
    class Meta:
        model = NodeTemplate
        fields = "__all__"

    def clean(self):
        # TODO: validate repository is local or not set
        # CANNOT ADD OR MODIFY NON LOCAL REPOSITORY
        # if self.instance.pk:
        #     # Modify an existent instance
        #     # Check if repository is local
        #     # TODO
        #     pass

        local_repo = Repository.objects.get(name="local", is_enabled=True)
        # TODO: could fail

        cleaned_data = super().clean()
        vendor = cleaned_data.get("vendor")
        os = cleaned_data.get("os")
        version = cleaned_data.get("version")
        extra = cleaned_data.get("extra")

        qs = NodeTemplate.objects.filter(
            vendor=vendor,
            os=os,
            version=version,
            extra=extra,
            repository_id=local_repo.pk,
        )
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(
                "La combinazione di Vendor, OS, Version e Extra è già presente."
            )

        return cleaned_data
