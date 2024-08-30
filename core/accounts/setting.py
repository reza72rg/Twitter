from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.core.files import File
from django.utils.translation import gettext as _
from PIL import Image
from io import BytesIO
def get_image_field(self):
    output = []
    for k, v in self.__dict__.items():
        if isinstance(v, ImageFieldFile):
            output.append(k)
    return output


class MainModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_("create date"))
    modify_date = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_("modify date"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))

    def save(self, *args, **kwargs):
        image_fields = get_image_field(self)
        if image_fields:
            for i in image_fields:
                if hasattr(self, i) and isinstance(getattr(self, i), ImageFieldFile):
                    image = Image.open(getattr(self, i).file)
                    image_io = BytesIO()
                    image_extension = getattr(self, i).name.rpartition(".")[-1].upper()
                    image_extension = "JPEG" if image_extension == "JPG" else image_extension
                    image.save(image_io, image_extension, quality=60)
                    new_image = File(image_io, name=getattr(self, i).name)
                    setattr(self, i, new_image)
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True