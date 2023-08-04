import io

from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response

from foodgram.settings import (FONT_COLOR, FOOT_FONT, FOOT_RIGHT, FOOT_UP,
                               HEAD_FONT, HEAD_RIGHT, HEAD_UP, HEIGHT_CROP,
                               HEIGHT_MAIN, MAIN_FONT, MAIN_RIGHT, POS_ONE,
                               POS_TWO, POS_ZERO)


def post(request, pk, get_object, models, serializer):
    """Post."""

    obj = get_object_or_404(get_object, id=pk)
    if models.objects.filter(
        recipe=obj, user=request.user
    ).exists():
        return Response(
            {'message':
                f'You have already added {obj}.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = serializer(
        obj, context={request: 'request'}
    )
    models.objects.create(
        recipe=obj, user=request.user
    )
    return serializer.data


def delete(request, pk, get_object, models):
    """Delete."""

    obj = get_object_or_404(get_object, id=pk)
    if not models.objects.filter(
        recipe=obj, user=request.user
    ).exists():
        return Response(
            {'message':
                f'You have not added recipe {obj}.'}
        )
    models.objects.filter(
        recipe=obj, user=request.user
    ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def make_shopping_cart(ingredients):
    """Make shopping cart."""

    grocery_list = {}
    download = io.BytesIO()
    pdfmetrics.registerFont(
        TTFont('verdana', 'fonts/Verdana.ttf', 'UTF-8'))
    for ingredient in ingredients:
        if ingredient[POS_ZERO] not in grocery_list:
            grocery_list[ingredient[POS_ZERO]] = {
                'measurement_unit': ingredient[POS_ONE],
                'amount': ingredient[POS_TWO]
            }
        else:
            grocery_list[ingredient[POS_ZERO]]['amount'] += ingredient[POS_TWO]
    report = canvas.Canvas(download)
    report.setFont('verdana', HEAD_FONT)
    report.drawString(HEAD_RIGHT, HEAD_UP, 'My grocery list:')
    height = HEIGHT_MAIN
    report.setFont('verdana', MAIN_FONT)
    for i, (name, data) in enumerate(grocery_list.items(), POS_ONE):
        report.drawString(MAIN_RIGHT, height, (f'{i}. {name.capitalize()} - '
                                               f'{data["amount"]} '
                                               f'{data["measurement_unit"]}'))
        height -= HEIGHT_CROP
    report.setFont('verdana', FOOT_FONT)
    report.setFillColorRGB(FONT_COLOR, FONT_COLOR, FONT_COLOR)
    report.drawCentredString(
        FOOT_RIGHT, FOOT_UP, 'Foodgram grocery assistant.'
    )
    report.showPage()
    report.save()
    download.seek(POS_ZERO)
    return download
