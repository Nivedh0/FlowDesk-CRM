from datetime import date
import re

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import (
    Course,
    Department,
    FollowUp,
    LeadActivity,
    Status,
    StudentEnquiry,
    TrainerSpecialization,
    UserProfile,
)


class CreateUserValidationTests(TestCase):
    def setUp(self):
        self.url = reverse("create_user")
        self.user_list_url = reverse("user_list")

    def test_create_user_success(self):
        payload = {
            "username": "john.smith",
            "password": "StrongPass@123",
            "first_name": "John",
            "last_name": "Smith",
            "email": "John.Smith@example.com",
            "mobile": "+15551234567",
            "role": "trainer",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.user_list_url)
        user = User.objects.get(username="john.smith")
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(user.email, "john.smith@example.com")
        self.assertEqual(profile.mobile, "+15551234567")
        self.assertEqual(profile.role, "trainer")

    def test_create_user_rejects_duplicates(self):
        existing = User.objects.create_user(
            username="existing_user",
            password="StrongPass@123",
            email="existing@example.com",
            first_name="Existing",
            last_name="User",
        )
        UserProfile.objects.create(user=existing, mobile="+15550001111", role="cre")

        payload = {
            "username": "existing_user",
            "password": "StrongPass@123",
            "first_name": "John",
            "last_name": "Smith",
            "email": "EXISTING@example.com",
            "mobile": "+15550001111",
            "role": "trainer",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Username already exists.", status_code=400)
        self.assertContains(response, "Email already exists.", status_code=400)
        self.assertContains(response, "Mobile number already exists.", status_code=400)
        self.assertEqual(User.objects.filter(username="existing_user").count(), 1)

    def test_create_user_rejects_invalid_input(self):
        payload = {
            "username": "a",
            "password": "123",
            "first_name": "J0hn",
            "last_name": "Sm1th",
            "email": "not-an-email",
            "mobile": "12ab",
            "role": "not-a-role",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Username must be at least 3 characters.", status_code=400)
        self.assertContains(response, "First name contains invalid characters.", status_code=400)
        self.assertContains(response, "Last name contains invalid characters.", status_code=400)
        self.assertContains(response, "Enter a valid email address.", status_code=400)
        self.assertContains(response, "Enter a valid mobile number", status_code=400)
        self.assertContains(response, "Select a valid role.", status_code=400)
        self.assertFalse(User.objects.filter(username="a").exists())


class EditUserTrainerSpecializationTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="adminuser",
            password="StrongPass@123",
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
        )
        self.admin_profile = UserProfile.objects.create(
            user=self.admin_user,
            mobile="+15551112222",
            role="admin",
        )
        self.trainer_user = User.objects.create_user(
            username="traineruser",
            password="StrongPass@123",
            first_name="Trainer",
            last_name="User",
            email="trainer@example.com",
        )
        self.trainer_profile = UserProfile.objects.create(
            user=self.trainer_user,
            mobile="+15553334444",
            role="trainer",
        )
        self.department = Department.objects.create(department_name="Software")
        self.course = Course.objects.create(
            course_name="Python",
            department=self.department,
        )
        TrainerSpecialization.objects.create(
            trainer=self.trainer_profile,
            department=self.department,
            course=self.course,
        )
        self.url = reverse("edit_user", args=[self.trainer_user.id])

    def test_edit_user_page_shows_existing_trainer_department(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Software")
        self.assertContains(response, "const initialSpecializedDepartments = [")
        self.assertContains(response, 'value="{}"'.format(self.course.id))
        self.assertContains(response, "checked")

    def test_edit_user_updates_trainer_specializations(self):
        new_department = Department.objects.create(department_name="Design")
        new_course = Course.objects.create(
            course_name="UI UX",
            department=new_department,
        )
        self.client.force_login(self.admin_user)

        response = self.client.post(
            self.url,
            {
                "first_name": "Trainer",
                "last_name": "User",
                "email": "trainer@example.com",
                "mobile": "+15553334444",
                "role": "trainer",
                "specialized_departments": [str(new_department.id)],
                "specialized_courses": [str(new_course.id)],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_detail", args=[self.trainer_user.id]))
        self.assertTrue(
            TrainerSpecialization.objects.filter(
                trainer=self.trainer_profile,
                department=new_department,
                course=new_course,
            ).exists()
        )
        self.assertFalse(
            TrainerSpecialization.objects.filter(
                trainer=self.trainer_profile,
                department=self.department,
                course=self.course,
            ).exists()
        )


class UpdateLeadStatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="statususer",
            password="StrongPass@123",
        )
        self.followup_status = Status.objects.create(status_name="Follow Up")
        self.new_status = Status.objects.create(status_name="New Enquiry")
        self.lead = StudentEnquiry.objects.create(
            full_name="Jane Doe",
            email="jane@example.com",
            mobile="9876543210",
            enquiry_date=date.today(),
            qualification="BSc",
            status=self.new_status,
            location="Kochi",
        )

    def test_followup_status_redirects_to_add_followup_page(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("update_lead_status", args=[self.lead.id]),
            {"status": self.followup_status.id},
        )

        self.lead.refresh_from_db()
        self.assertEqual(self.lead.status, self.followup_status)
        self.assertRedirects(response, reverse("add_followup", args=[self.lead.id]))
        self.assertFalse(FollowUp.objects.filter(lead=self.lead).exists())


class LeadProfileFollowupActivityTests(TestCase):
    def setUp(self):
        self.lead = StudentEnquiry.objects.create(
            full_name="Alex Doe",
            email="alex@example.com",
            mobile="9998887776",
            enquiry_date=date.today(),
            qualification="BCA",
            location="Kochi",
        )
        self.followup = FollowUp.objects.create(
            lead=self.lead,
            title="Call back",
            followup_date=date.today(),
            status="completed",
            created_by=User.objects.create_user(
                username="creator",
                password="StrongPass@123",
            ),
        )
        LeadActivity.objects.create(
            lead=self.lead,
            action="Follow-up Added",
            new_value=f"{self.followup.title} on {self.followup.followup_date}",
        )
        LeadActivity.objects.create(
            lead=self.lead,
            action="Completed Follow-up",
            new_value=f"{self.followup.title} on {self.followup.followup_date}",
        )

    def test_followup_added_activity_stays_pending_after_completion(self):
        response = self.client.get(reverse("lead_profile", args=[self.lead.id]))

        self.assertEqual(response.status_code, 200)
        html = response.content.decode()
        self.assertRegex(
            html,
            re.compile(r"Follow-up Added\s*<span class=\"badge bg-warning ms-2\">Pending</span>")
        )
        self.assertRegex(
            html,
            re.compile(r"Completed Follow-up\s*<span class=\"badge bg-success ms-2\">Completed</span>")
        )

    def test_task_section_shows_related_followups(self):
        response = self.client.get(reverse("lead_profile", args=[self.lead.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Follow-ups")
        self.assertContains(response, self.followup.title)
        self.assertContains(response, "Completed")
