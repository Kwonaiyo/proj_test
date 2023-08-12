from flask import Flask, render_template, request, jsonify,json
import package.pkg_scale as pb


app = Flask(__name__)

# 메인 홈 화면
@app.route("/", methods=['GET', 'POST'])
def start():
    rows = pb.get_itemcode()  # 콤보박스에 컬럼들을 채움
    whcode_rows = pb.get_whcode()
    if request.method == 'POST': # html에서 조회 버튼을 클릭했을 때 
        selected_option = request.form.get('selected_option') # 선택된 option의 value를 가져옴
        current = pb.get_current(selected_option)
        value1,value2,value3,value4 = current[0]
        try:
            value2 = int(value2)
        except:
            pass
        try:
            value3 = int(value3)
        except:
            pass
        try:
            value4 = int(value4)
        except:
            pass
        return render_template("auto_scale.html", whcode = whcode_rows, items = rows, itemcode1=value1,itemcode2=value2,itemcode3=value3,itemcode4=value4)
    return render_template("auto_scale.html", whcode = whcode_rows, items = rows) 

# 현재 개수 몇 개 있는지 확인
@app.route("/fetch_data_check")
def check_button():
    input_data = request.args.get('input')
    string = pb.enroll_check(input_data)
    try:
        message1 = int(string[0][0])
    except:
        message1 = 0
    try:
        message2 = int(string[1][0])
    except:
        message2 = 0
    return jsonify({'message1':message1, 'message2':message2})

# 발주 버튼 클릭
@app.route("/fetch_data_enroll2")
def manual_button():
    input_data = request.args.get('input')
    input_Qty = request.args.get('inputQty')
    if(int(input_Qty) <= 0 or input_Qty == ""):
        return jsonify({'message':'적어도 한 개 이상은 보냅시다;;'})
    string = pb.autu_enroll(input_data, input_Qty)
    return jsonify({'message':f'{string}'})



if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)