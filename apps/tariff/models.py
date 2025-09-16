from django.db import models
from django.db.models import Case
from django.db.models import F
from django.db.models import Value
from django.db.models import When
from django.db.models.functions import Length
from django.db.models.lookups import Exact
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey
from tinymce.models import HTMLField

# Create your models here.


class Tariff(MPTTModel):
    class ItemTypeChoices(models.TextChoices):
        SECTION = "section", _("Bölüm")
        CHAPTER = "chapter", _("Fasıl")
        POSITION = "position", _("Pozisyon")
        SUBPOSITION = "subposition", _("Alt Pozisyon : AS Nomanklatüre Kod")
        COMBINENOM = "combinenom", _("Kombine Nomanklatüre Kod")
        NAT = "national", _("Milli Alt Açılım Kodu")
        STATS = "stats", _("İstatistik Kod")
        NAN = "nan", _("Not Selected")

    class MetricUnitChoices(models.TextChoices):
        GT = "GT", _("Gross ton")
        CK = "c/k", _("Karat (1 metrik karat=2*10-4 kg)")
        CEEL = "ce/el", _("Hücre adedi")
        CTL = "ct/l", _("Ton başına taşıma kapasitesi(1)")
        G = "g", _("Gram")
        GI = "gi F/S", _("Gram olarak fissile izotop ")
        KGH2O2 = "kg H2O2", _("Kilogram olarak Hidrojen peroksit")
        KGK20 = "kg K2O", _("Kilogram olarak Potasyum oksit ")
        KGKOH = "kg KOH", _("Kilogram olarak Potasyum hidroksit (kostik potas) ")
        KGMETAM = "kg met.am.", _("Kilogram olarak Metil aminler ")
        KGN = "kg N", _("Kilogram olarak Azot")
        KGNAOH = "Kg NaOH", _("Kilogram olarak Sodyum hidroksit (kostik soda)")
        KGNETEDA = "kg/net eda", _("Kilogram olarak kurutulmuş net ağırlık")
        KGP205 = "kg P2O5", _("Kilogram olarak Difosfor pentaoksit ")
        KG90SDT = "kg %90 sdt", _("Kilogram olarak % 90 kuru ürün")
        KGU = "kg U", _("Kilogram olarak Uranyum")
        KWH1000 = "1000 kWh", _("1000 kilovat saat")
        L = "l", _("Litre")
        KGC5H14CINO = "Kg C5H14CINO", _("Kilogram olarak Kolin klorür")
        LALC100 = "l alc. %100", _("Litre olarak saf alkol (%100) ")
        M = "m", _("Metre")
        M2 = "m2", _("Metre kare")
        M3 = "m3", _("Metre küp")
        M31000 = "1000 m3", _("1000 Metre küp")
        PA = "p/a", _("Çift")
        PST = "p/st", _("Adet")
        PST100 = "100 p/st", _("100 Adet")
        PST1000 = "1000 p/st", _("1000 Adet")
        TJ = "TJ", _("Terajul (Brüt kalori değeri)")
        TCO2 = "t. CO2", _("Ton CO2 (karbon dioksit) eşdeğeri")
        NA = "n/a", _("Not specified")

    position_number = models.CharField(
        _("Position Number"),
        max_length=12,
        help_text=_("Position Number"),
        blank=True,
        null=True,
    )
    item_definition = models.CharField(
        _("Definition"),
        help_text=_("Item Definition"),
        max_length=1500,
    )

    item_type = models.GeneratedField(
        expression=Case(
            When(
                Exact(Length(F("position_number")), 1),
                then=Value(ItemTypeChoices.SECTION),
            ),
            When(
                Exact(Length(F("position_number")), 2),
                then=Value(ItemTypeChoices.CHAPTER),
            ),
            When(
                Exact(Length(F("position_number")), 4),
                then=Value(ItemTypeChoices.POSITION),
            ),
            When(
                Exact(Length(F("position_number")), 6),
                then=Value(ItemTypeChoices.SUBPOSITION),
            ),
            When(
                Exact(Length(F("position_number")), 8),
                then=Value(ItemTypeChoices.COMBINENOM),
            ),
            When(
                Exact(Length(F("position_number")), 10),
                then=Value(ItemTypeChoices.NAT),
            ),
            When(
                Exact(Length(F("position_number")), 12),
                then=Value(ItemTypeChoices.STATS),
            ),
            default=Value(ItemTypeChoices.NAN),
            output_field=models.CharField(
                max_length=50,
                choices=ItemTypeChoices.choices,
            ),
        ),
        output_field=models.CharField(max_length=50, choices=ItemTypeChoices.choices),
        db_persist=True,
    )

    notes = HTMLField(_("Notes"), help_text=_("Item notes"), blank=True, null=True)
    metric_unit = models.CharField(
        _("Metric Unit"),
        max_length=50,
        choices=MetricUnitChoices.choices,
        default=MetricUnitChoices.NA,
        help_text=_("Item metric unit"),
    )
    tax_limit = models.FloatField(
        _("Tax Limit"),
        blank=True,
        default=0,
        help_text=_("Item Tax Limit"),
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    class MPTTMeta:
        order_insertion_by = ["position_number", "item_definition"]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="position_number_uniquie_constraint",
                fields=["position_number"],
                nulls_distinct=True,
            ),
        ]

    def __str__(self):
        return f"{self.position_number or '*'} {self.item_definition}"
