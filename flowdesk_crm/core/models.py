import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

# class Lead(models.Model):

#     status = models.CharField(max_length=50)
#     source = models.CharField(max_length=50)
#     assigned = models.EmailField(blank=True)
#     enquiry_date = models.DateField()

#     name = models.CharField(max_length=100)
#     email = models.EmailField(blank=True)
#     phone = models.CharField(max_length=20)
#     qualification = models.CharField(max_length=100, blank=True)

#     department = models.CharField(max_length=50)
#     course = models.CharField(max_length=100)

#     address = models.TextField(blank=True)
#     location = models.CharField(max_length=100, blank=True)
#     feedback = models.TextField(blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name



# class UserProfile(models.Model):

#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('trainer', 'Trainer'),
#         ('cre', 'CRE'),
#         ('management', 'Management'),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     mobile = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username

# # Create your models here.
# #---------------------------
# from django.db import models
# from django.contrib.auth.models import User


class Status(models.Model):
    status_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.status_name


class Source(models.Model):
    source_name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['source_name']

    def __str__(self):
        return self.source_name


class Department(models.Model):
    department_name = models.CharField(max_length=50, unique=True)

    def _str_(self):
        return self.department_name



class Course(models.Model):
    course_name = models.CharField(max_length=25)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )
    fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    advance_payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('1000.00')
    )
    duration_months = models.PositiveIntegerField(default=3, help_text="Duration in months")
    installment_enabled = models.BooleanField(default=False)
    installment_count = models.PositiveIntegerField(default=1)
    installment_interval_days = models.PositiveIntegerField(default=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course_name', 'department'],
                name='unique_course_per_department'
            )
        ]

    def __str__(self):
        return f"{self.course_name} ({self.department.department_name}) - ₹{self.fees if self.fees else 'N/A'} - {self.duration_months} months"

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, unique=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('trainer', 'Trainer'),
        ('cre', 'CRE'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')

from django.conf import settings

class StudentEnquiry(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=25)
    enquiry_date = models.DateField()
    dob = models.DateField(blank=True, null=True)
    guardian_number = models.CharField(max_length=25, blank=True, null=True)
    year_of_passing = models.PositiveIntegerField(blank=True, null=True)

    qualification = models.CharField(
        max_length=50,
        help_text="Eg: BSc, BCA, Diploma, +2"
    )

    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True, blank=True)
    assigned = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True)

    source = models.ForeignKey(Source, on_delete=models.PROTECT, null=True, blank=True)

    TYPE_CHOICES = (
        ('new', 'New'),
        ('dnp', 'DNP'),
        ('hot', 'Hot'),
        ('warm', 'Warm'),
        ('cold', 'Cold'),
        ('done', 'Done'),
    )
    lead_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='new')
    interest_notes = models.TextField(blank=True, null=True)

    # ================= NORMALIZED ADDRESS =================
    house_name = models.CharField(max_length=150, blank=True, null=True)
    place = models.CharField(max_length=150, blank=True, null=True)
    district = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)

    location = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.CharField(max_length=150, blank=True, null=True)

    # ===== FOLLOW UP DETAILS =====
    followup_title = models.CharField(max_length=150, blank=True, null=True)
    followup_date = models.DateField(blank=True, null=True)
    followup_time = models.TimeField(blank=True, null=True)

    # ===== ADDITIONAL DETAILS =====
    college_name = models.CharField(max_length=150, blank=True, null=True)

    MODE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
    )
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, blank=True, null=True)

    campaign_name = models.CharField(max_length=150, blank=True, null=True)
    campaign_adset = models.CharField(max_length=150, blank=True, null=True)
    campaign_content = models.CharField(max_length=150, blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_leads",
        null=True, blank=True
    )

    def __str__(self):
        return self.full_name

# 🔥 MULTIPLE COURSES FOR LEAD
class LeadCourse(models.Model):
    lead = models.ForeignKey(
        StudentEnquiry,
        on_delete=models.CASCADE,
        related_name="lead_courses"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lead.full_name} - {self.course.course_name}"
    

