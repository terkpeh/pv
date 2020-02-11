from django.contrib.auth.models import User
from django.db import models
from django.utils.html import format_html
from django.conf import settings
from crum import get_current_user
from datetime import datetime

# from datetime import datetime


# Create your models here.
class user_type(models.Model):
    is_director = models.BooleanField(default=False)
    is_standard = models.BooleanField(default=False)
    is_management = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
       if self.is_director == True:
           return User.get_username(self.user) + " - is_director"
       elif self.is_standard == True :
           return User.get_username(self.user) + " - is_standard"
       else:
           return User.get_username(self.user) + " - is_management"


class Pv(models.Model):
    accounts =(
        ('Sub CF','Sub CF'),
        ('Special','Special'),
        ('Directors','Directors'),
        ('Operations','Operations'),
        ('LSGDP','LSGDP'),
        ('DWAP','DWAP'),
        ('Capacity(USD)','Capacity(USD)')
        )
    acc =(
    ('Yes','Yes'),
    ('No', 'No')
    )

    source =(
            ('GOG','GOG'),
            ('Others', 'Others')
          )
    pv =(
        ('General','General'),
        ('Honorarium','Honorarium')
       )
    center=(
        ('Cost Center 1','Cost Center 1'),
        ('Cost Center 2','Cost Center 2'),
        ('Cost Center 3','Cost Center 3'),
        ('Cost Center 4','Cost Center 4'),
        ('Cost Center 5','Cost Center 5')
           )
    stat =(
        ('Completed','Completed'),
        ('Returned','Returned'),
        ('Cancelled','Cancelled')
    )
    IA_System_Code = models.AutoField(primary_key = True)
    IA_code = models.CharField(max_length = 150)
    Date_recieved = models.DateField()
    Pv_reference = models.CharField(unique = True, max_length = 120)
    Source_of_Funding = models.CharField(max_length=50, choices = source)
    Cost_center = models.CharField(max_length=50, choices = center)
    Payee = models.CharField(max_length=500,blank=True, null=True)
    Description = models.CharField(max_length = 500)
    Account_code = models.CharField(max_length=350)
    Gross_amount = models.DecimalField(max_digits=19, decimal_places=2)
    Withholding_tax = models.DecimalField(max_digits=19, decimal_places=2)
    Net_amount = models.DecimalField(max_digits=19, decimal_places=2)
    Status = models.CharField(max_length = 60, choices = stat )
    Remarks =models.CharField(max_length = 500, blank = True)
    Acc_Impress = models.CharField(max_length = 350,choices=acc)
    Date_returned =models.DateField(null=True,blank = True)
    Type_of_accounts= models.CharField(max_length = 100, choices = accounts)
    Type_of_pv = models.CharField(max_length = 20, choices = pv)
    returned_to_chest = models.DecimalField(max_digits=19, decimal_places=2,default= 0.00)
    created = models.DateTimeField(null=True)
    created_by = models.ForeignKey('auth.User', blank=True, null=True, default=None,on_delete=models.CASCADE,related_name='create')
    modified = models.DateTimeField(null=True)
    modified_by = models.ForeignKey('auth.User', blank=True, null=True,default=None ,on_delete=models.CASCADE,related_name='modified')
    class Meta():
            ordering = ["-IA_System_Code"]



    def __str__(self):
        return self.Pv_reference + "--- " + self.Description + "--- " + self.Type_of_pv

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
            self.created = datetime.now()
        else:
            self.modified_by = user
            self.modified = datetime.now()
        super(Pv, self).save(*args, **kwargs)

class staff(models.Model):
    grade =(
        ('A.A.G','A.A.G'),
        ('AG','AG'),
        ('ARTISAN GD I','ARTISAN GD I'),
        ('ARTISAN GD II','ARTISAN GD II'),
        ('ARTISAN GD III','ARTISAN GD III'),
        ('ARTISAN GRADE','ARTISAN GRADE'),
        ('ASST SECURITY GUARD','ASST SECURITY GUARD'),
        ('ASST. CHIEF SEC.OFF.','ASST. CHIEF SEC.OFF.'),
        ('ASST. DIR','ASST. DIR'),
        ('AUD EXAMINER','AUD EXAMINER'),
        ('AUDIT ASST','AUDIT ASST'),
        ('AUDITOR','AUDITOR'),
        ('CHEIF SEC. OFF','CHEIF SEC. OFF'),
        ('CLEANER','CLEANER'),
        ('CLEANER GD I','CLEANER GD I'),
        ('CLEANER GD II','CLEANER GD II'),
        ('DAG','DAG'),
        ('DIRECTOR','DIRECTOR'),
        ('DIR GD. I','DIR GD. I'),
        ('DIR GD. II','DIR GD. II'),
        ('DIR GD. III','DIR GD. III'),
        ('EX OF A/C','EX OF A/C'),
        ('HEAD LAB','HEAD LAB'),
        ('HEAD WATCHMAN','HEAD WATCHMAN'),
        ('LAB GD II','LAB GD II'),
        ('LAB GD I','LAB GD I'),
        ('LAB./CLEARN','LAB./CLEARN'),
        ('P.E.A','P.E.A'),
        ('PRIN.AUD','PRIN.AUD'),
        ('PRIN.RECEPTIONIST','PRIN.RECEPTIONIST'),
        ('PRIN. SEC OFF','PRIN. SEC OFF'),
        ('PRIN .STORE OFF','PRIN .STORE OFF'),
        ('PRIN. TYPIST','PRIN. TYPIST'),
        ('RECEPTIONIST','RECEPTIONIST'),
        ('PRIVATE SEC','PRIVATE SEC'),
        ('RECEPTIONIST','RECEPTIONIST'),
        ('S.E.A','S.E.A'),
        ('SEC OFF.','SEC OFF.'),
        ('SEN EST.ASSIST','SEN EST.ASSIST'),
        ('SEN STENO.','SEN STENO.'),
        ('SNR. TYPIST','SNR. TYPIST'),
        ('SNR. AUDITOR','SNR. AUDITOR'),
        ('SRN. PRIV. SEC','SRN. PRIV. SEC'),
        ('SNR. SEC OFF','SNR. SEC OFF'),
        ('SNR. TELEPHONIST','SNR. TELEPHONIST'),
        ('SNR. TRANS. OFFICER','SNR. TRANS. OFFICER'),
        ('STENO','STENO'),
        ('STENO. SEC','STENO. SEC'),
        ('STORES ASSISTANT','STORES ASSISTANT'),
        ('SWEEPER','SWEEPER'),
        ('TELEPHONIST','TELEPHONIST'),
        ('TRANSPORT OFF','TRANSPORT OFF'),
        ('TYPIST','TYPIST'),
        ('TYPIST GD I','TYPIST GD I'),
        ('WATCHMAN','WATCHMAN'),
        ('YARD FOR','YARD FOR'),



        )
    staff_id = models.CharField(max_length = 150)
    name = models.CharField(max_length = 300)
    rank = models.CharField(max_length = 300,choices = grade)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    Pv_reference = models.ForeignKey('Pv',on_delete=models.CASCADE, related_name='Pvreference')
    Date_added = models.DateTimeField(default= datetime.now)

    def __str__(self):
        return self.name






 # class Grade(models.Model):
