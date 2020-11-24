from django.test import TestCase
from .models import *
from django.contrib.auth import get_user_model
from study_buddy.forms import *
import unittest
'''from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By'''
import time
from django.urls import reverse, reverse_lazy
from . import views


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

    def create_student(self, first="John", last="Smith", zoomID="1234567890"):
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
        data = {'email': s.email, }
        form = UserForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_form_pt2(self):
        s = Student.objects.create(firstName='john', lastName='Smith', computingID='jds4fk',
                                   phone='8044325324', zoomID='1234567890', graduationYear='2022', bio='Hi!', )
        data = {'firstName': s.firstName, 'lastName': s.lastName, 'computingID': s.computingID,
                'phone': s.phone, 'zoomID': s.zoomID, 'graduationYear': s.graduationYear, 'bio': s.bio, }
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        s = Student.objects.create(
            email='johnsmith@gmail.com', zoomID="1234567890")
        data = {'name': s.email, 'zoomID': s.zoomID}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form2(self):
        s = Student.objects.create(
            email='johnsmith@gmail.com', zoomID="1234567890", graduationYear="2019")
        data = {'name': s.email, 'zoomID': s.zoomID}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form3(self):
        s = Student.objects.create(
            email='johnsmithgmail.com', zoomID="1234567890", graduationYear="2019")
        data = {'name': s.email, 'zoomID': s.zoomID}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form4(self):
        s = Student.objects.create(
            email='johnsmith@gmail.com', zoomID="123456789012")
        data = {'name': s.email, 'zoomID': s.zoomID}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form5(self):
        s = Student.objects.create(
            email='johnsmith@gmail.com', zoomID="123456789012", computingID="abc1c")
        data = {'name': s.email, 'zoomID': s.zoomID}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())

    def test_valid_study_group_form(self):
        s = Student.objects.create(email='johnsmith@gmail.com')
        t = StudentCourse.objects.create(student=s, prefix="CS", number=3240)
        g = StudyGroup.objects.create(
            owner=s, studentCourse=t, courseName="Software Engineering", groupName="Name Generator")
        data = {'studentCourse': g.studentCourse,
                'courseName': g.courseName, 'groupName': g.groupName}
        form = StudyGroupForm(user=s.user, data=data)
        self.assertTrue(form.is_valid())


class UrlsTests(TestCase):

    def test_url(self):
        url1 = reverse_lazy('study_buddy:profile')
        self.assertEqual(url1, '/study_buddy/profile/')

    def test_url2(self):
        url = reverse_lazy('study_buddy:update_profile')
        self.assertEqual(url, '/study_buddy/profile/update_profile/')

    def test_url3(self):
        url = reverse_lazy('study_buddy:update_courses')
        self.assertEqual(url, '/study_buddy/profile/update_courses/')

'''class ViewsTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_signup_fire(self):
        self.driver.get("https://name-generator43.herokuapp.com/")

        username = 'gracebrickley'
        password = '09231999kgb'
        self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        time.sleep(2)
        self.driver.get("https://name-generator43.herokuapp.com/study_buddy")
        time.sleep(5)

        self.driver.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent')
                '.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2'
                '259%3A3%3Abbc%2C16%3A561fd7d2e94237c0%2C10%3A1599663155%2C16%3Af18105f2b08c3ae6%2C2f06af367387a967072e3124597eeb4e36c2eff92d3eef697'
                '1d95ddb5dea5225%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%'
                '2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2226bafb488fcc494f92c896ee923849b6%22%7D&response_type=code&flowName=GeneralOAuthFlow')

        username = 'gracebrickley'
        password = '09231999kgb'
        self.driver.find_element_by_name("identifier").send_keys(username)
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='identifierNext']/div/button/div[2]"))).click()
        self.driver.implicitly_wait(4)

        try:
            self.driver.find_element_by_name("password").send_keys(password)
            WebDriverWait(self.driver, 2).until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='passwordNext']/div/button/div[2]"))).click()
        except TimeoutException:
            print('\nUsername/Password seems to be incorrect, please re-check\nand Re-Run the program.')
            del username, password
            exit()
        except NoSuchElementException:
            print('\nUsername/Password seems to be incorrect, please re-check\nand Re-Run the program.')
            del username, password
            exit()
        try:
            WebDriverWait(self.driver, 5).until(lambda webpage: "https://stackoverflow.com/" in webpage.current_url)
            print('\nLogin Successful!\n')
        except TimeoutException:
            print('\nUsername/Password seems to be incorrect, please re-check\nand Re-Run the program.')
            exit()

        

        self.driver.find_element_by_id('user').send_keys("test user")
        self.driver.find_element_by_id('email').send_keys("test email")
        self.driver.find_element_by_id('submit').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def tearDown(self):
        self.driver.quit
'''
if __name__ == '__main__':
    unittest.main()