class LeadActivity(models.Model):
    lead = models.ForeignKey(StudentEnquiry, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    action = models.CharField(max_length=255)
    old_value = models.CharField(max_length=255, blank=True, null=True)
    new_value = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

from django.utils import timezone

class LeadTask(models.Model):

    CATEGORY_CHOICES = (
        ('call', 'Call'),
        ('message', 'Message'),
        ('meeting', 'Meeting'),
    )

    lead = models.ForeignKey(
        StudentEnquiry,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    task_name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    date = models.DateField()
    time = models.TimeField()

    assigned_to = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead.full_name} - {self.task_name}"


class FollowUp(models.Model):
    lead = models.ForeignKey(
        StudentEnquiry,
        on_delete=models.CASCADE,
        related_name="followups"
    )
    title = models.CharField(max_length=150)
    followup_date = models.DateField()
    followup_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    assigned_to = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_followups"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-followup_date', '-followup_time']

    def __str__(self):
        return f"{self.lead.full_name} - {self.title}"


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=50)

class Topic(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=500)




# core/models.py

from django.db import models
from django.conf import settings
from django.utils.dateparse import parse_date

class Batch(models.Model):
    batch_name = models.CharField(max_length=25, unique=True)

    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,null=True,blank=True
    )

    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,null=True,blank=True
    )

    trainer = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,null=True,blank=True
    )

    start_date = models.DateField()
    end_date = models.DateField()

    
    start_time = models.TimeField(db_column='start_time',null=True, blank=True)

    end_time = models.TimeField(null=True, blank=True)

    MODE_CHOICES = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Hybrid', 'Hybrid'),
    )
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    no_of_students = models.IntegerField(
        default=30,
        db_column='no_of_students'
    )

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)     


    def __str__(self):
        return f"{self.batch_name} - {self.course.course_name}"
    
    def seats_left(self):
        return self.no_of_students - self.students.count()




class Student(models.Model):
    student_name = models.CharField(max_length=50)

    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=25)

    STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='enrolled'
    )

    house_name = models.CharField(max_length=150, blank=True, null=True)
    place = models.CharField(max_length=150, blank=True, null=True)
    district = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=150, blank=True, null=True)

    location = models.CharField(max_length=100, null=True, blank=True)

    enrolled_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.student_name

class StudentCourse(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="student_courses"
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.student.student_name} - {self.course.course_name}"

class Fee(models.Model):
    ADVANCE_PAYMENT_MINIMUM = Decimal('1000.00')

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    custom_installment_plan = models.BooleanField(default=False)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    course_fee_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    due_date = models.DateField()
    FEE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )
    fee_status = models.CharField(max_length=10,choices=FEE_STATUS_CHOICES,default='pending')

    @property
    def pending_amount(self):
        pending = self.total_fee - self.paid_amount
        return pending if pending > 0 else Decimal('0.00')

    @property
    def advance_payment_required(self):
        total_fee = self.total_fee or Decimal('0.00')
        if total_fee <= 0:
            return Decimal('0.00')
        configured_advance = getattr(self.course, 'advance_payment_amount', None)
        if configured_advance is None:
            configured_advance = self.ADVANCE_PAYMENT_MINIMUM
        return min(total_fee, configured_advance)

    @property
    def advance_payment_remaining(self):
        remaining = self.advance_payment_required - (self.paid_amount or Decimal('0.00'))
        return remaining if remaining > 0 else Decimal('0.00')

    @property
    def has_minimum_advance_payment(self):
        return self.advance_payment_remaining <= 0

    def recalculate_payment_status(self):
        from django.db.models import Sum
        total_paid = self.payments.aggregate(total=Sum('amount_paid')).get('total') or Decimal('0.00')
        self.paid_amount = total_paid
        advance_target = self.advance_payment_required
        self.advance_amount = advance_target
        self.advance_paid = min(self.paid_amount, advance_target)
        course_fee_paid = self.paid_amount - self.advance_paid
        self.course_fee_paid = course_fee_paid if course_fee_paid > 0 else Decimal('0.00')
        self.remaining_balance = self.pending_amount
        student_course = self.student.student_courses.filter(course=self.course).first()
        has_batch_assigned = bool(student_course and student_course.batch)

        today = timezone.localdate()
        original_due_date = self.due_date
        due_date = original_due_date
        if isinstance(due_date, str):
            parsed_due_date = parse_date(due_date)
            if parsed_due_date:
                due_date = parsed_due_date
                self.due_date = parsed_due_date
        if self.paid_amount >= self.total_fee:
            self.fee_status = 'paid'
        elif self.paid_amount > 0:
            self.fee_status = 'overdue' if has_batch_assigned and due_date < today else 'partial'
        else:
            self.fee_status = 'overdue' if has_batch_assigned and due_date < today else 'pending'

        update_fields = [
            'paid_amount',
            'advance_paid',
            'course_fee_paid',
            'remaining_balance',
            'advance_amount',
            'fee_status',
        ]
        if original_due_date != self.due_date:
            update_fields.append('due_date')
        self.save(update_fields=update_fields)



