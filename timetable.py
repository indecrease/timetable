from flask import Flask, jsonify, request
import pandas as pd
import json, sys
timetable = Flask(__name__)


df = pd.read_excel("timetable.xlsx")
@timetable.route("/timetable", methods=["POST"])
def time():
    rqdata = json.loads(request.get_data(), encoding= "utf-8")
    params = rqdata["action"]['params']
    grade = params.get('grade')
    clazz = params.get('class')
    week = params.get('day')
    output = df[(df["학년"] == int(grade)) & (df["반"] == int(clazz)) & (df["요일"] == week)]
    if output.empty:
        output = f"{grade}학년 {clazz}반 학생의 {week}요일의 시간표가 없습니다."
    else:
        row = output.iloc[0]
        for i in range(1, 8):
            if f"{i}교시" in row:
                subject = row[f"{i}교시"] 
            for i, subj in enumerate(subject):
                text = f"{grade}학년 {clazz}반 {week}요일 시간표입니다. \n"
                text += "\n".join(f"{i+1}교시 :{subj}")
        
    response = {"version": "2.0", "template": {
                   "outputs": [
                       {
                           "simpleText": {
                               "text": text
                           }
                       }
                   ]
               }}
    return jsonify(response)


if __name__ == "__main__":
    timetable.run(host="0.0.0.0", port=int(sys.argv[1]), debug=True)