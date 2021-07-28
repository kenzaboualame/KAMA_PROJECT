from rh.models import Candidate, ContractType, Offer, Tag
from django.contrib import admin
from dal import autocomplete
from dal_select2_taggit.widgets import TaggitSelect2


class StaffRequiredAdminMixin(object):

    def check_perm(self, user_obj):
        if not user_obj.is_active or user_obj.is_anonymous():
            return False
        if user_obj.is_superuser or user_obj.is_staff:
            return True
        return False

    def has_add_permission(self, request):
        return self.check_perm(request.user)

    def has_change_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_delete_permission(self, request, obj=None):
        return self.check_perm(request.user)

    def has_module_permission(self, request):
        return self.check_perm(request.user)


class CandidateForm(autocomplete.FutureModelForm):
    class Meta:
        model = Candidate
        exclude = ()
        widgets = {
            'candidate_tags': TaggitSelect2(
                'tags-autocomplete'
            ),
            'webpick_tags': TaggitSelect2(
                'tags-autocomplete'
            )
        }


class TagAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    pass


class ContractTypeAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    pass


class OfferAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'url')


class CandidateAdmin(StaffRequiredAdminMixin, admin.ModelAdmin):
    form = CandidateForm
    list_display = ('fullname', 'offer', 'email', 'state')
    list_filter = ('state', 'offer')
    search_fields = ('firstname', 'lastname', 'candidate_tags', 'webpick_tags', 'email')
    list_editable = ('state',)
    readonly_fields = ('created_date',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(ContractType, ContractTypeAdmin)
admin.site.register(Candidate, CandidateAdmin)
