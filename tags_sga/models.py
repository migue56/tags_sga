from django.db import models



class Pictogram(models.Model):
  codename = models.CharField(max_length=150,primary_key=True)
  ilustrator_oit = models.FileField(upload_to='pictograms/',blank=True, null=True)
  ilustrator_sga = models.FileField(upload_to='pictograms/',blank=True, null=True) 
  warning_level = models.IntegerField() 
  human_tag = models.CharField(max_length=50)

    
#consejo    
class Tip (models.Model):
    physical_warnig =  models.TextField()
    health_safe = models.TextField()

# prudencia    
class Prudence(models.Model):   
    codename = models.CharField(max_length=150,primary_key=True)
    general_help = models.TextField()
    conditions_use = models.TextField()

class Category (models.Model):
    codename = models.CharField(max_length=150)  # División 1.1
    warning_class = models.ManyToManyField("self",blank=True) # Explosivos (capítulo 2.1)
    tips = models.ManyToManyField(Tip)
    prudence = models.ManyToManyField(Prudence)
    pictogram = models.ManyToManyField(Pictogram)


class SGAIndicator(models.Model):
    codename = models.CharField(max_length=150,primary_key=True)
    warning_categories = models.ManyToManyField(Category)
    warning_indication = models.CharField(max_length=255)  # Explosivo; grave peligro de proyección



class Component(models.Model):
      marketing_name = models.CharField(max_length=250) 
      SGAIndicator = models.ManyToManyField(Category)
      

class Sustance(models.Model):
      marketing_name = models.CharField(max_length=250) 
      cas_number = models.CharField(max_length=150)
      componets = models.ManyToManyField(Component)