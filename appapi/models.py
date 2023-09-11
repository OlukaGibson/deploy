from django.db import models

class FirmwareUpdate(models.Model):
    version = models.CharField(max_length=20)
    description = models.TextField()
    #file = models.FileField(upload_to='firmware/')
    spvValue = models.PositiveIntegerField()
    batteryValue = models.PositiveIntegerField()
    firmware = models.CharField(max_length=50)
    device_id = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.version
