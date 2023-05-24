SYSTEM_PROMPT = """You are a robot that produces Python code using the Django framework based on a YAML document.
"""

MODELS_PROMPT = """You are a code production bot. You take a YAML string and convert it into django models. 
Each model has to be it's own file. Here is the YAML string:

{yaml}

You output each file in a single message. When I respond with "next", return the next file until there are no more files. 
When there are no more files, respond with "done". 
Do not provide anything else but the Python code. 
Do not format the code. 
The first line will be the path + filename, and the filename only. 
The second and line after that will be the actual code.

Group the models by different apps. For the app name, use the plural form. e.g "cars" instead of "car".

When referring to the User model, use "from django.contrib.auth import get_user_model"

For example:

cars/models.py
from django.db import models

class Car(models.Model):
    title = models.CharField(max_length=100)
    brand = models.ForeignKey("brands.brand", on_delete=models.CASCADE)
    def __str__(self):
        return self.title
"""

SERIALIZERS_PROMPT = """Now for each model you created, create a DRF serializer using the same rules. 
Each filename should be called `serializers.py` and live in their respective app path.
"""

ADMIN_PROMPT = """Now for each model you created, create a Django admin using the same rules. 

Make sure to register each site and use autocomplete fields where it makes sense. 

Use list_fields too where it makes sense.
"""

API_PROMPT = """Create REST endpoints using DRF. 

These files should live in the base directory under api/v1, where each model is it's own endpoint.
"""

APPS_PROMPT = """For each app you created, created an apps.py.

For example:

from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cars"
"""

SETTINGS_PROMPT = """Take the following Django settings file, and update the INSTALLED_APPS list to include the apps you created.

{content}

Do not provide anything else but the Python code. 
Do not format the code.
"""

NEXT = "next"
DONE = "done"
