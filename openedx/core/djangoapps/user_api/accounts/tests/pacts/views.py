from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from common.djangoapps.student.tests.factories import UserFactory
from common.djangoapps.student.models import User
from common.djangoapps.student.models import UserProfile

class ProviderState():

    def account_setup(self, request):
        User.objects.filter(username="staff").delete()
        user_acc = UserFactory.create(username = "staff")
        user_acc.profile.name = "Lemon Seltzer"
        user_acc.profile.bio = "This is my bio"
        user_acc.profile.country = "ME"
        user_acc.profile.is_active = True
        user_acc.profile.goals = "Learn and Grow!"
        user_acc.profile.year_of_birth = 1901
        user_acc.profile.phone_number = "+11234567890"
        user_acc.profile.mailing_address = "Park Ave"
        user_acc.profile.save()
        return user_acc
    
@csrf_exempt
@require_POST
def provider_state(request):
    state_setup = {"I have a user's basic information": ProviderState().account_setup}

    request_body = json.loads(request.body)

    state = request_body.get('state')

    User.objects.filter(username="staff").delete()

    print('Setting up provider state for state value: {}'.format(state))

    state_setup["I have a user's basic information"](request)
    
    return JsonResponse({'result': state})