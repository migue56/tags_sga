from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Manager


from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
from pymodm.files import FieldFile



connect('mongodb://localhost:27017/tags_sga')


class Pictogram(MongoModel):
    DANGER = 5
    ATTENTION = 1
    EMPTY=0
    CHOICES = ( 
         (EMPTY,_('---')),
        ( DANGER,_('Danger')),
        (ATTENTION,_('Attention')),
    )
    codename =  fields.CharField(primary_key=True)
    ilustrator_sga = fields.FileField(verbose_name="%s"%_('SGA Ilustration'),mongo_name='isga',storage='pictograms/') #fields.FieldFile(upload_to='pictograms/',blank=True, null=True) 
    ilustrator_oit = fields.FileField(verbose_name="%s"%_('OIT Ilustration'),mongo_name='ioit',storage='pictograms/') #fields.FieldFile(upload_to='pictograms/',blank=True, null=True)
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
class Tip (MongoModel):
    codename = fields.CharField(max_length=200)
    physical_warning =  fields.CharField()
    combinations = fields.ListField(fields.ReferenceField('Tip')) # MPTT


    def __str__(self):
      return "%s:%s"%(self.codename,self.physical_warnig) 

    class Meta:
        indexes = [IndexModel([('codename', TEXT)])]
        
          
# prudencia    
class Prudence(MongoModel):   
    codename = fields.CharField(primary_key=True)
    general_help = fields.CharField()
    conditions_use = fields.CharField()
    combinations = fields.ListField(fields.ReferenceField('Prudence')) # MPTT

    def __str__(self):
      return self.codename 
    
    class Meta:
        indexes = [IndexModel([('codename', TEXT)])]

class Warning_class(MongoModel):
    codename = fields.CharField(max_length=200)  # División 1.1
    prudence = fields.ListField(fields.ReferenceField('Prudence'))
    
class Category (MongoModel):
    codename = fields.CharField(max_length=150)  # División 1.1
    warning_classes =  fields.ListField(fields.ReferenceField('Warning_class')) # Explosivos (capítulo 2.1)
    tips = fields.ListField(fields.ReferenceField('Tip'))
    prudence = fields.ListField(fields.ReferenceField('Prudence'))
    pictogram = fields.ListField(fields.ReferenceField('Pictogram'))

    class Meta:
        indexes = [IndexModel([('codename', TEXT)])]
        
    def __str__(self):
      return self.codename 

class SGAIndicator(MongoModel):
    codename = fields.CharField(primary_key=True)
    warning_categories = fields.ListField(fields.ReferenceField('Category')) 
    tips = fields.ListField(fields.ReferenceField('Tip'))
    
    def __str__(self):
      return self.codename
  
class Component(MongoModel):
    marketing_name = fields.CharField(max_length=250) 
    cas_number = fields.CharField(max_length=150)
    sga_indicators = fields.ListField(fields.ReferenceField('SGAIndicator')) 
    warning_classes =  fields.ListField(fields.ReferenceField('Warning_class')) # Explosivos (capítulo 2.1)
    

    def __str__(self):
      return self.marketing_name

class Provider(EmbeddedMongoModel):
    name = fields.CharField(max_length=250)
    phone = fields.CharField(max_length=30)
    address = fields.CharField(max_length=500)
    
    def __str__(self):
        return self.name
      
class Sustance(MongoModel):
    marketing_name = fields.CharField(max_length=250) 
    components = fields.EmbeddedDocumentListField('Component')
    use_instructions=fields.CharField(max_length=500)
    provider = fields.EmbeddedDocumentListField('Provider')
    
    def __str__(self):
      return (self.marketing_name)    
    
class Product(MongoModel):
#     sustance = models.ForeignKey(Sustance,null=False,blank=False, on_delete=models.CASCADE)
     loading_date = fields.DateTimeField()
     expiration_date = fields.DateTimeField()
     tare=fields.CharField(max_length=250) 
     lot_number=fields.CharField(max_length=250) 
     gross_weight=fields.CharField(max_length=250) 
     
#     def __str__(self):
#       return "%s, %s"%(self.sustance.marketing_name,self.gross_weight)
#   
#   
  