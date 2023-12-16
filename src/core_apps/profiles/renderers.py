import json
from rest_framework.renderers import JSONRenderer

class ProfileJSONRenderer(JSONRenderer):
    charset = 'utf-8' #character encoding to be used when serializing the data

