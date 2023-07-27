from flask import Flask, render_template, Response, request,session
import pandas as pd
from new_app import get_row_by_phone,get_row_by_id
from jinja2 import Template
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os   


app = Flask(__name__)
SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'api/credentials.json')
print(SERVICE_ACCOUNT_FILE)


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


SAMPLE_SPREADSHEET_ID = '1XksmEkGLbsrMluREMBXlRJOzCY6A7zjF7DEtr3Va21s'
attendance = '1qOkoQP_f_ATpbO7jDTxKpouUbCSuUXN-K-1Yn7OuL88'

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()
app.secret_key = "abc"


@app.route("/")
def home_route():
    return "hello"

@app.route('/get_number/<qr_id>')
def index(qr_id):
    session["qrcode"]=qr_id
    print(session["qrcode"])
    return render_template('mobile.html')

@app.route('/submit_mobile', methods=['POST'])
def submit_mobile():

    result = sheet.values().get(spreadsheetId=attendance, range="CSE").execute()
    values = result.get('values', [])

    mobile_number = request.form['mobile']
    row=get_row_by_phone(str(mobile_number))[0]
    idx=get_row_by_phone(str(mobile_number))[1]
    if(row):
        # row[12]=session["qrcode"]
        # request = sheet.values().update(
        # spreadsheetId=attendance, range="CSE!M{}".format(idx), valueInputOption="USER_ENTERED", body={"values": [[session["qrcode"]]]}).execute()
        print(row)
    
    # print("Mobile Number:", mobile_number)
    # print(session["qrcode"])
    session["mobile"] = mobile_number
    # df1 = df[df['Contact'] == mobile_number]
    # if not df1.empty:
    #     print("Number found. Details:")
    #     # print(df1)
    #     index = df1.index[0]
    #     df1["Id"]=session["qrcode"]
    #     df.loc[index, 'Id'] = session["qrcode"]
    #     df.to_csv("data.csv", index=False)
    request1 = sheet.values().update(
    spreadsheetId=attendance, range="CSE!M{}".format(idx), valueInputOption="USER_ENTERED", body={"values": [[session["qrcode"]]]}).execute()
        # df1["Id"]=session["qrcode"]
    # else:
    #     print("Number not found in the DataFrame.")

    # return render_template("details.html", df1=df1.to_html())
    return "successfully encoded"


@app.route('/home1')
def home():
    return "reg done"

@app.route('/check')
def check_qr():
    return render_template('check.html')

@app.route('/fetch_data')

def fetch_user_data():
    id = int(session["qrcode"])
    result = sheet.values().get(spreadsheetId=attendance, range="CSE").execute()
    values = result.get('values', [])

    rows=get_row_by_id(str(id))
    if(rows):
        print(rows)

    data_frame = pd.DataFrame([rows], columns=["Name", "Degree","Year","College","Mail","Contact","Food","Gender","Department","Id-Card","Time","Event","Id" ])
    template_string = """
<!DOCTYPE html>
<html>
<head>
    <title>Row Data</title>
</head>
<body>
    <h1>Row Data from Google Sheets</h1>
    {{ data_frame.to_html() | safe }}
</body>
</html>
"""

# Create a Jinja template object.
    template = Template(template_string)

# Render the template with the DataFrame.
    return template.render(data_frame=data_frame)
    # data=get_id_sheet(str(id))
    # print(data)
    # df=pd.read_csv("data.csv")
    
    # print(id)
    # df1 = df[df['Id'] == id]
    # if not df1.empty:
    #     print("Number found. Details:")
    #     # print(df1)

    # else:
    #     print("Number not found in the DataFrame.")

    # return render_template("final.html", df1=df1.to_html())



# @app.route('/register',methods=['POST'])
# def register():
#     data=request.get_json()
#     print(data)

@app.route('/qr_scan')
def qr_scan():
    # return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('scanner.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
