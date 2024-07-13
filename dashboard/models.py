from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta

class SupplierDetails(models.Model):
    SUPPLIER_CHOICES = [
        ('supplier1', 'Supplier 1'),
        ('supplier2', 'Supplier 2'),
        ('supplier3', 'Supplier 3'),
        ('supplier4', 'Supplier 4'),
    ]

    supplier = models.CharField(max_length=50, choices=SUPPLIER_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SupplierDetails(models.Model):
    SUPPLIER_CHOICES = [
        ('supplier1', 'Supplier 1'),
        ('supplier2', 'Supplier 2'),
        ('supplier3', 'Supplier 3'),
        ('supplier4', 'Supplier 4'),
    ]

    supplier = models.CharField(max_length=50, choices=SUPPLIER_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EquipmentDetails(models.Model):
    EQUIPMENT_CHOICES = [
        ('plough', 'Plough'),
        ('seed-drill', 'Seed Drill'),
        ('sprayer', 'Sprayer'),
        ('harvester', 'Harvester'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('un_available', 'Un-Available'),
    ]

    equipment = models.CharField(max_length=20, choices=EQUIPMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    supplied_by = models.ForeignKey(SupplierDetails, on_delete=models.CASCADE, related_name='equipment_supplied')

    def __str__(self):
        return f'{self.equipment}-{self.status}-{self.supplied_by}' 

class WorkerDetails(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class AssignmentDetails(models.Model):
    TASK_CHOICES = [
        ('ploughing', 'Ploughing'),
        ('sowing', 'Sowing'),
        ('watering', 'Watering'),
        ('harvesting', 'Harvesting'),
    ]

    task = models.CharField(max_length=50, choices=TASK_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    assigned_to = models.ForeignKey(WorkerDetails, on_delete=models.CASCADE)
    equipment_needed = models.ForeignKey(EquipmentDetails, on_delete=models.CASCADE, related_name='assignments', null=True, blank=True)

    def __str__(self):
        return self.task

    def clean(self):
        # Ensure all required equipment is available
        if self.equipment_needed.status != 'available':
            raise ValidationError(f'Equipment {self.equipment_needed.equipment} is not available.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate all fields including ForeignKey
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"

    
class CropDetails(models.Model):
    CROP_CHOICES = [
        ('wheat', 'Wheat'),
        ('rice', 'Rice'),
        ('maize', 'Maize'),
        ('millet', 'Millet'),
    ]
    
    crop = models.CharField(max_length=20, choices=CROP_CHOICES)
    planting_date = models.DateField()
    harvesting_date = models.DateField()
    task_assigned = models.ForeignKey(AssignmentDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.crop

    def clean(self):
        # Ensure harvesting date is after planting date
        if self.harvesting_date <= self.planting_date:
            raise ValidationError('Harvesting date must be after planting date.')

    def crop_cycle_duration(self):
        # Calculate the duration of the crop cycle
        return (self.harvesting_date - self.planting_date).days

    @classmethod
    def ready_for_harvest(cls, within_days=0):
        # Filter crops that are ready for harvest or will be ready within a certain timeframe
        today = models.DateField().today()
        end_date = today + timedelta(days=within_days)
        return cls.objects.filter(harvesting_date__lte=end_date)