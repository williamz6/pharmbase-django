from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from backend.models import Order, OrderItem, Drug


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(user=user, username=user.username, email=user.email)

# @receiver(post_save, sender=OrderItem)
# def update_order_total_price(sender, instance, **kwargs):
#     order = instance
#     order_price = sum(item.quantity *item.drug.price_per_item for order.orderitem_set.all())

@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    total_amount = sum(item.quantity * item.drug.price_per_item for item in order.items.all())
    order.total_price = total_amount
    order.save()


@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.firstName
        user.last_name = profile.lastName
        user.username = profile.username
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
