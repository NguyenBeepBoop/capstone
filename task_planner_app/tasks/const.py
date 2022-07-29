from xml.dom.minidom import Text
from django.db.models import TextChoices

STATUS_TODO = 'To do'
STATUS_INPROG = 'In progress'
STATUS_REV = 'Review'
STATUS_DONE = 'Complete'
STATUS_LOWEST = '5'
STATUS_LOW = '4'
STATUS_MED = '3'
STATUS_HIGH = '2'
STATUS_HIGHEST = '1'

class TaskStatus(TextChoices):
    TODO = STATUS_TODO, 'To Do'
    IN_PROGRESS = STATUS_INPROG, 'In Progress'
    REVIEW = STATUS_REV, 'Under Review'
    DONE = STATUS_DONE, 'Done'
    LOWEST = STATUS_LOWEST, 'Lowest'
    LOW = STATUS_LOW, 'Low'
    MEDIUM = STATUS_MED, 'Medium'
    HIGH = STATUS_HIGH, 'High'
    HIGHEST = STATUS_HIGHEST, 'Highest'

status_color = {
    STATUS_TODO: 'info',
    STATUS_INPROG: 'primary',
    STATUS_REV: 'warning',
    STATUS_DONE: 'success',
    STATUS_LOWEST: 'light',
    STATUS_LOW: 'secondary',
    STATUS_MED: 'info',
    STATUS_HIGH:  'warning',
    STATUS_HIGHEST: 'danger'
}