from django.urls import path, include
from .views import ProductViewset, AddToCartViewset, VendorViewset, BillViewSet, OrderViewSet, UpdateCart, loginPage, register, home, logoutUser, userPage

urlpatterns = [
    path('products', ProductViewset.as_view()),
    path('updatecart', UpdateCart.as_view()),
    path('carts', AddToCartViewset.as_view()),
    path('vendors', VendorViewset.as_view()),
    path('order', OrderViewSet.as_view()),
    path('login/', loginPage, name = "loginpage"),
    path('register', register, name="register"),
    path('home', home, name = "home"),
    path('bill', BillViewSet.as_view()),
    path('logout/', logoutUser, name='logout'),
    path('user/', userPage, name='user')
    # path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    # path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
    # path('account/', include('django.contrib.auth.urls')),#, name = "login"),
    # path('signup/', signup, name = "signup"),
    # path('account/', include('django.contrib.auth.urls')),
]