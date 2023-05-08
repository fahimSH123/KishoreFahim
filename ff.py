import urllib.request
event='meet'
time='11:67'
body="Hello%20Greeting%20for%20the%20day%20Your%20event%20name%20"+str(event)+"%20is%20scheduled%20from%20"+str(time)+"%20Do%20bring%20laptop%20for%20this%20event"
urllib.request.urlopen('https://www.fast2sms.com/dev/bulkV2?authorization=uEXyjpio5NjLERWLSciOMnyk1s7MZ4qtdCoKehIiKXAgeXVJ5Xgad6E7sqiU&route=v3&sender_id=Cghpet&message='+body+'&language=english&flash=0&numbers=9025457430')
