from rest_framework.views import APIView
from .serializers import UsersDataSerializer
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework import status
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist
from .models import UsersData
from json import loads
from django.core.validators import validate_email, URLValidator
from django.core.exceptions import ValidationError

# Create your views here.get(
class UsersDataList(APIView):
    def get(self, request : HttpRequest, id=None):
        #check the incoming request and validate them
        try:
            page_no = int(request.query_params.get('page', 1))
            limit_val = int(request.query_params.get('limit', 5))
        except ValueError:
            return Response({'status': 'fail', 'data': [], "message": "Incorrect Data Types For Params", 'status_code': 400}, status.HTTP_400_BAD_REQUEST)

        search_name = request.query_params.get('name', None)
        sort_val = request.query_params.get('sort', None)

        #fix the start and end point for pagination
        start = (page_no - 1)*limit_val
        end = limit_val+start

        if not id is None:
            try:
                userObj = UsersData.objects.get(id=id)
            except UsersData.DoesNotExist:
                return Response({'status': 'fail', 'data': [], "message": "No Data Found", 'status_code': 404}, status.HTTP_404_NOT_FOUND)
            info = UsersDataSerializer(userObj)
        else:
            #query for your desired data
            userObj = UsersData.objects.all()
            if search_name:
                userObj = userObj.filter(Q(first_name__icontains=search_name) | Q(last_name__icontains=search_name))

            if sort_val:
                desc = '-' if '-' in sort_val else ''
                order_col = sort_val.split('-')[-1]
                #check if sorting field exost in model
                try:
                    _ = UsersData._meta.get_field(order_col)
                except FieldDoesNotExist:
                    return Response({'status': 'fail', 'data': [], "message": "Sort Value is Incorrect", 'status_code': 400}, status.HTTP_400_BAD_REQUEST)
                userObj = userObj.order_by(desc+order_col)
            else:
                #sending latest created data first
                userObj = userObj.order_by('-id')
            userObj = userObj[start:end]
            if not userObj:
                return Response({'status': 'fail', 'data': [], "message": "No Data Found", 'status_code': 404}, status.HTTP_404_NOT_FOUND)
            #serialize and return the data
            info = UsersDataSerializer(userObj, many=True)

        return Response({'status': 'success', 'data': info.data, "message": "Data Fetched Successfully", 'status_code': 200}, status.HTTP_200_OK)

    def post(self, request: HttpRequest):
        in_data = loads(request.body)

        #check the incoming request and validate them
        empty_keys, missing_keys = [], []
        required_keys = ['first_name', 'last_name', 'company_name', 'city', 'state', 'zip', 'email', 'web', 'age']
        if not all(field in in_data for field in required_keys):
            for field in required_keys:
                if not field in in_data:
                    missing_keys.append(field)
            if missing_keys:
                return Response({'status': 'fail', 'data': [], "message": "Json Data has empty keys: Keys - "+', '.join(missing_keys), 'status_code': 400}, status.HTTP_400_BAD_REQUEST)

        for key, value in in_data.items():
            if not value:
                empty_keys.append(key)
        if empty_keys:
            return Response({'status': 'fail', 'data': [], "message": "Json Data has empty keys: Keys - "+', '.join(empty_keys), 'status_code': 400}, status.HTTP_400_BAD_REQUEST)

        #apply some extra validations
        try:
            in_data['user_age'] = int(in_data['age'])
            in_data['zip_code'] = int(in_data['zip'])
            if in_data['user_age'] <= 0 or in_data['zip_code'] <= 0 or in_data['user_age'] >= 120:
                raise ValueError
            _ = validate_email(in_data['email'])
            in_data['email'] = in_data['email'].lower()
            del in_data['age']
            del in_data['zip']
        except ValueError:
            return Response({'status': 'fail', 'data': [], "message": "Incorrect Data For User, Age an Zip has to be integers and cannot be zero and age cannot be greater than 150", 'status_code': 400}, status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'status': 'fail', 'data': [], "message": "Email Not Valid", 'status_code': 400}, status.HTTP_400_BAD_REQUEST)

        #check if the exact first name and last name and email exist in db or not, this check is not necessary, but to stop data redundancy
        data_exist = UsersData.objects.filter(first_name__iexact=in_data['first_name'], last_name__iexact=in_data['last_name'], email=in_data['email'])
        if data_exist:
            return Response({'status': 'fail', 'data': [], "message": "A user with the exact same name and email already exist", 'status_code': 400}, status.HTTP_400_BAD_REQUEST)

        #feed the data to the serializer for validation of fields 
        new_data = UsersDataSerializer(data=in_data)
        if new_data.is_valid():
            try:
                new_data.save()
                return Response({'status': 'success', 'data': new_data.data, "message": "Data Created Successfully", 'status_code': 201}, status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'status': 'fail', 'data': [], "message": "DB Error Occured, "+str(e), 'status_code': 500}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'status': 'fail', 'data': [], "message": "Error Occured, "+str(new_data.errors), 'status_code': 500}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request: HttpRequest, id=None):
        in_data = loads(request.body)

        if not in_data:
            return Response({'status': 'fail', 'data': [], "message": "No Json Data Received", 'status_code': 400}, status.HTTP_400_BAD_REQUEST)

        if id is None:
            return Response({'status': 'fail', 'data': [], "message": "Id is missing for deletion", 'status_code': 400}, status.HTTP_400_BAD_REQUEST)
        try:
            userObj = UsersData.objects.get(id=id)
        #check if record exist or not
        except UsersData.DoesNotExist:
            return Response({'status': 'fail', 'data': [], "message": "No Data Found", 'status_code': 404}, status.HTTP_404_NOT_FOUND)

        update_error, empty_keys = {}, []
        #check if the values given for updation are valid
        for key, value in in_data.items():
            if not value:
                empty_keys.append(key)
        if empty_keys:
            return Response({'status': 'fail', 'data': [], "message": "Json Data has empty keys: Keys - "+', '.join(empty_keys), 'status_code': 400}, status.HTTP_400_BAD_REQUEST)

        #start updating the values, could have user '.filter()' & '.update()' and as well, but for single record this is fine
        #update first_name
        if 'first_name' in in_data:
            if userObj.first_name == in_data['first_name']:
                update_error['first_name'] = "Value same as in DB"
            else:
                userObj.first_name = in_data['first_name']
        #update last_name
        if 'last_name' in in_data:
            if userObj.last_name == in_data['last_name']:
                update_error['last_name'] = "Value same as in DB"
            else:
                userObj.last_name = in_data['first_name']
        #update company_name
        if 'company_name' in in_data:
            if userObj.company_name == in_data['company_name']:
                update_error['company_name'] = "Value same as in DB"
            else:
                userObj.company_name = in_data['company_name']
        #update user_age
        if 'age' in in_data:
            try:
                user_age = int(in_data['age'])
                if user_age <=0 or user_age >=150:
                    update_error['age'] = "Age cannot less than or greater than 0, 150"
                elif userObj.user_age == user_age:
                    update_error['age'] = "Value same as in DB"
                else:
                    userObj.user_age = user_age
            except ValueError:
                update_error['age'] = "Age needs to be integer"
        #update city
        if 'city' in in_data:
            if userObj.city == in_data['city']:
                update_error['city'] = "Value same as in DB"
            else:
                userObj.city = in_data['city']
        #update state
        if 'state' in in_data:
            if userObj.state == in_data['state']:
                update_error['state'] = "Value same as in DB"
            else:
                userObj.state = in_data['state']
        #update zip_code
        if 'zip' in in_data:
            try:
                zip_code = int(in_data['zip'])
                if zip_code <=0:
                    update_error['zip'] = "Zip cannot less than 0"
                elif userObj.zip_code == zip_code:
                    update_error['zip'] = "Value same as in DB"
                else:
                    userObj.zip_code = zip_code
            except ValueError:
                update_error['zip'] = "Age needs to be integer"
        #update email
        if 'email' in in_data:
            if userObj.email == in_data['email'].lower():
                update_error['email'] = "Value same as in DB"
            else:
                try:
                    _ = validate_email(in_data['email'])
                    userObj.email = in_data['email'].lower()
                except ValidationError:
                    update_error['email'] = "Email Not Valid"
        #update web
        if 'web' in in_data:
            if userObj.web == in_data['web']:
                update_error['web'] = "Value same as in DB"
            else:
                validator = URLValidator()
                try:
                    validator(in_data['web'])
                    userObj.web = in_data['web']
                except ValidationError as exception:
                    update_error['web'] = "URL Not Valid"

        try:
            userObj.save()
            not_updated_fields = ''
            if update_error:
                not_updated_fields = ',\n '.join([f"{key} : {value}" for key, value in update_error.items()])
            return Response({'status': 'success', 'data': UsersDataSerializer(userObj).data, "message": "Data Updated Successfully", "unchanged_fields": not_updated_fields, 'status_code': 200}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'fail', 'data': [], "message": "DB Error Occured, "+str(e), 'status_code': 500}, status.HTTP_500_INTERNAL_SERVER_ERROR)


    """### this method should have a confirm param as well, to avoid accidental deletion ###"""
    def delete(self, request: HttpRequest, id=None):
        #check if id is present in url
        if id is None:
            return Response({'status': 'fail', 'data': [], "message": "Id is missing for deletion", 'status_code': 400}, status.HTTP_400_BAD_REQUEST)
        try:
            _ = UsersData.objects.get(id=id).delete()
            return Response({'status': 'success', 'data': [], "message": "Data deleted Successfully", 'status_code': 200}, status.HTTP_200_OK)
        #check if record exist or not
        except UsersData.DoesNotExist:
            return Response({'status': 'fail', 'data': [], "message": "No Data Found", 'status_code': 404}, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': 'fail', 'data': [], "message": "DB Error Occured, "+str(e), 'status_code': 500}, status.HTTP_500_INTERNAL_SERVER_ERROR)
