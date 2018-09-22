class CheckForToeflListView(LoginRequiredMixin, ListView):
    model = University
    template_name = "msguide/check_with_toefl.html"
    paginated_by = 5

    def get_queryset(self):
        queryset = super(CheckForGreListView, self).get_queryset()
        user_query = UserProfile.objects.filter(email=self.request.user.email)
        budget = user_query[0].Budget
        user_data = []
        user_data.append(user_query[0].graduation_CGPA)
        user_data.append(user_query[0].work_experience)
        user_data.append(user_query[0].toefl)
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
