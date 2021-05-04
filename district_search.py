import json
import datetime
import requests
from twilio.rest import Client


def msg_test(event=None, context=None):
    account_sid = 'ACf8XXXXXXXXXXfa37e6892'    #update account_id from twillio
    auth_token = '5d5a1XXXXXXXXf3b80a46cfcce'  #update auth_token from twillio
    client = Client(account_sid, auth_token)
    today = datetime.date.today()
    new_today_date = today.strftime("%d-%m-%Y")
    district=['276','265','294']
    length = len(district)
    bd=[]

    for i in range(length):
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+district[i]+"&date=" + new_today_date
        print(url)
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        message = []
        data = json.loads(response.text)
        count = 0
        for i in data['centers']:
            for j in i['sessions']:
                if j['min_age_limit'] == 18:
                    if j['available_capacity'] != 0:
                        print(str(i['name']) + "," + str(i['address']) + "," + str(i['fee_type']) + "," + str(
                            j['date']) + "," + str(j['available_capacity']) + "," + str(j['vaccine']) + "," + "AVAILABLE")
                        message.append("slots are available " + str(
                            i['name'] + " on " + str(j['date']) + " vaccine " + str(j['vaccine'])))
                        count = count + 1
        bd.append(str(i['district_name'])+" - " + str(count) + " slots")
        print(bd)
    
    #Message being sent to whatsapp
    message = client.messages.create(
        from_='whatsapp:+1XXXXXXX',      #whatsapp_from 
        body=format(bd[0]+"\n"+bd[1]+"\n"+bd[2]),  #message_body
        to='whatsapp:+91XXXXXXX6'  #whatsapp_to
    )
    print(message.sid)

msg_test()
