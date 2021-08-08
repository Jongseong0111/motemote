import json, re, bcrypt, jwt, random, uuid

from django.views         import View
from django.http.response import JsonResponse
from django.db.models     import Q

from users.models         import Member
from my_settings          import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            id       = re.compile("[a-z0-9]{5,19}$")
            password = re.compile("[0-9]{8,16}")
            email    = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-z0-9-]+\.[a-zA-z0-9-]+$")

            if not password.match(data['password']) or not id.match(data['account']) or not email.match(data['email']):
                return JsonResponse({'MESSAGE':' INVALID_FORMAT'}, status=400)

            if Member.objects.filter(account = data["account"]).exists():
                return JsonResponse({"MESSAGE": "ALREADY_EXIST"}, status=400)

            encoded_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            Member.objects.create(
                account      = data['account'],
                password     = encoded_pw.decode('utf-8'),
                name         = data['name'],
                address      = data['address'],
                phone_number = data['phone_number'],
                email        = data['email'],
                points       = random.randrange(10000, 1000000)
             )
            return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)


class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not Member.objects.filter(account=data['account']).exists():
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=402)
            
            member = Member.objects.get(account=data['account'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), member.password.encode('utf-8')):
                return JsonResponse({"MESSAGE": "UNAUTHORIZED"}, status=401)
                
            token = jwt.encode({'id': member.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({"TOKKEN": token}, status=200)              

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)                


class FindMemberView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not Member.objects.filter(Q(email = data['email'])& Q(name=data['name'])).exists():
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=400)
            
            member = Member.objects.get(Q(email = data['email'])& Q(name=data['name']))

            result = {
                "name"    : member.name,
                "account" : member.account,
                "email"   : member.email  
            }
            return JsonResponse({"RESULT" : result}, status = 200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


class NewPasswordView(View):
    def patch(self, request):
        try:
            data = json.loads(request.body)
            if not Member.objects.filter(Q(account=data['account'])&Q(name=data['name'])&Q(email=data['email'])).exists():
                return JsonResponse({"MESSAGE": "INPUT_ERROR"}, status=400)
            
            member        = Member.objects.get(account=data['account'])
            password      = uuid.uuid1().hex
            encoded_password    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            member.password = encoded_password.decode('utf-8')
            member.save()

            return JsonResponse({"MESSAGE": password}, status=200)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

            

