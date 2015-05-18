# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def react_view(request):
    return render(request, 'react-base.html')
