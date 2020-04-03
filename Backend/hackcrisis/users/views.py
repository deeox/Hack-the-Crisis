from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import CustomUser,People

class LoginApi(APIView):
    
    def get(self,request):
        return Response("LoginAuth APIView")

    def post(self,request):
        username = request.data.get('phoneno')
        password = request.data.get('password')
        login_type = int(request.data.get('type'))
        print(username,password)
        user = authenticate(username=username, password=password)

        if user is not None:

            if login_type == 1:
                people = People.objects.filter(user=user)[0]
                contextfrontend  = {"phoneno":user.phoneno,"firstname":user.firstname,
                        "lastname":user.lastname,"aadharno":people.aadharno,"tag":people.tag}
            elif login_type == 2:
                pass
                seller = Seller.objects.filter(user=user)[0]
                contextfrontend  = {"phoneno":user.phoneno,"firstname":user.firstname,
                        "lastname":user.lastname,"shopname":seller.shopname,"gst_no":seller.gst_no,"categ":seller.categ}
            else:
                pass
            #     admin = ZoneAdmin.objects.filter(user=user)[0]
            #     contextfrontend  = {"phoneno":user.phoneno,"firstname":user.firstname,
            #             "lastname":user.lastname,"aadharno":admin.aadharno,"tag":admin.tag}
            return Response(contextfrontend)

        else:
            return Response({"F"})

class RegisterApi(APIView):
    
    def get(self,request):
        return Response("Register APIView")

    def post(self,request):
        f_phoneno = request.data.get('phoneno')
        f_password = request.data.get('password')
        f_fname = request.data.get('firstname')
        f_lname = request.data.get('lastname')
        login_type = request.data.get('type')

        try:
            user,created = CustomUser.objects.get_or_create(phoneno = f_phoneno)

            if created:
                user.firstname = f_fname 
                user.lastname = f_lname
                user.set_password(f_password)
                user.save()

            if login_type == 1:
                f_aadharno = request.data.get('aadharno')
                f_lastloc = request.data.get('lastloc')
                f_district = request.data.get('district')
                f_tag = request.data.get('tag')

                people,created = People.objects.get_or_create(user = user)

                if created:
                    people.aadharno =f_aadharno 
                    people.lastloc =f_lastloc 
                    people.district = f_district
                    people.tag = f_tag
                    people.save()

            elif login_type == 2:
                shopname = request.data.get('shopname')
                gst_no = request.data.get('gst_no')
                categ = request.data.get('categ')

                shop,created = Shop.objects.get_or_create(user = user)

                if created:
                    shop.shopname =shopname 
                    shop.gst_no =gst_no 
                    shop.categ = categ
                    shop.save()
            else:
                pass
                # admin = ZoneAdmin.objects.filter(user=user)[0]
                # contextfrontend  = {"phoneno":user.phoneno,"firstname":user.firstname,
                #         "lastname":user.lastname,"aadharno":admin.aadharno,"tag":admin.tag}

            return Response({"Success"})
        except Exception as e:
            print(e)

        return Response({"F"})