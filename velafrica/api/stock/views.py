from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from velafrica.stock.models import StockTransfer

@api_view(['POST'])
def book(request, pk):
    """
    Book a stock transfer.
    """
    if request.method == 'POST':
        try:
            stocktransfer = StockTransfer.objects.get(pk=pk)
        except StockTransfer.DoesNotExist:
            return Response({"error": "No Stock Transfer found with id {}".format(pk)}, status=status.HTTP_404_NOT_FOUND)

        if stocktransfer.booked:
            return Response({"error": "This Stock Transfer has already been booked"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            stocktransfer.book()

        return Response({"success": "Stock Transfer has been booked"}, status=status.HTTP_201_CREATED)