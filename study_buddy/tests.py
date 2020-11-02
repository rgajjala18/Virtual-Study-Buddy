from django.test import TestCase
from .models import Student
from .models import Course
from django.contrib.auth import get_user_model
from study_buddy.forms import UserForm, ProfileForm

class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='normal', email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='normal', email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class ModelsTests(TestCase):

    def create_student(self, first="John", last="Smith"):
        return Student.objects.create(firstName=first, lastName=last)

    def test_student_name(self):
        s = self.create_student()
        self.assertTrue(isinstance(s, Student))
        self.assertEqual(s.__str__(), "John Smith")

    def create_course(self, letters="CS", numbers="3240"):
        return Course.objects.create(prefix=letters, number=numbers)

    def test_course_name(self):
        t = self.create_course()
        self.assertTrue(isinstance(t, Course))
        self.assertEqual(t.__str__(), "CS 3240")

class FormsTests(TestCase):

    def test_valid_form(self):
        s = Student.objects.create(email='johnsmith@gmail.com')
        data = {'email': s.email,}
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_form_pt2(self):
        s = Student.objects.create(firstName='john', lastName='Smith', computingID='jds4fk', phone='8044325324', zoomID='94392843', graduationYear='2022', bio='Hi!', )
        data = {'firstName': s.firstName, 'lastName': s.lastName, 'computingID': s.computingID, 'phone': s.phone, 'zoomID': s.zoomID, 'graduationYear': s.graduationYear, 'bio': s.bio,}
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())