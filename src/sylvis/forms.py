from django.forms import CharField, DateField, DecimalField, ModelForm, TextInput
from django.utils.translation import gettext as _

from .models import Inventory, Section, Treatment


class AddFormBase(ModelForm):

    date = DateField(widget=TextInput(attrs={"type": "date", "placeholder": _("date")}))
    remarks = CharField(widget=TextInput(attrs={"placeholder": _("remarks")}))

    def __init__(self, plot_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.plot_id = plot_id


class AddSectionForm(AddFormBase):
    class Meta:
        model = Section
        fields = ["date", "remarks", "volume"]

    volume = DecimalField(widget=TextInput(attrs={"placeholder": _("volume")}))


class AddInventoryForm(AddFormBase):
    class Meta:
        model = Inventory
        fields = ["date", "remarks", "standing_volume"]

    standing_volume = DecimalField(
        widget=TextInput(attrs={"placeholder": _("standing volume")})
    )


class AddTreatmentForm(AddFormBase):
    class Meta:
        model = Treatment
        fields = ["date", "remarks", "description"]

    description = CharField(widget=TextInput(attrs={"placeholder": _("description")}))
