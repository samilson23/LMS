# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^transaction/completed/$",
        views.TransactionCompletedView.as_view(),
        name="transaction_completed",
    ),
    re_path(
        r"^transaction/status/$",
        views.TransactionStatusView.as_view(),
        name="transaction_status",
    ),
    re_path(r"^transaction/ipn/$", views.IPNCallbackView.as_view(), name="transaction_ipn"),
]
