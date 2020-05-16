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

from .MAP_Func import MAP_Func

# Create your views here.

@login_required
def upload(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        restaurant = Restaurant.objects.get(user_id = request.user.id)
        if not restaurant.isActive:
            return render(request, 'users/profile.html', {'restaurant': restaurant})

    if request.method == 'POST':
        uploadSel_form = uploadForm(request.user.id, request.POST, request.FILES)
        if uploadSel_form.is_valid():
            pdf_file = uploadSel_form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)
            uploaded_file_loc = "{0}/{1}".format(fs.location, filename)

            # today = date.today()
            is_lunch = True if uploadSel_form.cleaned_data['Period']=='opt1' else False
            drivers = uploadSel_form.cleaned_data['drivers']
            driver_list = [ele.idDriver for ele in drivers]
            restaurant = Restaurant.objects.get(user_id = request.user.id)

            today = date.today()
            precess_data = threading.Thread(target=processOrder, args=[uploaded_file_loc,restaurant,driver_list,is_lunch])
            precess_data.start()
            return redirect('uploadDone')
        else:
            print('Fail')
    else:
        uploadSel_form = uploadForm(request.user.id)
    restaurant = Restaurant.objects.get(user_id = request.user.id)
    return render(request, 'upload/upload.html',{'restaurant':restaurant,'uploadSel_form':uploadSel_form})

def processOrder(uploaded_file_loc, restaurant, driver_list, is_lunch):
    today = date.today()
    print("Start processes")
    today = str(today)
    if uploaded_file_loc[-3:] == 'pdf':
        Order.pdf2DB(uploaded_file_loc,restaurant.idRestaurant,today, is_lunch)
        print('PDF2DB DONE')
    else:
        Order.csv2DB(uploaded_file_loc, restaurant.idRestaurant, today, is_lunch)
        print('CSV2DB DONE')
    Order.assign_order_driver(restaurant.idRestaurant,today,driver_list, is_lunch)
    print('assign_order_driver DONE!')
    Order.generate_sequence(restaurant,today,is_lunch)
    print('generate_sequence Done')

def uploadDone(request):
    return render(request, 'upload/upload_done.html')

@login_required
def order_for_kitchen(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        restaurant = Restaurant.objects.get(user_id = request.user.id)
        if not restaurant.isActive:
            return render(request, 'users/profile.html', {'restaurant': restaurant})

    datetime = Orders.objects.filter(idRestaurant_id=restaurant).all().aggregate(Max("OrderDate"))
    dic = Order.parser_meals(restaurant.idRestaurant,datetime['OrderDate__max'])
    dic = {key:(value,len(value)) for key,value in dic.items()}
    return render(request,'order_for_kitchen.html',{'restaurant': restaurant, 'orders':dic.items()})

@login_required
def get_order_sequence(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        restaurant = Restaurant.objects.get(user_id = request.user.id)
        if not restaurant.isActive:
            return render(request, 'users/profile.html', {'restaurant': restaurant})

    driver_id = request.GET.get('driver_id')
    date = request.GET.get('date')
    lst = Order.generate_deliver_list(driver_id,date)
    return JsonResponse(lst,safe=False)

@login_required
def driverManager(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        restaurant = Restaurant.objects.get(user_id = request.user.id)
        if not restaurant.isActive:
            return render(request, 'users/profile.html', {'restaurant': restaurant})

    if request.method == 'POST':
        driver_form = DriverForm(request.POST)
        if driver_form.is_valid():
            #Create a new driver
            new_driver = driver_form.save(commit=False)
            driver_form.save()
            restaurant = Restaurant.objects.get(user_id = request.user.id)
            restaurant.driverNumber = F('driverNumber') + 1
            restaurant.save()
        else:
            print('Fail')
    else:
        driver_form = DriverForm()
    restaurant = Restaurant.objects.get(user_id = request.user.id)
    drivers = Drivers.objects.filter(idRestaurant=restaurant)
    driver_form = DriverForm(initial={'idRestaurant': restaurant,'driverCode':genDriverCode(restaurant)})

    # #Partial code for Test
    # addr1 = MAP_Func.saveAddress("first address", 100,32)
    # addr2 = MAP_Func.saveAddress("Second address", 101,30)
    # addr3 = MAP_Func.saveAddress("third address", 99.9999,32.00001)
    # addr4 = MAP_Func.saveAddress("fourth address", 110.00025,32)
    # addr5 = MAP_Func.saveAddress("fifth address", 110,32)
    # coor1 = MAP_Func.findAndSaveNearPoint(addr1,max_radius=150)
    # coor2 = MAP_Func.findAndSaveNearPoint(addr2,max_radius=150)
    # coor3 = MAP_Func.findAndSaveNearPoint(addr3,max_radius=150)
    # coor4 = MAP_Func.findAndSaveNearPoint(addr4,max_radius=150)
    # coor5 = MAP_Func.findAndSaveNearPoint(addr5,max_radius=150)
    # print('Address 1: ')
    # print('Address 1: ', addr1)
    # print('Coor 1: ', coor1)
    # print('Address 2: ')
    # print('Address 2: ', addr2)
    # print('Coor 2: ', coor2)
    # print('Address 3: ')
    # print('Address 3: ', addr3)
    # print('Coor 3: ', coor3)
    # print('Address 4: ')
    # print('Address 4: ', addr4)
    # print('Coor 4: ', coor4)
    # print('Address 5: ')
    # print('Address 5: ', addr5)
    # print('Coor 5: ', coor5)
    # #End Partial code for Test

    return render(request, 'driver/driverManager.html',{'restaurant': restaurant, 'drivers':drivers, 'driver_form':driver_form})

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
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        restaurant = Restaurant.objects.get(user_id = request.user.id)
        if not restaurant.isActive:
            return render(request, 'users/profile.html', {'restaurant': restaurant})

    driver = Drivers.objects.get(idDriver=id)
    if request.method == "POST":
        if driver:
            driver.delete()
        return redirect('../../')
    return render(request, "driver/driverDelete.html", {"driver": driver})

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
        restaurant = Restaurant.objects.get(user_id = self.request.user.id)
        context['restaurant'] = restaurant

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
    return render(request,"contact_us.html",{'restaurant': restaurant})

@login_required
def printable_routes(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        restaurant = Restaurant.objects.get(user_id = request.user.id)
        if not restaurant.isActive:
            return render(request, 'users/profile.html', {'restaurant': restaurant})
            
    # restaurant = Restaurant.objects.get(user_id=request.user.id)
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
    # print(orders)
    meal2str = lambda meals: [key+" X "+value for key,value in meals.items()]
    for order in orders:
        if not order["DriverId__driverCode"]:
            if order["isPickup"]:
                driver_dic[("自提:", order['Address'])] \
                    .append({'idDisplay': order['idDisplay'],
                             'Address': order['Address'],
                             'Phone': order['Phone'],
                             'Note': order['Note'],
                             'Meals': meal2str(order['Meals'])})
            else:
                driver_dic[("错误订单", "")] \
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
    return render(request, "printable_routes.html",{'restaurant':restaurant,'drivers':driver_dic.items()})


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
    return render(request, "driver_item_list.html", {'restaurant': restaurant, 'drivers': driver_item.items()})