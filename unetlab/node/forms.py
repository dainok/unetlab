from ui.forms import ObjectModelForm
from node.models import NodeTemplate


class NodeTemplateForm(ObjectModelForm):
    class Meta:
        model = NodeTemplate
        fields = "__all__"
