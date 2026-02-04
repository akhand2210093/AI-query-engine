from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SalesData
from .ai_utils import generate_sql
from django.db import connection

class QueryAPIView(APIView):
    def post(self, request):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response({"error": "Query is required"}, status=400)

        try:
            sql_query = generate_sql(user_query)
        except Exception as e:
            return Response({"error": f"AI error: {str(e)}"}, status=500)

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()

            data = [dict(zip(columns, row)) for row in rows]

            return Response({
                "query": sql_query,
                "result": data
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)


import ollama

class ExplainAPIView(APIView):
    def post(self, request):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response(
                {"error": "Query is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prompt = (
                "Explain how the following natural language query would be "
                "converted into an SQLite SQL query. Do not write SQL.\n\n"
                f"{user_query}"
            )

            response = ollama.chat(
                model="phi3:mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            explanation = response["message"]["content"].strip()

            return Response({
                "query": user_query,
                "explanation": explanation
            })

        except Exception as e:
            return Response(
                {"error": f"AI error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ValidateAPIView(APIView):
    def post(self, request):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response({"error": "Query is required"}, status=400)

        try:
            sql_query = generate_sql(user_query)
        except Exception as e:
            return Response({"error": f"AI error: {str(e)}"}, status=500)

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"EXPLAIN {sql_query}")
            return Response({"query": user_query, "status": "Valid"})
        except Exception:
            return Response({"query": user_query, "status": "Invalid"})
