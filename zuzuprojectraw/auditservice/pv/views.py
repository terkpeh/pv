from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView,ListView,DetailView,UpdateView,View,CreateView
from django.views.generic.edit import CreateView,UpdateView
from pv.models import Pv,user_type,staff
from django.contrib.messages.views import SuccessMessageMixin,messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login,logout,get_user_model
from .import models
from .forms import GeneralpvForm,UpdatepvForm,UserLoginForm,standardUpdatepvForm,HonpvForm ,BenefitForm, HunUpdatepvForm,UpdateBenefitForm
# from datetime import datetime
import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Sum ,Q,Count
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers


# A class based view to list registered pv for a given year
class PvList(LoginRequiredMixin,ListView):
    template_name = 'pv/registeredpv.html' # state the html file this view class is controling
    context_object_name ='pvs' # context name u will using in loping through the data in the html file
    model = models.Pv # state the model in which u are using in this class based view
    paginate_by = 5 # the number of record u want to show on each page of the above mentioned html file
    today = datetime.datetime.now() # a variable storing todays date
    queryset = Pv.objects.all().filter(Date_recieved__year=today.year).order_by('-IA_System_Code') # this is a query that pulls all objects in the pv model for a given yr

#generate csv file
def getfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registeredpv.csv"'
    today = datetime.datetime.now()
    pvlist = Pv.objects.all().filter(Date_recieved__year=today.year).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response

class BeneficiaryList(LoginRequiredMixin,ListView):
    template_name = 'pv/beneficiary.html' # state the html file this view class is controling
    context_object_name ='pvs' # context name u will using in loping through the data in the html file
    model = models.staff # state the model in which u are using in this class based view
    paginate_by = 5 # the number of record u want to show on each page of the above mentioned html file
    today = datetime.datetime.now() # a variable storing todays date
    queryset = staff.objects.all().filter(Date_added__year=today.year).order_by('-id') # this is a query that pulls all objects in the pv model for a given yr

