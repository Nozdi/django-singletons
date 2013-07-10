# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import HttpResponseRedirect
from django.utils.functional import update_wrapper

from django.conf.urls import patterns
from django.conf.urls import url

class SingletonModelAdmin(admin.ModelAdmin):
    
    change_form_template = "admin/singleton_models/change_form.html"
    object_history_template = "admin/singleton_models/object_history.html"

    def has_add_permission(self, request):
        """Singleton pattern: prevent addition of new objects."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Singleton pattern: prevent deletion of new objects."""
        return False
 
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns("",
            url(r'^history/$', wrap(self.history_view), {"object_id": "1"},\
                    name='%s_%s_history' % info),
            url(r"^(.+)/$", wrap(self.change_redirect),\
                     name = "%s_%s_change" % info),
            url(r"^$", wrap(self.change_view), {"object_id": "1"},\
                    name = "%s_%s_changelist" % info),
        )
        return urlpatterns
    

    def change_redirect(self, request, object_id, extra=None):
        from django.shortcuts import redirect
        info = self.model._meta.app_label, self.model._meta.module_name
        return redirect('admin:%s_%s_changelist' % info)

    def response_change(self, request, obj):
        """Determines the HttpResponse for the change_view stage."""
        opts = obj._meta

        msg = _("%s was changed successfully.") % force_unicode(obj)
        
        if request.POST.has_key("_continue"):
            self.message_user(request, "%s %s" % (msg, _("You may edit it again below.")))

            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            return HttpResponseRedirect("../../")

    def change_view(self, request, object_id, extra_context = None):
        if object_id == "1":
            self.model.objects.get_or_create(pk = 1)

        return super(SingletonModelAdmin, self).change_view(request,\
                object_id, extra_context=extra_context)
