from django import forms


class MinimumRequiredFormSet(forms.models.BaseInlineFormSet):
    """
    Inline formset that enforces a minimum number of non-deleted forms
    that are not empty
    """
    default_minimum_forms_message = "At least %s set%s of data is required"

    def __init__(self, *args, **kwargs):
        self.minimum_forms = kwargs.pop('minimum_forms', 0)
        minimum_forms_message = kwargs.pop('minimum_forms_message', None)
        if minimum_forms_message:
            self.minimum_forms_message = minimum_forms_message
        else:
            self.minimum_forms_message = \
                self.default_minimum_forms_message % (
                    self.minimum_forms,
                    '' if self.minimum_forms == 1 else 's'
                )

        super(MinimumRequiredFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        non_deleted_forms = self.total_form_count()
        non_empty_forms = 0
        for i in xrange(0, self.total_form_count()):
            form = self.forms[i]
            if self.can_delete and self._should_delete_form(form):
                non_deleted_forms -= 1
            if not (form.instance.id is None and not form.has_changed()):
                non_empty_forms += 1
        if (
            non_deleted_forms < self.minimum_forms
            or non_empty_forms < self.minimum_forms
        ):
            raise forms.ValidationError(self.minimum_forms_message)
