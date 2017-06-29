from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone    
from django.db.models import Q
from .models import Member,Bill, Transaction,WSGroup
from django.urls import reverse


def Signup(request):
    
    request.session['logerror']="false"
    request.session['signerror']="false"
    if request.method =='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        if not username or not email or not password or not confirmpassword:    
            request.session['signerror']="true"
            request.session['serrormessage']="All fields required"
        elif User.objects.filter(username=username).exists():
            request.session['signerror']="true"
            request.session['serrormessage']="Username already exist"
        elif not password == confirmpassword:
            request.session['signerror']="true"
            request.session['serrormessage']="Password do not match"
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            member=Member.objects.create(user=user)
            request.session['signerror']="false"
            return redirect('/home/')
    return render(request,'mess/login.html')

def Login(request):
    request.session['logerror']="false"
    request.session['signerror']="false"
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print username
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            request.session['username']=username
            request.session['logerror']="false"
            return redirect('/home/')
        else:
            request.session['logerror']="true"
            request.session['lerrormessage'] = "Invalid credentials"
            
    return render(request,'mess/login.html')                            

def Logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def index(request):
    member=Member.objects.get(user=request.user)
    mem_lenders=Transaction.objects.filter(lender=member, group__isnull=True)
    mem_receivers=Transaction.objects.filter(receiver=member, group__isnull=True)
    member_status={}
    for transaction in mem_lenders:
        if member_status.get(transaction.receiver.user.username):
            member_status[transaction.receiver.user.username] += transaction.amount 
        else:
            member_status[transaction.receiver.user.username] = transaction.amount

    for transaction in mem_receivers:
        if member_status.get(transaction.lender.user.username):
            member_status[transaction.lender.user.username] += -transaction.amount 
        else:
            member_status[transaction.lender.user.username] = -transaction.amount

    group_details=member.wsgroup_set.all()
    all_users=User.objects.all().exclude(username__in=["admin", request.user.username])
    user=request.user           
    return render(request,'mess/home.html',{'user':user,'all_users':all_users,'group_details':group_details})   



def Invoice(request):
    username=request.session['username']
    user=request.user
    users=User.objects.all()
    len_user=len(users)
    print len_user
    user_details=Member.objects.filter(user=user)
    total_ex=0
    for i in user_details:
        total=int(i.amount)
        total_ex=total+total_ex
        print total_ex
    mess_bill=Bill.objects.all()
    len_bil=len(mess_bill)
    print len_bil
    if len_bil== 0:
        grand_total=total_ex
        return render(request,'mess/invoice.html',{'total_ex':total_ex,'user':user,'user_details':user_details,'grand_total':grand_total,'mess_bill':mess_bill})
    for i in mess_bill:
        grand_t=int(i.electricity_bill)+int(i.water_bill)+int(i.rent)+int(i.other_expenses)
        grand_to=grand_t/4
        grand_total=grand_to-total_ex   
    if user is None:
        return render(request,'mess/home.html')
            
    return render(request,'mess/invoice.html',{'total_ex':total_ex,'user':user,'user_details':user_details,'grand_total':grand_total,'mess_bill':mess_bill})


def add_bill(request,id):
    user=Member.objects.get(user=request.user)
    group=WSGroup.objects.get(id=id)
    group_name=WSGroup.objects.filter(id=id)
    group_members=group.group_members.all()
    group_details=Transaction.objects.filter(group=group)
    if request.method=='POST':
        description=request.POST.get('description')
        amount=request.POST.get('amount')
        bill_type=request.POST.get('type')
        if not amount or not description or not bill_type :
            return redirect('group_report',id=id)   

        if bill_type=='invest':
            add_bill=Transaction.objects.create(lender=user,group=group,
                amount=amount,description=description,date=timezone.now())
            return redirect('group_report',id=id)   

        if bill_type=='spent':
            add_bill=Transaction.objects.create(receiver=user,group=group,
                amount=amount,description=description,date=timezone.now())
            return redirect('group_report',id=id)
    return redirect('group_report',id=id)          

