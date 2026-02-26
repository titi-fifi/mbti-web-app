from flask import Flask, render_template, request
from questions import questions

app = Flask(__name__)

# 首页
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions_with_index = [{"index": i, **q} for i, q in enumerate(questions)]

    if request.method == "POST":
        answers = {f"q{i}": request.form.get(f"q{i}") for i in range(len(questions))}
        mbti_result = calculate_mbti(answers)
        return render_template("result.html", mbti=mbti_result)

    return render_template("quiz.html", questions=questions_with_index)

# 计算 MBTI 类型（简单统计）
def calculate_mbti(answers):
    # 统计每个维度的选择
    # E/I, S/N, T/F, J/P
    dimensions = {"E":0,"I":0,"S":0,"N":0,"T":0,"F":0,"J":0,"P":0}
    for val in answers.values():
        if val:
            dimensions[val] += 1
    # 构建最终类型
    mbti = ""
    mbti += "E" if dimensions["E"] >= dimensions["I"] else "I"
    mbti += "S" if dimensions["S"] >= dimensions["N"] else "N"
    mbti += "T" if dimensions["T"] >= dimensions["F"] else "F"
    mbti += "J" if dimensions["J"] >= dimensions["P"] else "P"
    return mbti

if __name__ == "__main__":
    app.run(debug=True)