from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'credentials.json')
print(SERVICE_ACCOUNT_FILE)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


SAMPLE_SPREADSHEET_ID = '1XksmEkGLbsrMluREMBXlRJOzCY6A7zjF7DEtr3Va21s'
attendance = '1qOkoQP_f_ATpbO7jDTxKpouUbCSuUXN-K-1Yn7OuL88'

service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()



def create():
    result = sheet.values().get(spreadsheetId=attendance, range="Sheet1!AB8").execute()
    values = result.get('values', [])
    index_val = int(values[0][0])
    index_val += 1
    return index_val


def sheet_function(data_list, index_val):
    request = sheet.values().update(
        spreadsheetId=attendance, range="Sheet1!AB8", valueInputOption="USER_ENTERED", body={"values": [[index_val]]}).execute()

    request = sheet.values().update(
        spreadsheetId=attendance, range=f"Sheet1!A{index_val}", valueInputOption="USER_ENTERED", body={"values": data_list}).execute()


def email_list():
    result = sheet.values().get(spreadsheetId=attendance, range="Sheet1!A16:Q500").execute()
    values = result.get('values', [])
    ids = []

    for each in values:
        ids.append(each[15])

    return ids


def get_row_by_phone(phone_number):
    result = sheet.values().get(spreadsheetId=attendance, range="CSE").execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

  
    phone_column = 5
    for row in values:
        # print(row)
        if row[phone_column] == phone_number:
            return [row,values.index(row)+1]
            
    # request = sheet.values().update(
    #     spreadsheetId=attendance, range="C!A1", valueInputOption="USER_ENTERED", body={"values": [[10]]}).execute()
    print('Phone number not found.')
    return None


def get_row_by_id(target_id):
    result = sheet.values().get(spreadsheetId=attendance, range="CSE").execute()
    values = result.get('values', [])

    if not values:
        print("No ID found in the sheet.")
        return None

    id_column = 12  # Assuming IDs are in column L (index 11).

    if len(values[0]) <= id_column:
        print(f"Invalid id_column: {id_column}. The sheet might not have enough columns.")
        return None

    for row in values:
        if len(row) > id_column and row[id_column] == target_id:
            return row

    print(f"ID '{target_id}' not found.")
    return None

# Example usage:
# target_id_to_search = "4"  # Replace this with the ID you want to search for.
# row_data = get_row_by_id(target_id_to_search)
# if row_data:
#     print('Row data:', row_data)

# Example usage:
# phone_number_to_search = '7845866973'
# row_data = get_row_by_phone(phone_number_to_search)
# if row_data:
#     print('Row data:', row_data)