from fastapi import FastAPI
import engine  # our matching code

app = FastAPI()

@app.get("/match/{student_id}")
def match(student_id: int):
    try:
        result = engine.recommend_internship(student_id)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
