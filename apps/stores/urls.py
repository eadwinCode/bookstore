from django.urls import path

from apps.stores.views import CreateStoreView, DeleteStoreView, UpdateStoreView, ListStoreBooksView, AddStoreBooksView, \
    BorrowStoreBooksView, ReturnStoreBooksView, RetrieveStoreView, ListStoresView, StoryBookSubscribeView, \
    StoryBookUnSubscribeView, StoryBookSubscribersListView

app_name = 'store'

urlpatterns = [
    path('create/', CreateStoreView.as_view(), name='create'),
    path('<uuid:id>/detail/', RetrieveStoreView.as_view(), name='detail'),
    path('<uuid:id>/update/', UpdateStoreView.as_view(), name='update'),
    path('<uuid:id>/delete/', DeleteStoreView.as_view(), name='destroy'),
    path('<uuid:id>/books/', ListStoreBooksView.as_view(), name='books'),
    path('list/', ListStoresView.as_view(), name='list'),
    path('<uuid:store_id>/book/create/', AddStoreBooksView.as_view(), name='book-create'),
    path(
        '<uuid:store_id>/book/<uuid:book_id>/borrow/<int:user_id>/', BorrowStoreBooksView.as_view(),
        name='book-borrow'
    ),
    path('<uuid:store_id>/book/<uuid:book_id>/return', ReturnStoreBooksView.as_view(), name='book-return'),
]

# store_book subscription route
urlpatterns += [
    path('<uuid:store_book_id>/<int:user_id>/subscriber', StoryBookSubscribeView.as_view(), name='subscribe'),
    path('<uuid:store_book_subscription_id>/unsubscriber', StoryBookUnSubscribeView.as_view(), name='unsubscribe'),
    path('<uuid:store_id>/subscribers', StoryBookSubscribersListView.as_view(), name='unsubscribe'),
]
