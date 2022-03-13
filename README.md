# communication app bot

## what is this
This project is amied to create a python package can easily send message to any communication app

> Support telegram right now, fell free to let me know which app you want to have this function

### Installing

```
pip3 install communicationAppModule
```

### prerequisite

* Telegram
>create a bot via botfather to get a bot token

### Create Client
```py
# bot token only for telegram
# db_name optional
# log_file_name optional

client = createClient('Telegram', bot_token ='', db_name ='', log_file_name='')
```

### Send Message
```py
# send single sentence
client.send_message("hi")

# send multi line
client.send_message(['hi','John', 'this is wayne'])
```

### Get message
```py
# send last response
client.get_response()

# get multi responses
client.get_response(10)
```

### Response Format
```json
{
"status_code": 200, 
"data": [{
    "user_info":{},
    "date": "timestamp",
    "text": "string"
    }],
"error": "string"
}

```