#generate csv file
def beneficiariess(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Beneficiaries.csv"'
    today = datetime.datetime.now()
    pvlist = staff.objects.all().filter(Date_added__year=today.year).order_by('id')
    writer = csv.writer(response)
    writer.writerow(['id','Pv_reference','Staff_Id','Name','Rank','Amount'])
    for pv in pvlist :
        writer.writerow([staff.id,staff.Pv_reference,staff.staff_id,staff.name,staff.rank,staff.amount])
    return response

class Nonwitholding(LoginRequiredMixin,ListView):
    template_name = 'pv/nonwitholding.html' # state the html file this view class is controling
    context_object_name ='pvs' # context name u will using in loping through the data in the html file
    model = models.Pv # state the model in which u are using in this class based view
    paginate_by = 5 # the number of record u want to show on each page of the above mentioned html file
    today = datetime.datetime.now() # a variable storing todays date
    queryset = Pv.objects.filter(Withholding_tax__lte =0.00, Date_recieved__year=today.year).order_by('-IA_System_Code') # this is a query that pulls all objects in the pv model for a given yr

#generate csv file
def Nonwitholdings(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Non-Withholding-Tax.csv"'
    today = datetime.datetime.now()
    pvlist =Pv.objects.filter(Withholding_tax__lte =0.00, Date_recieved__year=today.year).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response

class accountableimpress(LoginRequiredMixin,ListView):

    template_name = 'pv/accountableimpress.html' # state the html file this view class is controling
    context_object_name ='pvs' # context name u will using in loping through the data in the html file
    model = models.Pv # state the model in which u are using in this class based view
    paginate_by = 5 # the number of record u want to show on each page of the above mentioned html file
    today = datetime.datetime.now() # a variable storing todays date
    queryset = Pv.objects.filter(Acc_Impress__exact ='Yes',Date_recieved__year=today.year).order_by('-IA_System_Code') # this is a query that pulls all objects in the pv model for a given yr

#generate csv file
def accountableimpresss(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="accountable-impress.csv"'
    today = datetime.datetime.now()
    pvlist =Pv.objects.filter(Acc_Impress__exact ='Yes',Date_recieved__year=today.year).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response

class nonaccountableimpress(LoginRequiredMixin,ListView):
    template_name = 'pv/nonaccountableimpress.html' # state the html file this view class is controling
    context_object_name ='pvs' # context name u will using in loping through the data in the html file
    model = models.Pv # state the model in which u are using in this class based view
    paginate_by = 5 # the number of record u want to show on each page of the above mentioned html file
    today = datetime.datetime.now() # a variable storing todays date
    queryset = Pv.objects.filter(Acc_Impress__exact ='No',Date_recieved__year=today.year).order_by('-IA_System_Code') # this is a query that pulls all objects in the pv model for a given yr

#generate csv file
def nonaccountableimpresss(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="non-accountableimpress.csv"'
    today = datetime.datetime.now()
    pvlist =Pv.objects.filter(Acc_Impress__exact ='No',Date_recieved__year=today.year).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response

#A class based view to update the pv system
class PvUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Pv # state the model in which u are using in this class based view
    form_class = UpdatepvForm # call the update form class in form.py
    template_name = 'pv/updatepv.html' # state the html file this view class is controling
    context_object_name = 'pvs' # context name u will using in  in the html file

    # a method to be called when a pv updates succesfully. it redirects u to the pv details by passing the IA_System_Code as a keyword argument
    def get_success_url(self):
        return reverse_lazy('pv:pv-detail', kwargs={'pk': self.object.IA_System_Code})

    # a method to desplay a success message when when a pv updates succesfully
    def form_valid(self, form):
        messages.success(self.request, 'Pv updated successfully')
        return super().form_valid(form)

class HunUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Pv # state the model in which u are using in this class based view
    form_class = HunUpdatepvForm # call the update form class in form.py
    template_name = 'pv/hunupdatepv.html' # state the html file this view class is controling
    context_object_name = 'pvs' # context name u will using in  in the html file

    # a method to be called when a pv updates succesfully. it redirects u to the pv details by passing the IA_System_Code as a keyword argument
    def get_success_url(self):
        return reverse_lazy('pv:hondetails', kwargs={'pk': self.object.IA_System_Code})

    # a method to desplay a success message when when a pv updates succesfully
    def form_valid(self, form):
        messages.success(self.request, 'Pv updated successfully')
        return super().form_valid(form)

class BenefitUpdateView(LoginRequiredMixin,UpdateView):
    model = models.staff # state the model in which u are using in this class based view
    form_class = UpdateBenefitForm # call the update form class in form.py
    template_name = 'pv/benefitupdate.html' # state the html file this view class is controling
    context_object_name = 'pvs' # context name u will using in  in the html file



    # a method to desplay a success message when when a pv updates succesfully
    def form_valid(self, form):
        messages.success(self.request, 'Pv updated with success!')
        return super().form_valid(form)

# class standardPvUpdateView(LoginRequiredMixin,UpdateView):
#     model = models.Pv # state the model in which u are using in this class based view
#     form_class = standardUpdatepvForm # call the update form class in form.py
#     template_name = 'pv/standardupdatepv.html' # state the html file this view class is controling
#     context_object_name = 'pvs' # context name u will using in  in the html file
#
#     # a method to be called when a pv updates succesfully. it redirects u to the pv details by passing the IA_System_Code as a keyword argument
#     def get_success_url(self):
#         return reverse_lazy('pv:pv-detail', kwargs={'pk': self.object.IA_System_Code})
#
#     # a method to desplay a success message when when a pv updates succesfully
#     def form_valid(self, form):
#         messages.success(self.request, 'Pv updated with success!')
#         return super().form_valid(form)


#A class based view to show detailed pv
class PvDetailView(LoginRequiredMixin,DetailView):
    model = models.Pv # state the model in which u are sing in this class based view
    template_name = 'pv/detailpv.html'  # state the html file this view class is controling
    context_object_name = 'pvs'  # context name u will using in  in the html file

class HonDetailView(LoginRequiredMixin,DetailView):
    model = models.Pv # state the model in which u are sing in this class based view
    template_name = 'pv/detailhun.html'  # state the html file this view class is controling
    context_object_name = 'pvs'  # context name u will using in  in the html file





#A class based view to create a pv
class PvCreateView(LoginRequiredMixin,CreateView):
    model = models.Pv  # state the model in which u are using in this class based view
    form_class = GeneralpvForm # call the update form class in form.py
    template_name = 'pv/generalpv.html' # state the html file this view class is controling

    success_url = reverse_lazy('pv:registeredpv') # a success url that redirects u to the list of registered pv

    #a method to desplay a success message when when a pv is created succesfull

    def form_valid(self, form):
        messages.success(self.request, 'Pv created successfully')
        return super().form_valid(form)

class HunCreateView(LoginRequiredMixin,CreateView):
    model = models.Pv  # state the model in which u are using in this class based view
    form_class = HonpvForm # call the update form class in form.py
    template_name = 'pv/Honurarium.html' # state the html file this view class is controling

    success_url = reverse_lazy('pv:pv-benefit') # a success url that redirects u to the list of registered pv


    #a method to desplay a success message when when a pv is created succesfull


    def form_valid(self, form):
        messages.success(self.request, 'Pv created successfully')
        return super().form_valid(form)

class benefitCreateView(CreateView):
    model = models.staff  # state the model in which u are using in this class based view
    form_class = BenefitForm # call the update form class in form.py
    template_name = 'pv/benefit.html' # state the html file this view class is controling



    #a method to desplay a success message when when a pv is created succesfull
    def get(self, *args, **kwargs):
        today = datetime.datetime.now()
        form = self.form_class()
        staffs = staff.objects.all().filter(Date_added=today).order_by('-id')
        return render(self.request, self.template_name,{"form": form, "staffs": staffs})


    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [ instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)

    def form_valid(self, form):
        messages.success(self.request, 'Beneficiary added successfully')
        return super().form_valid(form)






# a function to to log in a user
def login_view(request):
    form = UserLoginForm(request.POST or None) #create an instance the UserLoginForm in the form.py passing in request.Post or None as an argument
    if form.is_valid(): # if the data passed to the UserLoginForm in the form.py is passes all the clean data methods
        username = form.cleaned_data.get('username') # get the username form the already clearned data in UserLoginForm class in the form.py and store it into a varible called username
        password = form.cleaned_data.get('password') # get the password form the already clearned data in UserLoginForm class in the form.py and store it into a varible called password
        user = authenticate(username=username, password=password) # re-authenticate the username and password and store it into variable called user
        login(request,user) # pass in the request and user as arguments into the login() functions
        type_obj = user_type.objects.get(user = user) # get object of the user from user_type model and save it into a variable called type_obj
        if user.is_authenticated and type_obj.is_director: #if user passes the authentication and his object_type is == is_director
            return redirect ('pv:dashboard') # redirect the user to the director homepage
        elif user.is_authenticated and type_obj.is_standard:  #if user passes the authentication and his object_type is == is_standard
            return redirect('pv:registeredpv') # redirect the user to the standard user homepage
        else:
            return redirect(request,'pv/management.html') # redirect the user to the managers user homepage which is yet to be added

    context = {
                'form': form, #context is the form itself
        }
    return render(request,"pv/login.html",context) # render login page with the request and context

# a function to log out a user
def logout_request(request):
    logout(request) #passout the request as an argument to the logout() function
    return redirect("pv:log") # redirect to the login page

# a class base view for the is_director homepage
class Dashboard(LoginRequiredMixin,ListView):
    template_name = 'pv/dashboard.html' #state the html file this view class is controling
    context_object_name ='pvs' # context name u will using in  in the html file
    model = models.Pv # state the model in which u are using in this class based view
    queryset = Pv.objects.all() # a query to select all records in the pv model
    returned =Pv.objects.filter(Status = 'Returned') #a query to all records where status =='Returned'
    canceled =Pv.objects.filter(Status = 'Cancelled') #a query to all records where status =='Cancelled'
    completed =Pv.objects.filter(Status = 'Completed') #a query to all records where status =='Completed'
    table =Pv.objects.annotate(month = TruncMonth('Date_recieved')) #a query to group all records into months based on the Date_recieved
    ccost_center_net = Pv.objects.values('Cost_center').annotate(Monthly =Sum('Net_amount')) #a query to sum up all Net_amount of each cost center
    today = datetime.datetime.now()
    qry = User.objects.all()
    withholdings = Pv.objects.filter(Withholding_tax__gt =0.00)
    Nonwitholdings =Pv.objects.filter(Withholding_tax__lte =0.00, Date_recieved__year=today.year)
    accountableimpresss =Pv.objects.filter(Acc_Impress__exact ='Yes',Date_recieved__year=today.year)
    nonaccountableimpresss =Pv.objects.filter(Acc_Impress__exact ='No',Date_recieved__year=today.year)
    # a method
    def get_context_data(self, **kwargs):
        today = datetime.datetime.now() # todays date saved into a variable today
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['total_pv'] = self.queryset.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).count() #count all records in pv model for each month of the current yr
        context['cancelled_pv'] = self.canceled.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).count() #count all cancelled pv for the month of the current yr
        context['returned_pv'] = self.returned.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).count()  #count all Returned pv for the month of the current yr
        context['completed_pv'] = self.completed.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).count() #count all completed pv for the month of the current yr
        context['cost_center_net'] = self.ccost_center_net.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('-Monthly') # filter the sum up all Net_amount of each cost center for every month
        context['table_pv'] = self.table.values('month').annotate(G=Sum('Gross_amount'), T=Sum('Withholding_tax'), N=Sum('Net_amount'),).values('month','G','T','N').filter(Date_recieved__year=today.year).order_by('month') # sum the gross, tax, and net for each month for the year
        context['chest_pv'] = self.table.values('month').annotate( c=Sum('returned_to_chest'),).values('month','c').filter(Date_recieved__year=today.year).order_by('month')
        context['qryr'] = self.qry.filter(Q(create__isnull=False) & Q(create__created__year=today.year)).annotate(counter=Count('create')).prefetch_related('create').order_by('-counter')
        context['withholding'] = self.withholdings.filter(Date_recieved__year=today.year).count()
        context['Nonwitholding'] = self.Nonwitholdings.filter(Date_recieved__year=today.year).count()
        context['accountableimpress'] = self.accountableimpresss.filter(Date_recieved__year=today.year).count()
        context['nonaccountableimpress'] = self.nonaccountableimpresss.filter(Date_recieved__year=today.year).count()

        return context

