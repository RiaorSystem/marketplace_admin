from django.urls import path
from .views import CreateAdvertisementView, ApproveAdvertisementView, DepositToEscrowView, SellerAdsView, AdApplicantsView, ApplyForAdvertisementView, SubmitAdvertisementStatsView, ApproveAdvertisementApplicationView

urlpatterns = [
    path('ads/create/', CreateAdvertisementView.as_view(), name='create_ad'),
    path('ads/<int:ad_id>/approve/', ApproveAdvertisementView.as_view(), name='approve_ad'),
    path('deposit/', DepositToEscrowView.as_view(), name='deposit_escrow'),
    path('ads/my_ads/', SellerAdsView.as_view(), name='seller_ads'),
    path('ads/<int:ad_id>/applicants/', AdApplicantsView.as_view(), name='ad_applicants'),
    path('ads/<int:ad_id>/apply/', ApplyForAdvertisementView.as_view(), name='apply_ad'),
    path('ads/<int:application_id>/submit-stats/', SubmitAdvertisementStatsView.as_view(), name='submit_stats'),
    path('ads/<int:application_id>/approve/', ApproveAdvertisementApplicationView.as_view(), name='approve_ad'),
]
