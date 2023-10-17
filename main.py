import kivy
kivy.require("2.2.1")
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
import cv2 as cv
from kivy.clock import Clock
from kivy.graphics.texture import Texture
# from deepface import DeepFace

Window.size = (350, 550)
Builder.load_file('design.kv')

class LoginScreen(Screen):
	
	def get_user_credential(self):
		'''Get user email and password.
			Send request to server and if user is valid,
			then direct to main screen

		'''
		is_user_valid = False

		email = self.ids.email.text
		password = self.ids.password.text

		print(f"Email is {email} and password is {password}")
		# if returned response is valid

		is_user_valid = True

		if is_user_valid:
			self.manager.transition.direction = "right"
			self.manager.current = "MainScreen"
			# clean input
			self.ids.email.text = ''
			self.ids.password.text = ''





class MainScreen(Screen):

	def on_pre_enter(self):
		self.ids.nav_drawer.set_state("close") #close navigation drawer incase is already opened

		
	def log_user_out(self):
		'''Logout current user and redirect to sign in screen.

		'''
		self.manager.current = "LoginScreen"


	def to_profile_page(self):
		''' redirect to profile screen to capture and student

		'''
		self.manager.current = "ProfileCaptureScreen"


class ProfileCaptureScreen(Screen):
	# def __init__(self,**kwargs):
	# 	super(ProfileCaptureScreen, self).__init__(**kwargs)
	# 	self.capture = cv.VideoCapture(0)
	# 	Clock.schedule_interval(self.update, 1.0  / 33.0)

	def on_enter(self):
		self.capture = cv.VideoCapture(0)
		self.event = Clock.schedule_interval(self.update, 1.0  / 33.0)


	def update(self, *args):
		ret, self.frame = self.capture.read()
		self.cam = self.ids.profile_pic

		buf = cv.flip(self.frame, 0).tobytes()
		img_texture = Texture.create(
			size=(self.frame.shape[1], self.frame.shape[0]), colorfmt="bgr")

		img_texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
		self.cam.texture = img_texture
			

	def capture_face(self):
		print("capturing face now")

		is_captured = cv.imwrite("img/capture.png", self.frame)
		if is_captured:
			self.event.cancel() #cancel schedule_interval clock
			self.capture.release() #release capture obj

			captured_path = "img/capture.png"
			self.cam.source = captured_path

			
	def reset_face_capturing(self):
		print("face reset")
		self.event.start()
		# self.capture = cv.VideoCapture(0)
		# self.event = Clock.schedule_interval(self.update, 1.0  / 33.0)

	def verify_captured_face(self):
		print("verify face")
		# try:
		# 	# result = DeepFace.verify(img1_path = "img/capture.png", img2_path = 'img/capture1.png')
		# 	print(result)
		# except Exception as e:
		# 	print("NO face detected")
		# else:
		# 	pass
		# finally:
		# 	pass
		

		

	def on_pre_leave(self):
		self.event.cancel() #cancel schedule_interval clock
		self.capture.release() #release capture obj
		

	def on_leave(self):
		# set Image source
		self.cam.source = 'img/ai.jpeg'
		


class FaceApp(MDApp):
	"""ToDo application base class"""

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Blue"
		# self.theme_cls.primary_hue = "900"

		self.sm = ScreenManager()
		self.sm.add_widget(LoginScreen(name="LoginScreen"))
		self.sm.add_widget(MainScreen(name="MainScreen"))
		self.sm.add_widget(ProfileCaptureScreen(name="ProfileCaptureScreen"))
		# self.sm.add_widget(AboutToDoApp(name="about_app"))
		return self.sm

		# return ProfileCaptureScreen()
	

if __name__ == '__main__':
	FaceApp().run()