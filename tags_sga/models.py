from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.files import FieldFile



connect('mongodb://localhost:27017/tags_sga')

class Pictogram(EmbeddedMongoModel):
    DANGER = 5
    ATTENTION = 1
    EMPTY=0
    CHOICES = ( 
         (EMPTY,_('---')),
        ( DANGER,_('Danger')),
        (ATTENTION,_('Attention')),
    )
    codename =  fields.CharField(primary_key=True)
    ilustrator_sga = fields.CharField() #fields.FieldFile(upload_to='pictograms/',blank=True, null=True) 
    ilustrator_oit = fields.CharField() #fields.FieldFile(upload_to='pictograms/',blank=True, null=True)
    warning_level = fields.IntegerField(default=0,min_value=0,max_value=12)
    human_tag = fields.IntegerField(choices=CHOICES,default=EMPTY)

    class Meta:
        # Text index on content can be used for text search.
        indexes = [IndexModel([('human_tag', TEXT)])]

    def get_human_tag(self):
         d =dict(self.CHOICES)
         if self.human_tag!=self.EMPTY:
            return d[self.human_tag]
         return ""
         
    def __str__(self):
         return self.codename

    
#consejo    
class Tip (EmbeddedMongoModel):
    codename = fields.CharField(max_length=200)
    physical_warnig =  fields.CharField()
    combinations = models.ManyToManyField("self",blank=True, verbose_name=_("Children to combinations tips")) # MPTT

    class Meta:
        indexes = [IndexModel([('codename', TEXT)])]

    
    def __str__(self):
      return "%s:%s"%(self.codename,self.physical_warnig) 
  
# prudencia    
class Prudence(EmbeddedMongoModel):   
    codename = fields.CharField(primary_key=True)
    general_help = fields.CharField()
    conditions_use = fields.CharField()

    def __str__(self):
      return self.codename    

class Category (MongoModel):
    codename = fields.CharField(max_length=150)  # División 1.1
    warning_class =  fields.ListField(fields.ReferenceField('Category')) # Explosivos (capítulo 2.1)
    tips = fields.EmbeddedDocumentListField('Tip')
    prudence = fields.EmbeddedDocumentListField('Prudence')
    pictogram = fields.EmbeddedDocumentListField('Pictogram')

    class Meta:
        indexes = [IndexModel([('codename', TEXT)])]
        
    def __str__(self):
      return self.codename 

class SGAIndicator(MongoModel):
    codename = fields.CharField(primary_key=True)
    warning_categories = fields.ListField(fields.ReferenceField('Category')) 
    
    def __str__(self):
      return self.codename
  
class Component(EmbeddedMongoModel):
    marketing_name = fields.CharField(max_length=250) 
    SGAIndicator = fields.ListField(fields.ReferenceField('SGAIndicator')) 
    

    def __str__(self):
      return self.marketing_name

class Provider(EmbeddedMongoModel):
    name = fields.CharField(max_length=150)
    phone = fields.CharField(max_length=15)
    address = fields.CharField(max_length=100)
    
    def __str__(self):
        return self.name
      
class Sustance(MongoModel):
    marketing_name = fields.CharField(max_length=250) 
    cas_number = fields.CharField(max_length=150)
    componets = EmbeddedDocumentListField('Component')
    use_instructions=fields.CharField(max_length=500)
    provider = EmbeddedDocumentListField('Provider')
    
    def __str__(self):
      return "%s:%s"%(self.cas_number,self.marketing_name)    
    
# class Product(models.Model):
#     sustance = models.ForeignKey(Sustance,null=False,blank=False, on_delete=models.CASCADE)
#     loading_date = models.DateField(_("Date loading"))
#     expiration_date = models.DateField(_("Date expiration"))
#     tare=models.CharField(max_length=250) 
#     lot_number=models.CharField(max_length=250) 
#     gross_weight=models.CharField(max_length=250) 
     
#     def __str__(self):
#       return "%s, %s"%(self.sustance.marketing_name,self.gross_weight)
#   
#   
  