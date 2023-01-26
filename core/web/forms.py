from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.widgets import CheckboxInput

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(
    #     label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('NID','phone_number')
    
    def fetch_administration_info(self,NID):
        import requests

        # Make a GET request to the API
        response = requests.post(f'https://smarthrapi.mifotra.gov.rw/employees/getCitizen/{NID}')

        # Check for a successful response
        if response.status_code == 200:
            # Convert the JSON response to a Python dictionary
            data = response.json()
            return data
        else:
            raise forms.ValidationError("Failed to fetch data from the National ID")

    def save(self, commit=True):
        # Save the provided password in hashed format and all the other information

        user = super(UserAdminCreationForm, self).save(commit=False)
        # set username
        user.username = self.cleaned_data["NID"]
        user.set_password(self.cleaned_data["phone_number"])

        # fetch data from the api using the NID from the form
        data = self.fetch_administration_info(user.NID)

        # add other data
        user.full_name = data['surnames']+' '+data['foreName']
        user.father_names = data['fatherNames']
        user.mother_names = data['motherNames']
        user.date_of_birth = data['dateOfBirth']
        user.place_of_birth = data['placeOfBirth']
        user.birth_country = data['birthCountry']
        user.village = data['village']
        user.cell = data['cell']
        user.sector = data['sector']
        user.district = data['district']
        user.province = data['province']
        user.marital_status = data['maritalStatus']
        user.spouse = data['spouse']
        user.is_active = True
        user.admin = False
        user.staff = False
        user.is_superuser = False
        user.save()
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ToggleButton(CheckboxInput):
    template_name = 'toggle_button/toggle-button.html'

    def __init__(self, attrs=None, check_test=None, round=False, buttonType=""):
        self.round = round
        self.klass = buttonType
        super().__init__(attrs, check_test)

    def get_context(self, name, value, attrs=None):
        context = super().get_context(name, value, attrs)
        context.update({
            "round": self.round,
            "klass": self.klass,
        })
        return context

    class Media:
        css = {
            "all": [
                "toggle_button/css/toggle-button.css",
            ]
        }