# a class based view of total proccesed pv for the current year
class Total_Processed_PV(LoginRequiredMixin,ListView):
    template_name = 'pv/totalregistedpv.html' # template name the view will control
    context_object_name ='pvs' # context name used on the template
    model = models.Pv # model been used
    paginate_by = 5 # no of items u want to show on each page of the template
    today = datetime.datetime.now() #todays date saved in a variable called today
    queryset = Pv.objects.all().filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('-IA_System_Code') # query to filter the total processed pv for the yr

#generate csv file
def totalfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="totalmonthly.csv"'
    today = datetime.datetime.now()
    pvlist = Pv.objects.all().filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response

# a class based view of total completed  pv for the current year
class Total_completed_PV(LoginRequiredMixin,ListView):
    template_name = 'pv/completed.html' # template name the view will control
    context_object_name ='pvs'  # context name used on the template
    model = models.Pv # model been used
    paginate_by = 5 # no of items u want to show on each page of the template
    today = datetime.datetime.now() #todays date saved in a variable called today
    completed =Pv.objects.filter(Status = 'Completed')  #a query to all records where status =='Completed'
    queryset = completed.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('-IA_System_Code') # query to filter the total completed pv for the yr

def completedfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Total_completed_PV.csv"'
    today = datetime.datetime.now()
    completed =Pv.objects.filter(Status = 'Completed')  #a query to all records where status =='Completed'

    pvlist =completed.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response


