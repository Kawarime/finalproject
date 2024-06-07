from django.shortcuts import render, redirect
from LMS.models import *
from LMS.forms import *
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