class FeeInstallment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='installments')
    installment_number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['installment_number']
        unique_together = ['fee', 'installment_number']

    def __str__(self):
        return f"{self.fee.student.student_name} - Installment {self.installment_number}"

    @property
    def pending_amount(self):
        pending = self.amount - self.paid_amount
        return pending if pending > 0 else Decimal('0.00')

    def update_status(self):
        from django.db.models import Sum
        today = timezone.localdate()
        
        # Recalculate paid_amount from all payments
        total_paid = self.payments.aggregate(total=Sum('amount_paid')).get('total') or Decimal('0.00')
        self.paid_amount = total_paid
        
        if self.paid_amount >= self.amount:
            self.status = 'paid'
        elif self.paid_amount > 0:
            self.status = 'overdue' if self.due_date < today else 'partial'
        else:
            self.status = 'overdue' if self.due_date < today else 'pending'
        self.save(update_fields=['paid_amount', 'status'])


class Payment(models.Model):
    fee = models.ForeignKey(Fee,on_delete=models.CASCADE,related_name='payments')
    installment = models.ForeignKey('FeeInstallment', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_KIND_CHOICES = (
        ('advance', 'Advance'),
        ('course_fee', 'Course Fee'),
        ('mixed', 'Mixed'),
    )
    PAYMENT_MODE_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
    )
    payment_mode = models.CharField(max_length=10,choices=PAYMENT_MODE_CHOICES)
    payment_date = models.DateField(auto_now_add=True)
    remarks = models.CharField(max_length=150, null=True, blank=True)
    payment_kind = models.CharField(max_length=10, choices=PAYMENT_KIND_CHOICES, default='course_fee')
    advance_component = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    course_fee_component = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ['-payment_date']

    def clean(self):
        if self.amount_paid is None or self.amount_paid <= 0:
            raise ValidationError("Payment amount must be greater than zero.")

        if self.installment:
            # Allow any amount up to pending amount for installment
            if self.amount_paid > self.installment.pending_amount:
                raise ValidationError(f"Payment exceeds installment pending amount of {self.installment.pending_amount}.")
        else:
            # For non-installment payments, check against total fee
            existing_total = self.fee.payments.exclude(pk=self.pk).aggregate(
                total=Sum('amount_paid')
            ).get('total') or Decimal('0.00')
            if existing_total + self.amount_paid > self.fee.total_fee:
                raise ValidationError("Payment exceeds remaining fee amount.")

    @staticmethod
    def split_payment_components(fee, starting_paid_amount, payment_amount):
        advance_required = fee.advance_payment_required if fee else Decimal('0.00')
        unpaid_advance = advance_required - (starting_paid_amount or Decimal('0.00'))
        if unpaid_advance < 0:
            unpaid_advance = Decimal('0.00')

        advance_component = min(payment_amount, unpaid_advance)
        course_fee_component = payment_amount - advance_component

        if advance_component > 0 and course_fee_component > 0:
            payment_kind = 'mixed'
        elif advance_component > 0:
            payment_kind = 'advance'
        else:
            payment_kind = 'course_fee'

        return {
            'payment_kind': payment_kind,
            'advance_component': advance_component,
            'course_fee_component': course_fee_component,
        }

    def apply_payment_components(self, starting_paid_amount):
        components = self.split_payment_components(
            fee=self.fee,
            starting_paid_amount=starting_paid_amount,
            payment_amount=self.amount_paid,
        )
        self.payment_kind = components['payment_kind']
        self.advance_component = components['advance_component']
        self.course_fee_component = components['course_fee_component']

    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = self.pk is None
        existing_total = self.fee.payments.exclude(pk=self.pk).aggregate(
            total=Sum('amount_paid')
        ).get('total') or Decimal('0.00')
        self.apply_payment_components(existing_total)
        super().save(*args, **kwargs)
        
        # Update installment if payment is linked to one
        if self.installment:
            self.installment.update_status()
        elif is_new and self.fee.installments.exists():
            # Auto-allocate payment to installments if not linked to specific installment
            self._allocate_to_installments()
        
        # Always update fee status
        self.fee.recalculate_payment_status()
    
    def _allocate_to_installments(self):
        """Automatically allocate payment amount to pending installments in order"""
        already_paid_before_this_payment = self.fee.payments.exclude(pk=self.pk).aggregate(
            total=Sum('amount_paid')
        ).get('total') or Decimal('0.00')
        remaining_amount = self.amount_paid
        
        # Get all installments ordered by installment_number
        installments = self.fee.installments.order_by('installment_number')
        
        allocated_payments = []
        
        for inst in installments:
            if remaining_amount <= 0:
                break
            
            # Refresh to get latest paid_amount
            inst.refresh_from_db()
            pending = inst.pending_amount
            
            if pending > 0:
                # Allocate to this installment
                allocation = min(remaining_amount, pending)
                
                # Store allocation info
                allocated_payments.append({
                    'installment': inst,
                    'amount': allocation
                })
                
                remaining_amount -= allocation
        
        # If we allocated to installments, update this payment and create split records
        if allocated_payments:
            # Link this payment to first installment
            first_alloc = allocated_payments[0]
            self.installment = first_alloc['installment']
            self.amount_paid = first_alloc['amount']
            self.apply_payment_components(already_paid_before_this_payment)
            super(Payment, self).save(update_fields=[
                'installment',
                'amount_paid',
                'payment_kind',
                'advance_component',
                'course_fee_component',
            ])
            first_alloc['installment'].update_status()

            running_paid_total = already_paid_before_this_payment + first_alloc['amount']
            
            # Create additional payment records for remaining allocations
            for alloc in allocated_payments[1:]:
                new_payment = Payment(
                    fee=self.fee,
                    installment=alloc['installment'],
                    amount_paid=alloc['amount'],
                    payment_mode=self.payment_mode,
                    remarks=self.remarks
                )
                new_payment.apply_payment_components(running_paid_total)
                # Save without triggering allocation again
                super(Payment, new_payment).save()
                alloc['installment'].update_status()
                running_paid_total += alloc['amount']

