from flask import Flask, render_template, request, jsonify,json
import package.pkg_scale as pb


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def start():
    rows = pb.get_itemcode()
    # search_attempted = False  # 검색 시도를 기본값으로 False 설정

    if request.method == 'POST':
        # search_attempted = True  # 검색을 시도했을 때 True로 변경
        selected_option = request.form.get('selected_option')
        current = pb.get_current(selected_option)
        value1,value2,value3,value4 = current[0]
        
        return render_template("auto_scale.html", items = rows, itemcode1=value1,itemcode2=value2,itemcode3=value3,itemcode4=value4) 
    return render_template("auto_scale.html", items = rows) 

@app.route("/fetch_data")
def autu_button():
    input_data = request.args.get('input')
    pb.autu_enroll(input_data)
    return jsonify({'message': f'this point2'})
    # return render_template("screen2.html", items = rows) 



if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)