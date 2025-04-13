from google.oauth2 import service_account
from googleapiclient.discovery import build

class MyGsheet:
    def __init__(self, folderID=None, spreadsheet_id=None, cred=None):
        self.folderId = folderID
        self.service = None
        self.spreadsheet_id = spreadsheet_id
        self.cred = cred

    
    def initialize_service(self):
        credentials = service_account.Credentials.from_service_account_info(self.cred)
        try:
            service = build("sheets", "v4", credentials=credentials)
        except:
            print("Error while creating sheets service")
            return None
        if service:
            self.service = service
            print("Service created successfully")
            return None
 
    def clear_sheet(self, spreadsheet_id=None, sheet_range=None):
        if not spreadsheet_id:
            if self.spreadsheet_id:
                print("Working on spreadsheet default")
                spreadsheet_id_ = self.spreadsheet_id
            else:
                print("Please inform spreadsheet_id")
                return None
        else:
            spreadsheet_id_ = spreadsheet_id
        

        if self.service:
            sheet_range_ = sheet_range
            sheet = self.service.spreadsheets()
            sheet.values().clear(spreadsheetId=spreadsheet_id_, range=sheet_range_).execute()
            print("Range cleaned")
            return None
        else:
            print("Please initialize service first")
            return None

    def update_sheet(self, spreadsheet_id=None, title=None, sheet_range=None, new_data=None, clear=False):
        
        if not spreadsheet_id:
            print("Please inform spreadsheetId")
            return None
        if self.service:
            #sheet_range_ = "copy_buddies_history!A2:Z"
            sheet_range_ = sheet_range
            sheet = self.service.spreadsheets()
            values = [row.to_list() for idx, row in new_data.iterrows()]

            body = {"values": values}
            if clear:
                self.clear_sheet(spreadsheet_id=spreadsheet_id, sheet_range=sheet_range_)
            #st.write(new_data)
            sheet.values().update(spreadsheetId=spreadsheet_id, 
                                range=sheet_range, 
                                valueInputOption="USER_ENTERED",
                                body=body).execute()
            print("Sheet updated with new values")
            return None
        else:
            print("Please initialize service first")
            return None

    def create_new_sheet(self, spreadsheet_id=None, sheet_name=None):
        create = True
        if sheet_name in self.get_all_sheets(spreadsheet_id):
            create = False
            print(f"Sheet already exist with the name {sheet_name}")
            return None
        
        if (self.service and create):
            request_body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': f"{sheet_name}"
                        }
                    }
                }]
            }
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id
                ,body=request_body).execute()
            
            print(f"{sheet_name} created")

    def get_all_sheets(self, spreadsheet_id=None):
        # Call the Sheets API
        if not spreadsheet_id:
            print("Please inform spreadsheet_id")
            return None
        else:
            if not self.service:
                print("Please initialize service first")
                return None
            else:
                print("checking if sheet already exists...")
                sheet_metadata = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
                # Extract sheet names
                sheet_names = [sheet['properties']['title'] for sheet in sheet_metadata['sheets']]
                return sheet_names
            






