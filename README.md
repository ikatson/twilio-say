# Twilio-say

This is a super-simple app to use as a twilio URL callback to say something,
and then hangup.

For example, I use it to call from zabbix for alerts.

## Running
```sh
docker run -it -e TWILIO_SID=<YOUR_SID> -e TWILIO_TOKEN=<YOUR_TOKEN> -e TWILIO_DEFAULT_SAY=<DEFAULT_TEXT_TO_SAY> -p 5000:5000 ikatson/twilio-say
```

Then point URL parameter in Twilio's Call API to the URL of this script.