# a class based view of total returned pv for the current year
class Total_returned_PV(LoginRequiredMixin,ListView):
    template_name = 'pv/returned.html' # template name the view will control
    context_object_name ='pvs'  # context name used on the template
    model = models.Pv # model been used
    paginate_by = 5 # no of items u want to show on each page of the template
    today = datetime.datetime.now() #todays date saved in a variable called today
    returned =Pv.objects.filter(Status = 'Returned') #a query to all records where status =='Returned'
    queryset = returned.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('-IA_System_Code') # query to filter the total Returned pv for the yr

def returnedfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Total_returned_PV.csv"'
    today = datetime.now()
    returned =Pv.objects.filter(Status = 'Returned')  #a query to all records where status =='Completed'

    pvlist =returned .filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response

# a class based view of total Cancelled pv for the current year
class Total_cancelled_PV(LoginRequiredMixin,ListView):
    template_name = 'pv/cancelled.html' # template name the view will control
    context_object_name ='pvs'  # context name used on the template
    model = models.Pv # model been used
    paginate_by = 5 # no of items u want to show on each page of the template
    today = datetime.datetime.now()#todays date saved in a variable called today
    canceled =Pv.objects.filter(Status = 'Cancelled') #a query to all records where status =='Cancelled'
    queryset = canceled.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('-IA_System_Code') # query to filter the total Cancelled pv for the yr

def cancelledfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Total_cancelled_PV.csv"'
    today = datetime.datetime.now()
    canceled =Pv.objects.filter(Status = 'Cancelled')  #a query to all records where status =='Completed'

    pvlist =canceled.filter(Date_recieved__year=today.year,Date_recieved__month=today.month).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response

class Total_withholding_PV(LoginRequiredMixin,ListView):
    template_name = 'pv/witholding.html' # template name the view will control
    context_object_name ='pvs'  # context name used on the template
    model = models.Pv # model been used
    paginate_by = 5 # no of items u want to show on each page of the template
    today = datetime.datetime.now()#todays date saved in a variable called today
    Withholding =Pv.objects.filter(Withholding_tax__gt =0.00) #a query to all records where status =='Cancelled'
    # Withholding_tax__gt =0.00,Date_recieved__year=today.year
    queryset = Withholding.filter(Date_recieved__year=today.year).order_by('-IA_System_Code') # query to filter the total Cancelled pv for the yr

def withholdingtax(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Total-Withholding-Tax.csv"'
    today = datetime.datetime.now()
    Withholding =Pv.objects.filter(Withholding_tax__gt =0.00)  #a query to all records where status =='Completed'

    pvlist =Withholding.filter(Date_recieved__year=today.year).order_by('IA_System_Code')
    writer = csv.writer(response)
    writer.writerow(['IA_System_Code','IA_code','Date_recieved','Pv_reference','Source_of_Funding','Cost_center','Payee','Description','Account_code','Gross_amount','Withholding_tax','Net_amount','Status','Acc_Impress','Date_returned','Type_of_accounts','Type_of_pv'])
    for pv in pvlist :
        writer.writerow([pv.IA_System_Code,pv.IA_code,pv.Date_recieved,pv.Pv_reference,pv.Source_of_Funding,pv.Cost_center,pv.Payee,pv.Description,pv.Account_code,pv.Gross_amount,pv.Withholding_tax,pv.Net_amount,pv.Status,pv.Acc_Impress,pv.Date_returned,pv.Type_of_accounts,pv.Type_of_pv])
    return response


#custom serarch
class SearchView(ListView):
    model = Pv # model been used
    template_name = 'pv/search.html' # template name the view will control

    context_object_name = 'all_search_results' # context name used on the template

    # method to do do the actual search
    def get_queryset(self):
       result = super(SearchView, self).get_queryset()
       query = self.request.GET.get('search') # get the search critirial from the template
       if query:
          postresult = Pv.objects.filter(Pv_reference__exact=query) #filter th pv objects with the critirial
          result = postresult
       else:
           result = None
       return result  # return the searched results

class ReportView(ListView):
    model = Pv # model been used

    template_name = 'pv/report.html' # template name the view will control

    context_object_name = 'all_search_results' # context name used on the template

    # method to do do the actual search
    def get_queryset(self):
       result = super(ReportView, self).get_queryset()
       query = self.request.GET.get('search') # get the search critirial from the template
       today = datetime.datetime.now()
       if query:
           if query == "Withholding":
               postresult = Pv.objects.filter(Withholding_tax__gt =0.00,Date_recieved__year=today.year) #filter th pv objects with the critirial
           elif query =="Non-Withholding":
               postresult = Pv.objects.filter(Withholding_tax__lte =0.00, Date_recieved__year=today.year)
           elif query =="Accountable-Impress":
               postresult = Pv.objects.filter(Acc_Impress__exact ='Yes',Date_recieved__year=today.year)
           elif query =="Non-Accountable-Impress":
               postresult = Pv.objects.filter(Acc_Impress__exact = 'No',Date_recieved__year=today.year)
           else:
               postresult = Pv.objects.all()
           result = postresult
       else:
           result = None
       return result

    
