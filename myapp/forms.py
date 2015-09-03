from django import forms
from .models import *

class  SignUpForm(forms.Form):
	username = forms.CharField(max_length=50,min_length=4)
	password = forms.CharField(widget=forms.PasswordInput,min_length=6)
	email = forms.EmailField()
	first_name = forms.CharField(max_length=50,min_length=1,)
	last_name = forms.CharField(max_length=50,min_length=1,)

	def clean_username(self):
		data = self.cleaned_data['username']
		for existing_users in User.objects.all():
			if data == existing_users.username:
				raise forms.ValidationError("This username is already registered")
		return data			

	# def clean_email(self):
	# 	data = self.cleaned_data['email']
	# 	for existing_users in User.objects.all():
	# 		if data == existing_users.email:
	# 			raise forms.ValidationError("This email is already registered")
	# 	return data			

class SignInForm(forms.Form):
	username = forms.CharField(max_length=50,min_length=4)
	password = forms.CharField(widget=forms.PasswordInput,min_length=6)

# class Child_Profile_Form(forms.Form):
# 	name = forms.CharField(max_length=100,min_length=1)
# 	dob= forms.DateField()
# 	choices = [('male','male'),('female','female')]
# 	gender = forms.ChoiceField(choices=choices,widget=forms.RadioSelect())	
# 	grade = forms.CharField(required=False)
# 	image = forms.ImageField()

class Child_Profile_Form(forms.ModelForm):
	class Meta:
		model = Child
		fields = ['name', 'dob', 'gender', 'grade', 'image']
	def clean_image(self):
		image = self.cleaned_data.get('image',False)
		if image:
			if image._size > 4*1024*1024:
				raise forms.ValidationError("Image file too large ( > 4mb )")
			else :
				return image
		else :
			raise forms.ValidationError("Couldn't read uploaded image")	
