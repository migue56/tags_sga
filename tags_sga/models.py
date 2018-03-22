from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models




class Pictogram(models.Model):
    DANGER = 5
    ATTENTION = 1
    CHOICES = ( 
        ( DANGER,_('Danger')),
        (ATTENTION,_('Attention')),
    )
    codename = models.CharField(max_length=100,primary_key=True)
    ilustrator_oit = models.FileField(upload_to='pictograms/',blank=True, null=True)
    ilustrator_sga = models.FileField(upload_to='pictograms/',blank=True, null=True) 
    warning_level = models.IntegerField(default=0,
             validators=[
                MaxValueValidator(12),
                MinValueValidator(0)
        ]) 
    human_tag = models.IntegerField(choices=CHOICES,db_index=True)
  
  
    def get_human_tag(self):
         d =dict(self.CHOICES)
         return d[self.human_tag]
         
    def __str__(self):
         return self.codename

    
#consejo    
class Tip (models.Model):
    physical_warnig =  models.TextField()
    health_safe = models.TextField()
    combinations = models.ManyToManyField("self",blank=True)
    
    def __str__(self):
      return self.physical_warnig 
  
# prudencia    
class Prudence(models.Model):   
    codename = models.CharField(max_length=100,primary_key=True)
    general_help = models.TextField()
    conditions_use = models.TextField()

    def __str__(self):
      return self.codename    

class Category (models.Model):
    codename = models.CharField(max_length=150)  # División 1.1
    warning_class = models.ManyToManyField("self",blank=True) # Explosivos (capítulo 2.1)
    tips = models.ManyToManyField(Tip)
    prudence = models.ManyToManyField(Prudence)
    pictogram = models.ManyToManyField(Pictogram)

    def __str__(self):
      return self.codename 

class SGAIndicator(models.Model):
    codename = models.CharField(max_length=100,primary_key=True)
    warning_categories = models.ManyToManyField(Category)
    warning_indication = models.CharField(max_length=255)  # Explosivo; grave peligro de proyección

    def __str__(self):
      return self.codename
class Component(models.Model):
    marketing_name = models.CharField(max_length=250) 
    SGAIndicator = models.ManyToManyField(SGAIndicator)
    

    def __str__(self):
      return self.marketing_name

class Provider(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address = models.TextField(max_length=100)
    
    def __str__(self):
        return self.name
      
class Sustance(models.Model):
    marketing_name = models.CharField(max_length=250) 
    cas_number = models.CharField(max_length=150)
    componets = models.ManyToManyField(Component)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    
    
     
    def __str__(self):
      return self.marketing_name      