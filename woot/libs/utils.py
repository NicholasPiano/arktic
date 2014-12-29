#django

#local

#util
import string
import random

#vars
chars = string.ascii_uppercase + string.digits

def generate_id_token(Obj): #expects Obj.objects
  def get_id_token():
    return ''.join([random.choice(chars) for _ in range(8)]) #8 character string

  current_id_tokens = [obj.id_token for obj in Obj.objects.all()]
  id_token = get_id_token()
  while id_token in current_id_tokens:
    id_token = get_id_token()

  return id_token
