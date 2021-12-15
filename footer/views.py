from django.shortcuts import render
from .forms import ContactForm



# Create your views here.

def contact(request):

	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			message = "Your Message/Feedback is sent, we will contact you soon. Thank You."
			return render(request,'footer/contact.html',{'message':message})
	else:
		form = ContactForm()
		context = {'form':form}
		return render(request,'footer/contact.html',context)

def about(request):
	return render(request,'footer/about.html')

def error_404_view(request,exception):
	return render(request,'footer/404.html')