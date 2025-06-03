from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from notes.serializers import NoteSerializer
from .models import Note
from django.urls import path
from . import views


class NoteList(APIView):
    def post(self, request):
        note = NoteSerializer(
            data=request.data, context={"request": request}
        )  # Pass request context
        if note.is_valid(raise_exception=True):
            note.save()
            return Response(note.data, status=status.HTTP_201_CREATED)

        return Response(note.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(
            notes, many=True, context={"request": request}
        )  # Pass request context
        return Response({"notes": serializer.data}, status=status.HTTP_200_OK)


class NoteDetail(APIView):
    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)
