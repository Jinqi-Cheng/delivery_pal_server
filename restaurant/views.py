from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Max

from django.http import JsonResponse
from .models import Orders, Drivers
from accounts.models import Restaurant
from .Order import Order
from .forms import DriverForm, uploadForm
from .tables import OrderTable,OrderFilter
from django.db.models import Sum
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from datetime import date
import threading
import decimal

from collections import defaultdict
# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    if request.method == 'POST':
        uploadSel_form = uploadForm(request.user.id, request.POST, request.FILES)
        if uploadSel_form.is_valid():
            # print(uploadSel_form.cleaned_data)
            pdf_file = uploadSel_form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)
            uploaded_file_loc = "{0}/{1}".format(fs.location, filename)
            # print('URL : ', uploaded_file_loc)

            # today = date.today()
            is_lunch = True if uploadSel_form.cleaned_data['Period']=='opt1' else False
            drivers = uploadSel_form.cleaned_data['drivers']
            driver_list = [ele.idDriver for ele in drivers]
            restaurant = Restaurant.objects.get(user_id = request.user.id)
            # print(driver_list)

            today = date.today()
            precess_data = threading.Thread(target=processOrder, args=[uploaded_file_loc,restaurant,driver_list,is_lunch])
            precess_data.start()
            return redirect('uploadDone')
        else:
            print('Fail')
    else:
        uploadSel_form = uploadForm(request.user.id)
    restaurant = Restaurant.objects.get(user_id = request.user.id)
    # return render(request, 'home_upload.html',{'restaurant':restaurant,'uploadSel_form':uploadSel_form})
    return render(request, 'upload.html',{'restaurant':restaurant,'uploadSel_form':uploadSel_form, 'website':"dashboard"})

def processOrder(uploaded_file_loc, restaurant, driver_list, is_lunch):
    today = date.today()
    print("Start processes")
    today = str(today)
    if uploaded_file_loc[-3:] == 'pdf':
        Order.pdf2DB(uploaded_file_loc,restaurant.idRestaurant,today, is_lunch)
        print('PDF2DB DONE')
    else:
        Order.csv2DB_check(uploaded_file_loc, restaurant.idRestaurant, today, is_lunch)
        print('CSV2DB DONE')
    Order.assign_order_driver(restaurant.idRestaurant,today,driver_list, is_lunch)
    print('assign_order_driver DONE!')
    Order.generate_sequence(restaurant,today,is_lunch)
    print('generate_sequence Done')

def uploadDone(request):
    return render(request, 'upload_done.html')

