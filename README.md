# SMS API Usage Documentation


## EX: Sample code using Functions and Details
#### Building for source code Example:

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
## 1. SendApiEndpoint
### Document : Information in the document about sending parameters and returning results from pages 11-28
![image](https://github.com/user-attachments/assets/09092f40-462b-48d0-81e5-72f9090fd962)
![image](https://github.com/user-attachments/assets/818451cb-6e83-463b-a394-4a288d41a90b)
![image](https://github.com/user-attachments/assets/b7733019-5040-4543-99ec-4d4ed34ce838)


### Function SendSms :
```sh
var sendSmsRequest = new SendSmsDataRequest("0399679155", "Sample SMS content", 1);
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
  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___
## 2. GetResultApiEndpoint
### Document: Information in the document about sending parameters and returning results from pages 62-65
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
  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___
# MIRUKURUSTORE The changes for this version.
## The current version of the old code 
```sh
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web;

namespace MirukuruStore.ViewModels.Request
{
    /// <summary> 
    /// SMS送信APIパラメータクラス 
    /// Send SMS API Parameter Class
    /// </summary> 
    public class SendSmsDataRequest
    {
        /// <summary>
        /// SMS送達結果通知API利用フラグ
        /// 通知を受け取る必要があるため１固定
        /// 受け取らない場合は０
        /// 
        /// 
        /// SMS delivery results notification API usage flag
        /// 1 if notification is necessary, 0 if not
        /// 
        /// </summary>
        private const string USE_RETURN_API = "1";

        /// <summary>
        /// APIの利用範囲
        /// SMS送信のみのため1固定
        /// IVR認証を行う場合は２，４を使用する
        /// 
        /// API Usage Scope
        /// + Use 1 for SMS sending only
        /// + Use 2,4 for IVR Authentication
        /// 
        ///</summary>
        private const string USE_SMS_ONLY = "1";

        /// <summary>
        /// IVR認証 ２，４を使用する
        /// 
        /// Use 2,4 for IVR Authentication
        /// </summary>
        private const string USE_IVR = "2";

        /// <summary>
        /// 送信元表示名 (Sender's display name)
        ///
        /// APIのパラメータでは必須となっているが国際網から配信時以外は無視されるとの表記
        /// Notation that it is mandatory in the API parameters but is ignored except when distributed from the international network
        /// 
        /// （仕様書_MediaSMSAPI_20150605.pdf）
        /// </summary>
        private const string SMS_SENDER_NAME = "MIRUKURU";

        /// <summary>
        /// SMS送信時のリクエストパラメータ (Request parameters when sending SMS)
        ///</summary>
        public Dictionary<string, string> Parameter { get; set; }

        public string? MobileNum { get; set; }

        public string SmsTitle { get; set; } = SMS_SENDER_NAME;

        public string? SmsText { get; set; }

        public string? SmsText2 { get; set; }

        public string Status { get; set; } = USE_RETURN_API;

        public string SmsId { get; set; }

        public string Method { get; set; } = USE_SMS_ONLY;

        public string? MemberNum { get; set; }

        public int? UserNum { get; set; }

        /// <summary>
        /// コンストラクタ
        /// </summary>
        /// <param name="mobileNum">送信先電話番号</param>
        /// <param name="smsText">本文</param>
        /// <param name="smsText2">本文（au）</param>
        /// <param name="smsId">SMS送達結果通知取得用ID</param>
        /// <param name="memberNum">会員番号（DB書込に使用）</param>
        /// <param name="userNum">顧客番号（DB書込に使用）</param>
        public SendSmsDataRequest(string mobileNum, string smsText, string smsText2, string smsId, string memberNum, int userNum)
        {
            Parameter = new Dictionary<string, string>
            {
                { "mobilenumber", mobileNum },
                { "smstitle", SMS_SENDER_NAME },
                { "smstext", smsText },
                { "smstext2", smsText2 },
                { "status", USE_RETURN_API },
                { "smsid", smsId },
                { "method", USE_SMS_ONLY }
            };

            MobileNum = mobileNum;
            SmsText = smsText;
            SmsText2 = smsText2;
            SmsId = smsId;
            MemberNum = memberNum;
            UserNum = userNum;
        }

        /// <summary>
        /// コンストラクタ(送達結果再取得時用)
        ///</summary>
        /// <param name="smsId">SMS送達結果通知取得用ID</param>
        public SendSmsDataRequest(string smsId)
        {
            SmsId = smsId;

            Parameter = new Dictionary<string, string>
            {
                { "smstitle", SMS_SENDER_NAME },
                { "smsid", smsId },
                { "status", USE_RETURN_API },
                { "method", USE_IVR }
            };
        }

        /// <summary>
        /// パラメータからPOST文字列を生成する
        ///</summary>
        /// <returns>POST文字列</returns>
        public string GetHttpQuery()
        {
           .....
        }
    }
}

```
## Changes will be made to the new code
  ```sh
 /// <summary>
 /// コンストラクタ
 /// </summary>
 /// <param name="mobileNum">送信先電話番号</param>
 /// <param name="smsText">本文</param>
 /// <param name="smsId">SMS送達結果通知取得用ID</param>
 /// <param name="memberNum">会員番号（DB書込に使用）</param>
 /// <param name="userNum">顧客番号（DB書込に使用）</param>
 public SendSmsDataRequest(string mobileNum, string smsText, string smsId, string memberNum, int userNum)
 {
     Parameter = new Dictionary<string, string>
     {
         { "mobilenumber", mobileNum },
         { "smstitle", SMS_SENDER_NAME },
         { "smstext", smsText },              
         { "status", USE_RETURN_API },
         { "smsid", smsId },                
     };

     MobileNum = mobileNum;
     SmsText = smsText;         
     SmsId = smsId;
     MemberNum = memberNum;
     UserNum = userNum;
 }

 /// <summary>
 /// コンストラクタ(送達結果再取得時用)
 ///</summary>
 /// <param name="smsId">SMS送達結果通知取得用ID</param>
 public SendSmsDataRequest(string smsId)
 {
     SmsId = smsId;

     Parameter = new Dictionary<string, string>
     {               
         { "smsid", smsId },               
     };
 }
  ```
#### Conclusion of Changes :
##### 1.SendApiEndpoint Removed Parameters in the New Version:
- "smsText2" – Previously set to parameters smstext2.
- "method" – Previously set to USE_IVR.

##### 2.GetResultApiEndpoint  Removed Parameters in the New Version:
- "smstitle" – Previously included the constant SMS_SENDER_NAME.
- "status" – Previously set to USE_RETURN_API.
- "method" – Previously set to USE_IVR.
