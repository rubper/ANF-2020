from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Ingrese su contraseña',
            'id' : 'password1',
            'required' : 'required',
        }
    ))
    password2 = forms.CharField(label = 'Contraseña de confirmación', widget = forms.PasswordInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Ingrese nuevamente su contraseña',
            'id' : 'password2',
            'required' : 'required',
        }
    ))

    class Meta:
        model = User
        fields = [
        'id',
        'nomUsuario',
        ]
        labels = {
        'id' : 'Id',
        'nomUsuario' : 'Nombre de usuario',
        }
        widgets = {
        'id' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el id'}),
        'nomUsuario' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de usuario'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UpdateUserForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Ingrese su contraseña',
            'id' : 'password1',
            'required' : 'required',
        }
    ))
    password2 = forms.CharField(label = 'Contraseña de confirmación', widget = forms.PasswordInput(
        attrs = {
            'class' : 'form-control',
            'placeholder' : 'Ingrese nuevamente su contraseña',
            'id' : 'password2',
            'required' : 'required',
        }
    ))
    id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'True'}))
    class Meta:
        model = User
        fields = [
        'id',
        'nomUsuario',
        ]
        labels = {
        'id' : 'Id',
        'nomUsuario' : 'Nombre de usuario',
        }
        widgets = {
        'nomUsuario' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de usuario'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
