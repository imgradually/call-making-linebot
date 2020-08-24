import copy
flex_message = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Do you want me to call?",
        "size": "xl",
        "color": "#FFFFFF",
        "wrap": True
      }
    ],
    "backgroundColor": "#000000"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "Yes",
          "data": "call somegroup"
        },
        "color": "#FFFFFF"
      },
      {
        "type": "button",
        "action": {
          "type": "postback",
          "label": "No",
          "data": "no"
        },
        "color": "#FFFFFF"
      }
    ],
    "backgroundColor": "#FF0000"
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}
button_example={
        "type": "button",
        "action": {
          "type": "message",
          "label": "default_option",
          "text": "default_data"
        },
        "color": "#FFFFFF"
      }
def set_button(index='text',return_type='message',data='data',option='option'):
    button=copy.deepcopy(button_example)
    button["action"][index] = data
    button["action"]["type"] = return_type
    button["action"]["label"] = option
    return button
def set_flex(question='Yes or No?',do=[['Yes','Yes'],['No','No']],return_type='message'):
    message=copy.deepcopy(flex_message)
    message["body"]["contents"][0]["text"] = question
    index = "text"
    if return_type == 'postback':
        index = "data"
    message["footer"]["contents"][0]["action"][index] = do[0][0]
    message["footer"]["contents"][0]["action"]["type"] = return_type
    message["footer"]["contents"][0]["action"]["label"] = do[0][1]
    message["footer"]["contents"][1]["action"][index] = do[1][0]
    message["footer"]["contents"][1]["action"]["type"] = return_type
    message["footer"]["contents"][1]["action"]["label"] = do[1][1]
    for i in range(2,len(do)):
        #print(do[i][0],' ',do[i][1])
        tmp_button = set_button(index=index,return_type=return_type,data=do[i][0],option=do[i][1])
        message["footer"]["contents"].append(copy.deepcopy(tmp_button))
    return message