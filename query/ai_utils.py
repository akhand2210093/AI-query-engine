import ollama

def clean_sql(text: str) -> str:
    return text.replace("```sql", "").replace("```", "").strip()

def generate_sql(query: str) -> str:
    prompt = (
        "Convert the following natural language query into ONLY a valid SQLite SQL query.\n"
        "Table name: query_salesdata\n"
        "Columns: id, month, revenue\n"
        "Rules:\n"
        "- SELECT queries only\n"
        "- MUST include the `id` column in SELECT\n"
        "- No DELETE, UPDATE, DROP, INSERT\n"
        "- No explanation, return only SQL\n\n"
        f"{query}"
    )

    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return clean_sql(response["message"]["content"])
