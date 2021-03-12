from django.db import models
import uuid

# Create your models here.
status_choices = [
    ('Queued','Queued'),
    ('Downloading Files from S3','Downloading Files from S3'),
    ('Processing','Processing'),
    ('Uploading the output to S3','Uploading the output to S3'),
    ('Completed','Completed')
]

class ChannelStatus(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True)
    channel_id = models.CharField(unique=True,max_length=128)
    status = models.CharField(max_length=100,choices=status_choices)
    aws_key = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    