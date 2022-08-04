"""User related model definitions for SQLite3 database."""
from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from tasks.models import Tags


class UserManager(BaseUserManager):
    """Manager class for simplifying creation process for users and Django admins.

    Inherits:
        BaseUserManager: gives access to Django pre-built user manager methods.
    """
    def create_user(self, email, username, password=None):
        """Expedites user creation.

        Args:
            email: the user's email.
            username: the user's username.
            password (default None): the user's password.

        Returns:
            A simple user object.

        Raises:
            ValueError if no email or username is provided.
        """
        if not email:
            raise ValueError('An email address must be provided')
        if not username:
            raise ValueError('A username address must be provided')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, username, password=None):
        """Creates a user that can access the Django admin pages.

        Args:
            email: the user's email.
            username: the user's username.
            password (default None): the user's password.

        Returns:
            A simple user object that has admin permissions.

        Raises:
            ValueError if no email or username is provided.
        """
        if not email:
            raise ValueError('An email address must be provided')
        if not username:
            raise ValueError('A username address must be provided')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.password = make_password(password)
        user.save(using=self._db)
        return user


def get_profile_image_path(self, filename):
    """Returns the filepath for profile images."""
    return f'profile_images/{self.pk}/{"defa.png"}'


def get_default_profile_image():
    """Returns the filepath for the default profile image."""
    return 'default_image/default.png'
    

class User(AbstractBaseUser):
    """Base model for all authenticated users.
    
    Inherits:
        AbstractBaseUser: gives access to Django pre-built model methods and attributes.
    """
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_path, 
                                    null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField(default=10)
    workload = models.PositiveIntegerField(default=0)
    proficiencies = models.ManyToManyField(Tags)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth']
    
    def __str__(self):
        """Returns the name of object if type casted to str or .str() method is called."""
        return self.username
        
    def get_profile_image_filename(self):
        """Returns the filename for the user's profile image."""
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
        
    def has_perm(self):
        """Checks if the user is an admin."""
        return self.is_admin
        
    def has_module_perms(self):
        """Checks is the user has module permissions."""
        return True


class FriendList(models.Model):
    """Model for a user's friend list.
    
    Inherits:
        models.Model: gives access to Django pre-built model methods and attributes.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends') 

    def __str__(self):
        """Returns the name of object if type casted to str or .str() method is called."""
        return self.user.username

    def add_friend(self, account):
        """Add a new account to the friend list.
        
        Args:
            account: the user to be added.
        """
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        """Helper function to removes an account from the friend list.
        
        Args:
            account: the user to be removed.
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, account):
        """Removes an account from the friend list.

        Args:
            account: the user to be removed.
        """
        self.remove_friend(account)
        friends_list = FriendList.objects.get(user=account)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        """Checks if user and a second user, friend, are mutual friends."""
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    """Model for a user friend request.
    
    Inherits:
        models.Model: gives access to Django pre-built model methods and attributes.
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    is_active = models.BooleanField(blank=False, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns the sender's username if type casted to str or .str() method is called."""
        return self.sender.username

    def accept(self):
        """Processes the friend request if accepted by the receiver."""
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
        self.is_active = False
        self.save()

    def decline(self):
        """Processes the friend request if declined by the receiver."""
        self.is_active = False
        self.save()

    def cancel(self):
        """Processes the friend request if cancelled by the sender."""
        self.is_active = False
        self.save()
        