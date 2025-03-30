from django.shortcuts import render

# Create your views here.
import openai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SalesData

openai.api_key = settings.OPENAI_API_KEY

class QueryAPIView(APIView):
    def post(self, request):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert natural language to SQL using OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Convert natural language queries into SQL queries for an SQLite database."},
                    {"role": "user", "content": user_query}
                ]
            )
            sql_query = response["choices"][0]["message"]["content"]
        except Exception as e:
            return Response({"error": f"AI processing error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Execute query
        try:
            result = SalesData.objects.raw(sql_query)
            data = [{"month": row.month, "revenue": row.revenue} for row in result]
            return Response({"query": sql_query, "result": data})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ExplainAPIView(APIView):
    def post(self, request):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Explain how this natural language query is converted into SQL."},
                    {"role": "user", "content": user_query}
                ]
            )
            explanation = response["choices"][0]["message"]["content"]
            return Response({"query": user_query, "explanation": explanation})
        except Exception as e:
            return Response({"error": f"AI processing error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ValidateAPIView(APIView):
    def post(self, request):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Convert natural language queries into SQL queries for an SQLite database."},
                    {"role": "user", "content": user_query}
                ]
            )
            sql_query = response["choices"][0]["message"]["content"]
            
            # Check if query is valid
            try:
                SalesData.objects.raw(f"EXPLAIN {sql_query}")
                return Response({"query": user_query, "status": "Valid"})
            except Exception:
                return Response({"query": user_query, "status": "Invalid"})
        except Exception as e:
            return Response({"error": f"AI processing error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