class Attendance(models.Model):

    STATUS_CHOICES = (
        ('present', 'Present'),
        ('late', 'Late'),
        ('leave', 'Leave'),
        ('absent', 'Absent'),
    )

    DURATION_CHOICES = (
        ('full', 'Full Day'),
        ('half', 'Half Day'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)

    date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default="full")

    remarks = models.CharField(max_length=255, blank=True, null=True)

    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'date']   # prevent duplicate attendance

    def __str__(self):
        return f"{self.student.student_name} - {self.date}"

class SessionUpdate(models.Model):
    session_date = models.DateField()
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    attendance_marked = models.BooleanField(default=False)
    assignment_given = models.CharField(max_length=100,null=True,blank=True)
    assignment_marks = models.PositiveIntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=50,null=True,blank=True)
    updated_by = models.ForeignKey(UserProfile,on_delete=models.PROTECT)

    class Meta:
        unique_together = ('batch', 'session_date')
        ordering = ['-session_date']

class TopicProgress(models.Model):

    STATUS_CHOICES = (
        ('not_started', 'Not Started'),
        ('partial', 'Partial'),
        ('completed', 'Completed'),
    )

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )

    remarks = models.TextField(blank=True, null=True)

    updated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('batch', 'topic')

    def __str__(self):
        return f"{self.batch.batch_name} - {self.topic.topic_name}"
    