@login_required(login_url='/')
def mtom_transaction(request):
    member=Member.objects.get(user=request.user)
    if request.method=='POST':
        receiver_id=request.POST.get("receiver")
        receiver=Member.objects.get(id=receiver_id)
        amount=request.POST.get('amount')
        description=request.POST.get('description')
        transaction=Transaction.objects.create(
            lender=member,receiver=receiver,
            amount=amount,description=description,
            date=timezone.now())
    transaction_list=Transaction.objects.filter(Q(lender=member)|Q(receiver=member))
    return HttpResponse('success')      

@login_required(login_url='/')
def member_report(request):
    member=Member.objects.get(user=request.user)
    mem_lenders=Transaction.objects.filter(lender=member)
    mem_receivers=Transaction.objects.filter(receiver=member)
    member_status={}
    for transaction in mem_lenders:
        if member_status.get(transaction.receiver.user.username):
            member_status[transaction.receiver.user.username] += transaction.amount 
        else:
            member_status[transaction.receiver.user.username] = transaction.amount

    for transaction in mem_receivers:
        if member_status.get(transaction.lender.user.username):
            member_status[transaction.lender.user.username] += -transaction.amount 
        else:
            member_status[transaction.lender.user.username] = -transaction.amount

    return render() 

@login_required(login_url='/')
def group_report(request,id):

    user=Member.objects.get(user=request.user)
    group=WSGroup.objects.get(id=id)
    group_name=WSGroup.objects.filter(id=id)
    group_members=group.group_members.all()
    group_details=Transaction.objects.filter(group=group)
    total_invest=0
    total_spent=0
    for i in group_details:
        if i.lender:
            print total_invest
            invest_amount=int(i.amount)
            total_invest+=invest_amount

        if i.receiver:   
            spent_amount=int(i.amount)
            total_spent+=spent_amount
    print "spent",total_spent
    print "invest",total_invest        
    balance_amount=total_invest- total_spent 
    print balance_amount
    return render(request,'mess/transactions.html',{'id':id,'balance_amount':balance_amount,'group_details':group_details,'group_members':group_members,'group_name':group_name})   

@login_required(login_url='/')
def group_creation(request):
    if request.method == 'POST':
        member=Member.objects.get(user=request.user)
        grname=request.POST.get("grname")
        members=request.POST.getlist("members")
        description=request.POST.get("description")
        if not grname or not description or not members:
            return redirect('/home/')   
        created_group= WSGroup.objects.create(group_name=grname,description=description)    
        member_objects = Member.objects.filter(user__username__in=members)
        created_group.group_members.add(*member_objects)
        created_group.group_members.add(member)
        return redirect('/home/')

    return redirect('/home/')

@login_required(login_url='/')
def mtog_transaction(request):
    member=Member.objects.get(user=request.user)
    if request.method=='POST':
        grp_id=request.POST.get('grname')
        grname=WSGroup.objects.get(id=grp_id)
        amount=request.POST.get('amount')
        description=request.POST.get('description')
        transaction=Transaction.objects.create(
            lender=member,group=grname,amount=amount,
            description=description,date=timezone.now())
        transaction_list=Transaction.objects.filter(Q(lender=member)|Q(group=grname))
    return render()



@login_required(login_url='/')
def settings(request):
    member=Member.objects.get(user=request.user)
    if request.method=='POST':
        profile_pic=request.FILES.get('filename')
        email=request.POST.get('email')
        phonenumber=request.POST.get('phonenumber')
        if not profile_pic or not email or not phonenumber:
            redirect('/home/')
        email_update=User.objects.get(username=member)
        email_update.email=email
        email_update.save()
        member.phonenumber=phonenumber
        member.profile_pic=profile_pic
        member.save()
        return redirect('/home/')
    return redirect('/home/')       