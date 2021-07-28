from django.db import models

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
# from river.models.fields.state import StateField

class Tag(TagBase):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class TaggedCandidate(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class TaggedWebpick(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class Offer(models.Model):
    title = models.CharField("Intitulé", max_length=50)
    description = models.TextField("Description", null=True, blank=True)
    url = models.URLField("Url", null=True, blank=True)

    class Meta:
        verbose_name = 'Offre'
        verbose_name_plural = 'Offres'

    def __str__(self):
        return self.title


class ContractType(models.Model):
    title = models.CharField("Nom", max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Type de contrat'
        verbose_name_plural = 'Types de contrat'

class Candidate(models.Model):

    firstname = models.CharField("Prénom", max_length=50)
    lastname = models.CharField("Nom", max_length=50)
    email = models.EmailField("E-mail")
    phone = models.CharField("Numéro de téléphone", max_length=50, null=True, blank=True)
    ticket = models.URLField("Url du ticket")
    cv = models.FileField("CV", null=True, blank=True)
    motivation_file = models.FileField("Lettre de motivation en fichier", null=True, blank=True)
    description_text = models.TextField("Lettre de motivation en texte", null=True, blank=True)
    offer = models.ForeignKey('Offer', verbose_name="Offre", on_delete=models.PROTECT, null=True)
    contract_type = models.ForeignKey('ContractType', verbose_name="Type de contrat", on_delete=models.PROTECT)

    candidate_tags = TaggableManager("Tags du candidats", through=TaggedCandidate, related_name="candidate_tags", blank=True)
    webpick_tags = TaggableManager("Tags de qualification", through=TaggedWebpick, related_name="webpick_tags", blank=True)

    synthesis = models.TextField("Synthèse", null=True, blank=True)

    INBOX = 'inbox'
    QUALIFICATION_INITIALE = 'SO'
    QUALIFICATION_TECHNIQUE = 'JR'
    ENTRETIEN = 'entretien'
    REFUSE = 'refused'
    EMBAUCHE = 'hired'
    WORKFLOW_STATES = [
        (INBOX, 'Inbox'),
        (QUALIFICATION_INITIALE, 'Qualification initiale'),
        (QUALIFICATION_TECHNIQUE, 'Qualification technique'),
        (ENTRETIEN, 'Entretien'),
        (REFUSE, 'Refusé'),
        (EMBAUCHE, 'Embauché')
    ]
    state = models.CharField(
        max_length=20,
        choices=WORKFLOW_STATES,
        default=INBOX,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def fullname(self):
        return self.firstname + ' ' + self.lastname

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Candidat'
        verbose_name_plural = 'Candidats'