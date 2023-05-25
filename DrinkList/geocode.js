function doPost(e) {
    //認證身份，重新輸入line@ access_token
    var CHANNEL_ACCESS_TOKEN = 'BH9fBAs/qirZVdcPCcQQ/rvCdq3Nwg0wUdJvQmcRux84p1Vk10IwqdehHGWTTPZFnupvwhDmQd8rg0+GolEx0305sEmU57tUZGF4J/7nFXxdK1KbT9zB8H8An5cNy03celRzKUWjI1yRMwtfOnZjnQdB04t89/1O/w1cDnyilFU=';//這邊要改成你的 CHANNEL_ACCESS_TOKEN
    var msg= JSON.parse(e.postData.contents);
  
    //除錯用
    //Logger.log(msg);
    console.log(msg);
  
    //從接收到的訊息中取出 replayToken 和發送的訊息文字
    var replyToken = msg.events[0].replyToken;
    var userMessage = msg.events[0].message.text;
    var userid = msg.events[0].source.userId;
  
    if (typeof replyToken === 'undefined') {
       return;
    };
  
    //定義回傳訊息
  var userMessageNum = parseInt(userMessage); //parseInt 是可將字串轉換成整數的方式
    if (isNaN(parseInt(userMessage))) {//測試是不是數字
       if(userMessage.match("帶我去")){//測試是不是要開地圖
          var posotion = userMessage.replace("帶我去","");
  
          var mapResponse = Maps.newGeocoder().geocode(posotion);
          console.log(mapResponse);
          var returnmessage=[{
             "type": "location",
             "title": posotion,
             "address": mapResponse.results[0].formatted_address,
             "latitude": mapResponse.results[0].geometry.location.lat,
             "longitude": mapResponse.results[0].geometry.location.lng
           }]
       }else{
  
          var returnmessage=[{
             'type': 'text',
             'text': "我是中邊Bot"
          }];
  
       };
  
    }else{
       var returnmessage=[{
          'type': 'text',
           'text': parseInt(userMessageNum)*2
        }];
    };
    //回傳訊息給line 並傳送給使用者
    var url = 'https://api.line.me/v2/bot/message/reply';
    UrlFetchApp.fetch(url, {
          'headers': {
          'Content-Type': 'application/json; charset=UTF-8',
          'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN,
       },
        'method': 'post',
        'payload': JSON.stringify({
           'replyToken': replyToken,
           'messages': returnmessage,
       }),
    });
  }