from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


from msguide.models import (
    UserProfile,
    University,
)
# Create your views here.


class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    fields = [f.name for f in UserProfile._meta.get_fields()]
    fields.remove('email')
    template_name = "msguide/UserProfile.html"
    success_message = 'Data updated successfully.'
    success_url = '/userhome/2'

    def form_valid(self, form):
        form_valid = super(UserProfileUpdateView, self).form_valid(form)
        return form_valid


def index(request):
    return render(request, 'msguide/home.html')


class CheckForGreListView(LoginRequiredMixin, ListView):
    model = University
    template_name = "msguide/check_with_gre.html"
    paginated_by = 5

    def get_queryset(self):
        queryset = super(CheckForGreListView, self).get_queryset()
        user_query = UserProfile.objects.filter(email=self.request.user.email)
        budget = user_query[0].Budget
        user_data = []
        user_data.append(user_query[0].gre_verbal)
        user_data.append(user_query[0].gre_writing)
        user_data.append(user_query[0].gre_quantitative)
        user_data.append(user_query[0].gre_percentile)
        user_data.append(user_query[0].graduation_CGPA)
        user_data.append(user_query[0].work_experience)
        preferred_location = user_query[0].preferred_country
        df = pd.read_csv('student.csv')
        X_train = df.iloc[:, 0: 6].values
        y_train = df.iloc[:, -1].values
        data = [user_data]
        data = np.array(data)
        svm_model_linear = SVC(kernel='linear', C=1).fit(X_train, y_train)
        svm_predictions = svm_model_linear.predict(data)
        grade = svm_predictions.reshape(1, 1)[0]
        student_grade = grade[0]

        university_df = pd.read_csv('college.csv')
        # result = (university_df[university_df.Grade == grade]).sort_values(by = 'Overall Rating', ascending = False)
        queryset = queryset.filter(grade=student_grade)
        queryset = queryset.filter(fees_in_lakhs__lte=budget + 4)
        queryset = queryset.order_by('-overall_rating')
        if preferred_location != 'all':
            queryset = queryset.filter(country=preferred_location)
        return queryset


class CheckForToeflListView(LoginRequiredMixin, ListView):
    model = University
    template_name = "msguide/check_with_toefl.html"
    paginated_by = 5

    def get_queryset(self):
        queryset = super(CheckForToeflListView, self).get_queryset()
        user_query = UserProfile.objects.filter(email=self.request.user.email)
        budget = user_query[0].Budget
        user_data = []
        user_data.append(user_query[0].graduation_CGPA)
        user_data.append(user_query[0].work_experience)
        user_data.append(user_query[0].toefl)
        preferred_location = user_query[0].preferred_country
        df = pd.read_csv('student.csv')
        X_train = df.iloc[:, [4, 5, 6]]
        y_train = df.iloc[:, -1]
        data = [user_data]
        data = np.array(data)
        svm_model_linear = SVC(kernel='linear', C=1).fit(X_train, y_train)
        svm_predictions = svm_model_linear.predict(data)
        grade = svm_predictions.reshape(1, 1)[0]
        student_grade = grade[0]

        # result = (university_df[university_df.Grade == grade]).sort_values(by = 'Overall Rating', ascending = False)
        queryset = queryset.filter(grade=student_grade)
        queryset = queryset.filter(fees_in_lakhs__lte=budget + 4)
        queryset = queryset.order_by('-overall_rating')
        if preferred_location != 'all':
            queryset = queryset.filter(country=preferred_location)
        return queryset
