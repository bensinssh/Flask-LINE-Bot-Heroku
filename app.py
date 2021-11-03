import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    # print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name

    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)

    reply(intent,text,reply_token,id,disname)

    return 'OK'


def reply(intent,text,reply_token,id,disname):
    if intent == 'intent 5':
        text_message = TextSendMessage(text='ทดสอบสำเร็จ')
        line_bot_api.reply_message(reply_token,text_message)

if __name__ == "__main__":
    app.run()



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
#=========[ LEAVE GROUP OR ROOM ]==========
    if text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
#=====[ TEMPLATE MESSAGE ]=============
    elif text == '/template':
        buttons_template = TemplateSendMessage(
            alt_text='template',
            template=ButtonsTemplate(
                title='[ TEMPLATE MSG ]',
                text= 'Tap the Button',
                actions=[
                    MessageTemplateAction(
                        label='Culum 1',
                        text='/aditmadzs'
                    ),
                    MessageTemplateAction(
                        label='CULUM 2',
                        text='/aditmadzs'
                    ),
                    MessageTemplateAction(
                        label='CULUM 3',
                        text='/aditmadzs'
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, buttons_template)
#=====[ CAROUSEL MESSAGE ]==========
    elif text == '/carousel':
        message = TemplateSendMessage(
            alt_text='OTHER MENU',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='ADD ME',
                        text='Contact Aditmadzs',
                        actions=[
                            URITemplateAction(
                                label='>TAP HERE<',
                                uri='https://line.me/ti/p/~adit_cmct'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='Instagram',
                        text='FIND ME ON INSTAGRAM',
                        actions=[
                            URITemplateAction(
                                label='>TAP HERE!<',
                                uri='http://line.me/ti/p/~adit_cmct'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
#=====[ FLEX MESSAGE ]==========
    elif text == 'flex':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://lh5.googleusercontent.com/VoOmR6tVRwKEow0HySsJ_UdrQrqrpwUwSzQnGa0yBeqSex-4Osar2w-JohT6yPu4Vl4qchND78aU2c5a5Bhl=w1366-h641-rw',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://line.me/ti/p/~adit_cmct', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Aditmadzs', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Tangerang, Indonesia',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='Aditmadzs', uri="https://line.me/ti/p/~adit_cmct")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
 

