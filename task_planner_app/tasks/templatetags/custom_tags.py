from django import template
from tasks.models import Membership, Notification, TaskDependency

register = template.Library()

@register.inclusion_tag('show_notifications.html', takes_context=True)
def show_notifications(context):
	request_user = context['request'].user
	notifications = Notification.objects.filter(receiver=request_user).exclude(seen=True).order_by('-date')
	return {'notifications': notifications}
	
@register.filter(name='add_classes')
def add_classes(value, arg):
    '''
    Add provided classes to form field
    :param value: form field
    :param arg: string of classes seperated by ' '
    :return: edited field
    '''
    css_classes = value.field.widget.attrs.get('class', '')
    # check if class is set or empty and split its content to list (or init list)
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []
    # prepare new classes to list
    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    # join back to single string
    return value.as_widget(attrs={'class': ' '.join(css_classes)})
    
@register.simple_tag
def user_date_joined(group, user):
    return Membership.objects.get(group=group, user=user, status='Active').created_at.strftime("%d %B, %Y")

@register.simple_tag
def get_child_tasks(task):
    return TaskDependency.objects.filter(parent_task=task)