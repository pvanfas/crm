from django.template import Library
from django.contrib.auth.models import User
register = Library()
from django.template.defaultfilters import stringfilter


@register.filter    
def check_default(value): 
	result = value
	if value == "default":
		result = "-"
	return result
                                                        
    
@register.filter
@stringfilter
def underscore_smallletter(value):
    value =  value.replace(" ", "_")
    return value
    

@register.filter
def to_fixed_two(value):
    return "{:10.2f}".format(value)


@register.filter
def tax_devide(value):
    return value/2