class Assignment(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionUpdate, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.batch.batch_name} - {self.title}"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('not_submitted', 'Not Submitted'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('assignment', 'student')
    
    def __str__(self):
        return f"{self.student.student_name} - {self.assignment.title}"


class Exam(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    exam_date = models.DateField()
    max_marks = models.PositiveIntegerField(default=100)
    created_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-exam_date', '-created_at']

    def __str__(self):
        return f"{self.batch.batch_name} - {self.title}"


class ExamPerformance(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='performances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam', 'student')

    def __str__(self):
        return f"{self.student.student_name} - {self.exam.title}"
    


class QuestionPaper(models.Model):
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, related_name='question_paper')
    total_marks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question Paper - {self.exam.title}"

    @property
    def total_marks_from_parts(self):
        return sum(part.marks for part in self.parts.all())


class QuestionPart(models.Model):
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, related_name='parts')
    part_name = models.CharField(max_length=50)
    marks = models.PositiveIntegerField()
    questions = models.TextField()
    question_marks = models.TextField(blank=True, default='')
    question_data = models.JSONField(blank=True, default=list)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = ('question_paper', 'part_name')

    def __str__(self):
        return f"Part {self.part_name} - {self.marks} marks"

    @property
    def question_items(self):
        if self.question_data:
            items = []
            for entry in self.question_data:
                question_text = (entry or {}).get('text', '').strip()
                if not question_text:
                    continue

                subquestions = []
                for subquestion in (entry or {}).get('subquestions', []):
                    subquestion_text = (subquestion or {}).get('text', '').strip()
                    if subquestion_text:
                        subquestions.append({
                            'text': subquestion_text,
                            'mark': str((subquestion or {}).get('mark', '')).strip(),
                        })

                items.append({
                    'text': question_text,
                    'mark': str((entry or {}).get('mark', '')).strip(),
                    'subquestions': subquestions,
                })
            if items:
                return items

        questions = [question.strip() for question in self.questions.splitlines() if question.strip()]
        marks = [mark.strip() for mark in self.question_marks.splitlines()] if self.question_marks else []

        items = []
        for index, question in enumerate(questions):
            mark_value = marks[index] if index < len(marks) else ''
            items.append({
                'text': question,
                'mark': mark_value,
                'subquestions': [],
            })
        return items


class TrainerSpecialization(models.Model):
    trainer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='specializations'
    )
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['trainer', 'department', 'course'],
                name='unique_trainer_specialization'
            )
        ]

    def __str__(self):
        return f"{self.trainer} - {self.department.department_name} - {self.course.course_name}"


class PendingMail(models.Model):
    MAIL_TYPE_CHOICES = (
        ('batch', 'Batch Assignment'),
        ('payment', 'Payment Success'),
        ('overdue', 'Overdue Mail'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='pending_mails'
    )
    email = models.EmailField(max_length=254, blank=True, null=True)
    mail_type = models.CharField(max_length=20, choices=MAIL_TYPE_CHOICES)
    batch = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pending_mails'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    fee = models.ForeignKey(
        Fee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pending_mails'
    )
    last_error = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.student_name} - {self.get_mail_type_display()}"


class MailLog(models.Model):
    MAIL_TYPE_CHOICES = (
        ('batch', 'Batch Assignment'),
        ('payment', 'Payment Success'),
        ('overdue', 'Overdue Mail'),
    )
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mail_logs'
    )
    fee = models.ForeignKey(
        Fee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mail_logs'
    )
    email = models.EmailField(max_length=254)
    mail_type = models.CharField(max_length=20, choices=MAIL_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    sent_at = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'mail_logs'
        ordering = ['-sent_at', '-id']

    def __str__(self):
        student_name = self.student.student_name if self.student else "Unknown Student"
        return f"{student_name} - {self.get_mail_type_display()} - {self.status}"


class DismissedNotification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dismissed_notifications'
    )
    notification_key = models.CharField(max_length=120)
    dismissed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'notification_key'],
                name='unique_dismissed_notification'
            )
        ]
        ordering = ['-dismissed_at']

    def __str__(self):
        return f"{self.user.username} dismissed {self.notification_key}"
