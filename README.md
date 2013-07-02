It is a fork of https://github.com/tttallis/django-singletons
Django 1.5 python 2.7 compatible.

Installation
============

<pre>pip install django-singletons</pre>

To get the custom admin templates working, you need to add "singleton_models" to your INSTALLED_APPS

Example Usage
=============

in models.py

<pre><code>
from singleton_models.models import SingletonModel

class HomePage(SingletonModel):
    welcome = models.TextField()
    
    def __unicode__(self):
        return u"The Home Page" # something like this will make admin message strings more coherent
        
    class Meta:
        verbose_name = "Home Page" # once again this will make sure your admin UI doesn't have illogical text
        verbose_name_plural = "Home Page"
</code></pre>

in admin.py

<pre><code>
from singleton_models.admin import SingletonModelAdmin
from models import HomePage
        
admin.site.register(HomePage, SingletonModelAdmin)
</code></pre>
