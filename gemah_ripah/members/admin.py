from django.contrib import admin

from models import Member, MemberRedeem


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "points", "is_active")


@admin.register(MemberRedeem)
class MemberRedeemAdmin(admin.ModelAdmin):
    list_display = ("member", "amount", "transaction_date")
