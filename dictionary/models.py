from django.db import models


class Definition(models.Model):
    # data
    word = models.CharField(max_length=30)
    phonetic = models.CharField(max_length=30, blank=True)
    meaning = models.TextField()
    extra_info = models.TextField(blank=True)
    private_notes = models.TextField(blank=True)
    synonyms = models.CharField(max_length=60, blank=True)
    related = models.CharField(max_length=60, blank=True)
    origin = models.CharField(max_length=60, blank=True)

    # metadata
    semantic_group = models.PositiveSmallIntegerField(default=1)
    priority = models.PositiveSmallIntegerField(default=1)
    source = models.CharField(max_length=60)
    reviewed = models.BooleanField(default=True)
    public = models.BooleanField(default=True)

    class Meta:
        ordering = ('word', 'semantic_group', 'priority')

    def __str__(self):
        return self.word
