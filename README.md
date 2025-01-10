# SMS API Usage Documentation


## EX: Functions and Details
#### Building for source

Code Example:

```sh
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

public class SendSmsDataRequest
{
    private const string USE_RETURN_API = "1";
    private const string SMS_SENDER_NAME = "MIRUKURU";

    public Dictionary<string, string> Parameter { get; private set; }
    public string MobileNum { get; private set; }
    public string SmsText { get; private set; }
    public string SmsId { get; private set; } 
    public string MemberNum { get; private set; }
    public int UserNum { get; private set; }

    /// <summary>
    /// Constructor for sending SMS
    /// </summary>
    public SendSmsDataRequest(string mobileNum, string smsText, string smsId)
    {
        Parameter = new Dictionary<string, string>
        {
            { "mobilenumber", mobileNum },
            { "smstitle", SMS_SENDER_NAME },
            { "smstext", smsText },
            { "status", USE_RETURN_API },
            { "smsid", smsId }
        };      
    }

    /// <summary>
    /// Constructor for retrieving delivery result
    /// </summary>
    public SendSmsDataRequest(string smsId)
    {
        SmsId = smsId;

        Parameter = new Dictionary<string, string>
        {
            { "smsid", smsId }
        };
    }

    /// <summary>
    /// Function to send SMS
    /// </summary>
    public async Task<string> SendSms(string apiUrl, string username, string password)
    {
        using (var client = new HttpClient())
        {
            var credentials = Convert.ToBase64String(Encoding.ASCII.GetBytes($"{username}:{password}"));
            client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", credentials);

            var content = new FormUrlEncodedContent(Parameter);

            var response = await client.PostAsync(apiUrl, content);

            if (response.IsSuccessStatusCode)
            {
                var resultContent = await response.Content.ReadAsStringAsync();
                return resultContent; // Return the result content
            }
            else
            {
                throw new Exception($"Error sending SMS: {response.StatusCode}");
            }
        }
    }

    /// <summary>
    /// Function to get SMS sending result
    /// </summary>
    public async Task<string> GetSmsDataResult(string apiUrl, string username, string password)
    {
        using (var client = new HttpClient())
        {
            var credentials = Convert.ToBase64String(Encoding.ASCII.GetBytes($"{username}:{password}"));
            client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", credentials);

            var content = new StringContent(
                $"smsid={SmsId}", 
                Encoding.UTF8, 
                "application/x-www-form-urlencoded");

            var response = await client.PostAsync(apiUrl, content);

            if (response.IsSuccessStatusCode)
            {
                var resultContent = await response.Content.ReadAsStringAsync();
                return resultContent; // Return the result content
            }
            else
            {
                throw new Exception($"Error getting SMS result: {response.StatusCode}");
            }
        }
    }

    
}

```
# Usage Instructions:
## Document : Information in the document about sending parameters and returning results from pages 11-28
![image](https://github.com/user-attachments/assets/09092f40-462b-48d0-81e5-72f9090fd962)
![image](https://github.com/user-attachments/assets/818451cb-6e83-463b-a394-4a288d41a90b)
![image](https://github.com/user-attachments/assets/b7733019-5040-4543-99ec-4d4ed34ce838)


### Function SendSms:
```sh
var sendSmsRequest = new SendSmsDataRequest("0399679155", "Sample SMS content", "unique_sms_id", "123", 1);
string apiUrl = "https://www.sms-console.jp/api/?";
string username = "your_username";
string password = "your_password";

var resultContent = await sendSmsRequest.SendSms(apiUrl, username, password);
Console.WriteLine(resultContent);

```
Results when returned MS Sending Result

- Status: success
- Message: SMS sent successfully
- SMS ID: unique_sms_id
- Recipient: 09012345678
- Sent At: 2025-01-10T10:30:00Z
- Delivery Status: delivered
- Delivery Time: 2025-01-10T10:45:00Z
- Message Content: Sample SMS content
### Document : Information in the document about sending parameters and returning results from pages 62-65
![image](https://github.com/user-attachments/assets/1d1c4437-7c96-447d-a934-7cdd02f42398)
![image](https://github.com/user-attachments/assets/cd8fa806-3b9d-46d0-bc22-543790f9e3aa)
### Function GetSms

```sh
string apiUrl = "https://www.sms-console.jp/api5/?";
string username = "your_username";
string password = "your_password";


var sendSmsRequest = new SendSmsDataRequest("unique_sms_id");
var resultContent = await sendSmsRequest.GetSmsDataResult(apiUrl, username, password);
Console.WriteLine(resultContent);

```
