from django.test import TestCase, SimpleTestCase, Client

# Create your tests here.

from django.urls import reverse

from .views import *

# Rewrite the tests
# class MatrixTests(SimpleTestCase):
#     def test_url_exists_at_correct_location(self):
#         response = self.client.get(reverse("/matrix"))
#         self.assertEqual(response.status_code, 200)

    
#     def test_url_available_by_name(self):
#         response = self.client.get(reverse("/matrix"))
#         self.assertEqual(response.status_code, 200)


#     def test_template_name_correct(self):
#         response = self.client.get(reverse("/matrix"))
#         self.assertTemplateUsed(response,"schedule/time_matrix.html")


#     def test_template_content(self):
#         response = self.client.get(reverse("/matrix"))
#         self.assertNotContains(response, "This is the contents")






from django.test.client import RequestFactory


class ScheduleCoursesTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_schedule_courses_view(self):
        view = ScheduleCourses.as_view()
        request = self.client.get(reverse("schedule-courses"))
        response = view(request)

        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'schedule/timetable.html')


        expected_template = 'schedule/timetable.html'
        self.assertEqual(response.template_name[0], expected_template)


        context = response.context_data
        self.assertIn('columns', context)
        self.assertIn('rows', context)
        self.assertIn('cells', context)
        self.assertIn('days', context)
        self.assertIn('time_slots', context)


