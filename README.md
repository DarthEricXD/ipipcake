# ipipcake - Cake is not a LIE!

ipipcake is an IP location query application built with Python. It fetches your public IP address and geographical information (country, region, city, and coordinates) and logs the results to a Google Sheet. 

<p align="center">
  <img src="https://github.com/DarthEricXD/ipipcake/blob/main/media/Cake.png" alt="image" width="80">
</p>

Please note: IP addresses may be considered personal data under privacy laws. Do not use ipipcake for any illegal or unethical purposes.


## APIs Used
The application relies on the following external APIs:

- **ipify**: Retrieves the user's public IP address in JSON format. 
- **ip-api**: Provides geolocation data based on the IP address.

Both APIs are free for non-commercial use.


## Google Sheets Integration for IP Logging

Follow these steps to log IP and location data to a Google Sheet.

### 1. Create a Google Sheet

- Open [Google Sheets](https://sheets.google.com)
- Create a new spreadsheet
- In the first row, add the following headers:

<pre> Timestamp | IP | Country | Region | City | Coordinates </pre>

### 2. Open Apps Script Editor

- In the spreadsheet, click: `Extensions → Apps Script`
- Replace any existing code with the following:

```javascript
function Post(e) {
  Logger.log(e.postData.contents);
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = JSON.parse(e.postData.contents);

  sheet.appendRow([
    new Date(),
    data.ip,
    data.country,
    data.region,
    data.city,
    data.coordinates
  ]);

  return ContentService.createTextOutput("Success");
}

```

### 3. Deploy as a Web App

- Click `Deploy → New Deployment`
- Under **Select type**, choose **Web app**
- Configure the settings:
   - **Execute as**: `Me`
   - **Who has access**: `Anyone`
- Click **Deploy**
- Authorize and copy the **Web App URL**
- In the `query_ip_location()` function of your Python script, replace the `webhook_url` variable with the copied URL:

```python
webhook_url = "https://script.google.com/macros/s/.../exec"
```

<p align="center">
  <img src="https://github.com/DarthEricXD/ipipcake/blob/main/media/example1.png" alt="image" width="500">
</p>


Please note: If you see a "Bad Request Error 400" when opening **Extensions**, it may be caused by multiple Google accounts logged in simultaneously. To fix this, please log out of extra accounts or open the browser in incognito mode.

## Build Executable

You can use PyInstaller to generate an `.exe` file. Run this command in the terminal:

```bash
pyinstaller --noconsole --onefile --icon=media\cake.ico --add-data "media\cake.png;media" --add-data "media\click_sound.wav;media" ipipcake.py