@login_required
def order_for_kitchen(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    restaurant = Restaurant.objects.get(user_id=request.user.id)
    datetime = Orders.objects.filter(idRestaurant_id=restaurant).all().aggregate(Max("OrderDate"))
    dic = Order.parser_meals(restaurant.idRestaurant,datetime['OrderDate__max'])
    dic = {key:(value,len(value)) for key,value in dic.items()}
    return render(request,'order_for_kitchen.html',{'restaurant': restaurant, 'orders':dic.items(), 'website':"order_for_kitchen"})

def get_order_sequence(request):
    driver_id = request.GET.get('driver_id')
    date = request.GET.get('date')
    isError = request.GET.get('isError')
    lst = Order.generate_deliver_list(driver_id,date,True if isError == '1' else False)
    return JsonResponse(lst,safe=False)

def driverManager(request):
    if request.method == 'POST':
        driver_form = DriverForm(request.POST)
        if driver_form.is_valid():
            #Create a new driver
            new_driver = driver_form.save(commit=False)
            driver_form.save()
            restaurant = Restaurant.objects.get(user_id = request.user.id)
            restaurant.driverNumber = F('driverNumber') + 1
            restaurant.save()
            # print('New Name:', new_driver.driverName)
            # print('New Code:', new_driver.driverCode)
            # print('New ID:', new_driver.idDriver)
            # redirect('restaurant/driverManager')
        else:
            print('Fail')
    else:
        driver_form = DriverForm()
    restaurant = Restaurant.objects.get(user_id = request.user.id)
    drivers = Drivers.objects.filter(idRestaurant=restaurant)

    driver_form = DriverForm(initial={'idRestaurant': restaurant,'driverCode':genDriverCode(restaurant)})
    # driver_form = DriverForm(initial={'idRestaurant': restaurant,'driverCode':genDriverCode(request.user.id, drivers)})
    return render(request, 'driverManager.html',{'restaurant': restaurant, 'drivers':drivers, 'driver_form':driver_form, 'website':"driverManager"})

def genDriverCode(restaurant):
    alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    rest_id = restaurant.idRestaurant
    next_id = restaurant.driverNumber+1
    rest_code = ''
    num_code = ''
    while(rest_id!=0):
        rest_id, i = divmod(rest_id, 36)
        rest_code = alphabet[i] + rest_code
    if len(rest_code)<3:
        rest_code= rest_code.zfill(3)

    while(next_id!=0):
        next_id, i = divmod(next_id, 36)
        num_code = alphabet[i] + num_code
    if len(num_code)<3:
        num_code= num_code.zfill(3)

    return rest_code+num_code


@login_required
def driverDelete(request, id):
    driver = Drivers.objects.get(idDriver=id)
    if request.method == "POST":
        if driver:
            driver.delete()
        return redirect('../../')
    return render(request, "driverDelete.html", {"driver": driver})

# @login_required
class orderHistoryWithFilter(SingleTableMixin, FilterView):
    table_class = OrderTable
    model = Orders
    template_name = "order_history.html"
    filterset_class = OrderFilter
    paginate_by = 15

    def get_queryset(self):
        restaurant = Restaurant.objects.get(user_id = self.request.user.id)
        return Orders.objects.filter(idRestaurant=restaurant)

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # get the default context data
        query = self.filterset.qs
        if not query:
            context['commission'] = 0
            context['amount'] = 0
        else:
            amount = query.aggregate(Sum('Price'))
            commission = amount['Price__sum']*decimal.Decimal(0.4)
            commission = "{:.3f}".format(commission)
            amount = "{:.2f}".format(decimal.Decimal(amount['Price__sum']))
            context['commission'] = commission
            context['amount'] = amount
        return context

@login_required
def contact_us(request):
    restaurant = Restaurant.objects.get(user_id=request.user.id)
    return render(request,"contact_us.html",{'restaurant': restaurant, 'website':"contact_us"})

@login_required
def printable_routes(request):
    restaurant = Restaurant.objects.get(user_id=request.user.id)
    datetime = Orders.objects.filter(idRestaurant_id=restaurant).all().aggregate(Max("OrderDate"))
    orders = Orders.objects.filter(idRestaurant_id=restaurant,
                                   OrderDate=datetime['OrderDate__max']).values("DriverId__driverCode",
                                                                                "DriverId__driverName",
                                                              "idDisplay",
                                                              "Address",
                                                              "Phone",
                                                              "Note",
                                                              "isPickup",
                                                              "Meals").order_by("Sequence")
    driver_dic = defaultdict(list)
    error_dic = defaultdict(list)
    pickup_dic = defaultdict(list)
    # print(orders)
    meal2str = lambda meals: [key+" X "+value for key,value in meals.items()]
    for order in orders:
        if not order["DriverId__driverCode"]:
            if order["isPickup"]:
                pickup_dic[("自提:", order['Address'])] \
                    .append({'idDisplay': order['idDisplay'],
                             'Address': order['Address'],
                             'Phone': order['Phone'],
                             'Note': order['Note'],
                             'Meals': meal2str(order['Meals'])})
            else:
                error_dic[("错误订单", "")] \
                    .append({'idDisplay': order['idDisplay'],
                             'Address': order['Address'],
                             'Phone': order['Phone'],
                             'Note': order['Note'],
                             'Meals': meal2str(order['Meals'])})
        else:
            driver_dic[(order["DriverId__driverName"],order["DriverId__driverCode"])]\
                .append({'idDisplay':order['idDisplay'],
                         'Address':order['Address'],
                         'Phone':order['Phone'],
                         'Note':order['Note'],
                         'Meals':meal2str(order['Meals'])})
    return render(request, "printable_routes.html",{'restaurant':restaurant,'drivers':driver_dic.items(),
                                                    'error':error_dic.items(),'pickup':pickup_dic.items(),
                                                    'website':"printable_routes"})


@login_required
def orderHistory(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    restaurant = Restaurant.objects.get(user_id = request.user.id)
    drivers = Drivers.objects.filter(idRestaurant=restaurant)
    orders = []
    for driver in drivers:
        orders += Orders.objects.filter(DriverId=driver)
    return render(request, 'order_history.html',{'restaurant': restaurant,'orders':orders})

@login_required
def driver_item_list(request):
    restaurant = Restaurant.objects.get(user_id=request.user.id)
    datetime = Orders.objects.filter(idRestaurant_id=restaurant).all().aggregate(Max("OrderDate"))
    orders = Orders.objects.filter(idRestaurant_id=restaurant,
                                   OrderDate=datetime['OrderDate__max']).values("DriverId__driverCode",
                                                                                "DriverId__driverName",
                                                                                "Address",
                                                                                "isPickup",
                                                                                "Meals").order_by("Sequence")
    driver_dic = defaultdict(lambda: defaultdict(int))
    # print(orders)
    # meal2str = lambda meals: [key + " X " + value for key, value in meals.items()]
    for order in orders:
        if not order["DriverId__driverCode"]:
            if order["isPickup"]:
                for meal,num in order['Meals'].items():
                    # print(meal,num)
                    driver_dic[("自提:", order['Address'])][meal]+=int(num)
            else:
                for meal,num in order['Meals'].items():
                    # print(meal, num)
                    driver_dic[("错误订单", "")][meal]+=int(num)
        else:
            for meal, num in order['Meals'].items():
                # print(meal, num)
                driver_dic[(order["DriverId__driverName"], order["DriverId__driverCode"])][meal] += int(num)
    driver_item = defaultdict(list)
    for name,orders in driver_dic.items():
        driver_item[name] += [(key,value) for key,value in orders.items()]
    return render(request, "driver_item_list.html", {'restaurant': restaurant, 'drivers': driver_item.items(), 'website':"driver_item_list"})

@login_required
def printable_driver_sequence(request):
    restaurant = Restaurant.objects.get(user_id=request.user.id)
    datetime = Orders.objects.filter(idRestaurant_id=restaurant).all().aggregate(Max("OrderDate"))
    orders = Orders.objects.filter(idRestaurant_id=restaurant,
                                   OrderDate=datetime['OrderDate__max']).values("DriverId__driverCode",
                                                                                "DriverId__driverName",
                                                                                "idDisplay",
                                                                                "Address",
                                                                                "Phone",
                                                                                "Note",
                                                                                "isPickup",
                                                                                "Meals").order_by("Sequence")
    driver_dic = defaultdict(list)
    error_dic = defaultdict(list)
    pickup_dic = defaultdict(list)
    meal2str = lambda meals: [key + " X " + value for key, value in meals.items()]
    for order in orders:
        if not order["DriverId__driverCode"]:
            if order["isPickup"]:
                pickup_dic[("自提:", order['Address'])] \
                    .append({'idDisplay': order['idDisplay'],
                             'Address': order['Address'],
                             'Phone': order['Phone'],
                             'Note': order['Note'],
                             'Meals': meal2str(order['Meals'])})
            else:
                error_dic[("错误订单", "")] \
                    .append({'idDisplay': order['idDisplay'],
                             'Address': order['Address'],
                             'Phone': order['Phone'],
                             'Note': order['Note'],
                             'Meals': meal2str(order['Meals'])})
        else:
            driver_dic[(order["DriverId__driverName"], order["DriverId__driverCode"])] \
                .append({'idDisplay': order['idDisplay'],
                         'Address': order['Address'],
                         'Phone': order['Phone'],
                         'Note': order['Note'],
                         'Meals': meal2str(order['Meals'])})
    driver_seq_clipboard = ""
    index = 1
    for key,value in driver_dic.items():
        driver_seq_clipboard+="第 {} 条送餐路线: ".format(index)
        index+=1
        for order in value:
            driver_seq_clipboard+= str(order['idDisplay'])+" "
        driver_seq_clipboard+="\n"

    return render(request, "printable_driver_sequence.html",
                  {'restaurant': restaurant, 'drivers': driver_dic.items(), 'error': error_dic.items(),
                   'pickup': pickup_dic.items(), 'driver_seq_clipboard':driver_seq_clipboard,'website':"printable_driver_sequence"})