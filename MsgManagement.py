import sys
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent

TOKEN = '' #Insert your bot tokens here.
OWNER_ID = int()   #Insert your user ID here.
Channel_username = '@' #Insert Channel's username here.


message_with_inline_keyboard = None
orginal_message = None
reply_to_id=None
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    if chat_id != OWNER_ID:
        try:
            print('[EDIT][',msg['edit_date'],']:',msg['message_id'],' -->',msg['text'])
        except:
            time.sleep(0)
        else:
            try:
                bot.sendMessage(OWNER_ID,msg['from']['username']+' 編輯了信息')
            except:
                bot.sendMessage(OWNER_ID,msg['from']['id']+'(No Username) 編輯了信息')
        if chat_type == 'private':
            try:
                reply_to = msg['reply_to_message']['from']['id']
            except:
                bot.forwardMessage(OWNER_ID,chat_id,msg['message_id'])
                if content_type != 'text':
                    try:
                        print('[Info][',msg['message_id'],']',msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                    except:
                        print('[Info][',msg['message_id'],']',chat_id, ' sent a ', content_type)
                    return
                try:
                    print('[Info][',msg['message_id'],']',msg['chat']['username'],'(',chat_id, ') :', msg['text'])
                except:
                    print('[Info][',msg['message_id'],']',chat_id, ' :', msg['text'])
            else:
                try:
                    bot.sendMessage(OWNER_ID,msg['from']['username']+' 回覆了 '+msg['reply_to_message']['from']['username'])
                except:
                    try:
                        bot.sendMessage(OWNER_ID,msg['from']['id']+'(No Username) 回覆了 '+msg['reply_to_message']['from']['username'])
                    except:
                        try:
                            bot.sendMessage(OWNER_ID,msg['from']['username']+' 回覆了 '+msg['reply_to_message']['from']['id'],'(No Username)')
                        except:
                            bot.sendMessage(OWNER_ID,msg['from']['id']+'(No Username) 回覆了 '+msg['reply_to_message']['from']['id'],'(No Username)')
                bot.forwardMessage(OWNER_ID,chat_id,msg['message_id'])
                if content_type != 'text':
                    try:
                        print('[Info][',msg['message_id'],'](Reply)',msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                    except:
                        print('[Info][',msg['message_id'],'](Reply)',chat_id, ' sent a ', content_type)
                    return
                try:
                    print('[Info][',msg['message_id'],'](Reply)',msg['chat']['username'],'(',chat_id, ') :', msg['text'])
                except:
                    print('[Info][',msg['message_id'],'](Reply)',chat_id, ' :', msg['text'])
                return
        elif chat_type == 'group' or chat_type == 'supergroup':
            try:
                reply_to = msg['reply_to_message']['from']['id']
            except:
                if content_type != 'text':
                    if content_type == 'new_chat_member':
                        if msg['new_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',msg['message_id'],'] I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                            except:
                                print('[Info][',msg['message_id'],'] I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                        else:
                            try:
                                print('[Info][',msg['message_id'],'] ',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                print('[Info][',msg['message_id'],'] ',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                    elif content_type == 'left_chat_member':
                        if msg['left_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',msg['message_id'],'] I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                            except:
                                print('[Info][',msg['message_id'],'] I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                        else:
                            try:
                                print('[Info][',msg['message_id'],'] ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                print('[Info][',msg['message_id'],'] ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                    else:
                        try:
                            print('[Info][',msg['message_id'],']',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                        except:
                            print('[Info][',msg['message_id'],']',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                    bot.sendMessage(chat_id,'I am not belong to here.')
                    print('[Info][',msg['message_id'],'] I left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                    bot.leaveChat(chat_id) 
                    return
                try:
                    print('[Info][',msg['message_id'],']',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                except:
                    print('[Info][',msg['message_id'],']',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                bot.sendMessage(chat_id,'I am not belong to here.')
                print('[Info][',msg['message_id'],'] I left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                bot.leaveChat(chat_id)  
            else:
                if content_type != 'text':
                    if content_type == 'new_chat_member':
                        if imsg['new_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                                except:
                                    try:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                                    except:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                        else:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['new_chat_member']['username'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                except:
                                    try:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                    except:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['new_chat_member']['id'],' joined a ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                    elif content_type == 'left_chat_member':
                        if msg['left_chat_member']['id'] == bot_me['id']:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['username'],'(',msg['from']['id'],')')
                                except:
                                    try:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                                    except:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') I have been kicked from ', chat_type,':',msg['chat']['title'],'(',chat_id,') by',msg['from']['id'])
                        else:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['left_chat_member']['username'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                except:
                                    try:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],') ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                                    except:
                                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],') ',msg['left_chat_member']['id'],' left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                    else:
                        try:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                        except:
                            try:
                                print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                            except:
                                try:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                                except:
                                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ')sent a ', content_type)
                    bot.sendMessage(chat_id,'I am not belong to here.')
                    print('[Info][',msg['message_id'],'] I left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                    bot.leaveChat(chat_id) 
                    return
                try:
                    print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                except:
                    try:
                        print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['username'],'(',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                    except:
                        try:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['username'],')',msg['from']['id'], ' in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                        except:
                            print('[Info][',msg['message_id'],'] (Reply to ',msg['reply_to_message']['from']['id'],')',msg['from']['id'], ') in',msg['chat']['title'],'(',chat_id, ') :',msg['text'])
                bot.sendMessage(chat_id,'I am not belong to here.')
                print('[Info][',msg['message_id'],'] I left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
                bot.leaveChat(chat_id)
    else:
        global message_with_inline_keyboard
        global orginal_message
        global reply_to_id
        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            bot.editMessageText(msg_idf, '操作已被取消')
        reply_to_id = None
        message_with_inline_keyboard=None
        orginal_message=None
        try:
            print('[EDIT][',msg['edit_date'],']:',msg['message_id'],' -->',msg['text'])
        except:
            time.sleep(0)
        #else:
            #bot.sendMessage(OWNER_ID,msg['from']['username']+' 編輯了信息')
        try:
            reply_to = msg['reply_to_message']
        except:
            #bot.forwardMessage(OWNER_ID,chat_id,msg['message_id'])
            if content_type != 'text':
                try:
                    print('[Info][',msg['message_id'],']',msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                except:
                    print('[Info][',msg['message_id'],']',chat_id, ' sent a ', content_type)
            else:
                try:
                    print('[Info][',msg['message_id'],']',msg['chat']['username'],'(',chat_id, ') :', msg['text'])
                except:
                    print('[Info][',msg['message_id'],']',chat_id, ' :', msg['text'])
            markup = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='直接轉寄到頻道', callback_data='FTC')],
                        [InlineKeyboardButton(text='匿名轉寄到頻道', callback_data='PFTC')],
                        [InlineKeyboardButton(text='取消', callback_data='cancel')],
                    ])

            orginal_message  = msg
            message_with_inline_keyboard = bot.sendMessage(chat_id, '你想要對這信息做甚麼', reply_markup=markup,reply_to_message_id=msg['message_id'])
        else:

            #bot.sendMessage(OWNER_ID,msg['from']['username']+' 回覆了 '+msg['reply_to_message']['from']['username'])
            #bot.forwardMessage(OWNER_ID,chat_id,msg['message_id'])
            if content_type != 'text':
                try:
                    print('[Info][',msg['message_id'],'](Reply)',msg['chat']['username'],'(',chat_id, ') sent a ', content_type)
                except:
                    print('[Info][',msg['message_id'],'](Reply)',chat_id, ' sent a ', content_type)
                bot.sendMessage(chat_id,'如果你想要傳送你回覆的信息，請回覆該信息後打 /action 指令，否則將直接受理您送的信息',reply_to_message_id=reply_to['message_id'])
                try:
                    reply_to_id = reply_to['forward_from']['id']
                except:
                    markup = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='直接轉寄到頻道', callback_data='FTC')],
                        [InlineKeyboardButton(text='匿名轉寄到頻道', callback_data='PFTC')],
                        [InlineKeyboardButton(text='取消', callback_data='cancel')],
                    ])
                else:
                    markup = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='直接轉寄到頻道', callback_data='FTC')],
                            [InlineKeyboardButton(text='匿名轉寄到頻道', callback_data='PFTC')],
                            [InlineKeyboardButton(text='回覆他', callback_data='Reply')],
                            [InlineKeyboardButton(text='取消', callback_data='cancel')],
                        ])
                orginal_message  = msg
                message_with_inline_keyboard = bot.sendMessage(chat_id, '你想要對這信息做甚麼', reply_markup=markup,reply_to_message_id=msg['message_id'])
                return
            try:
                print('[Info][',msg['message_id'],'](Reply)',msg['chat']['username'],'(',chat_id, ') :', msg['text'])
            except:
                print('[Info][',msg['message_id'],'](Reply)',chat_id, ' :', msg['text'])
            if msg['text'] == '/action':
                markup = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text='直接轉寄到頻道', callback_data='FTC')],
                        [InlineKeyboardButton(text='匿名轉寄到頻道', callback_data='PFTC')],
                        [InlineKeyboardButton(text='取消', callback_data='cancel')],
                    ])
                orginal_message  = reply_to
                message_with_inline_keyboard = bot.sendMessage(chat_id, '你想要對這信息做甚麼', reply_markup=markup,reply_to_message_id=reply_to['message_id'])
            else:
                bot.sendMessage(chat_id,'如果你想要傳送你回覆的信息，請回覆該信息後打 /action 指令，否則將直接受理您送的信息',reply_to_message_id=reply_to['message_id'])
                try:
                    reply_to_id = reply_to['forward_from']['id']
                except:
                    markup = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='直接轉寄到頻道', callback_data='FTC')],
                                [InlineKeyboardButton(text='匿名轉寄到頻道', callback_data='PFTC')],
                                [InlineKeyboardButton(text='取消', callback_data='cancel')],
                            ])
                else:
                    markup = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='直接轉寄到頻道', callback_data='FTC')],
                                [InlineKeyboardButton(text='匿名轉寄到頻道', callback_data='PFTC')],
                                [InlineKeyboardButton(text='回覆他', callback_data='Reply')],
                                [InlineKeyboardButton(text='取消', callback_data='cancel')],
                            ])
                orginal_message  = msg
                message_with_inline_keyboard = bot.sendMessage(chat_id, '你想要對這信息做甚麼', reply_markup=markup,reply_to_message_id=msg['message_id'])
            return 
        
        
def on_callback_query(msg):
    global orginal_message
    global message_with_inline_keyboard
    global reply_to_id
    if orginal_message:
        content_type, chat_type, chat_id = telepot.glance(orginal_message)
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('[Info] Callback query:', query_id, from_id, data)

    if data == 'FTC':
        if orginal_message:
            try:
                bot.forwardMessage(Channel_username,chat_id,orginal_message['message_id'])
            except:
                bot.answerCallbackQuery(query_id, text='ERROR:無法轉寄信息(機器人沒有在頻道內或沒有權限發送訊息)', show_alert=True)
                print('[ERROR] Unable to forward message to',Channel_username,' : Permission denied')
                return
            bot.answerCallbackQuery(query_id, text='操作已完成...', show_alert=True)

            if message_with_inline_keyboard:
                msg_idf = telepot.message_identifier(message_with_inline_keyboard)
                bot.editMessageText(msg_idf, '操作已完成')
            else:
                bot.answerCallbackQuery(query_id, text='ERROR:找不到可編輯的信息', show_alert=True)
                return
        else:
            bot.answerCallbackQuery(query_id, text='ERROR:無法轉寄信息(找不到要轉送的信息)', show_alert=True)
            print('[ERROR] Unable to forward message to',Channel_username,' : Message not found')
            return
    elif data == 'PFTC':
        #print(orginal_message, Channel_username, content_type)
        if orginal_message:
            try:
                if content_type == 'text':
                    bot.sendMessage(Channel_username,orginal_message['text'])
                elif content_type == 'photo':
                    try:
                        caption=orginal_message['caption']
                    except:
                        photo_array=orginal_message['photo']
                        photo_array.reverse()
                        bot.sendPhoto(Channel_username,photo_array[1]['file_id'])
                    else:
                        photo_array=orginal_message['photo']
                        photo_array.reverse()
                        bot.sendPhoto(Channel_username,photo_array[1]['file_id'],caption=caption)
                elif content_type == 'audio':
                    try:
                        caption=orginal_message['caption']
                    except:
                        bot.sendAudio(Channel_username,orginal_message['audio']['file_id'])
                    else:
                        bot.sendAudio(Channel_username,orginal_message['audio']['file_id'],caption=caption)
                elif content_type == 'document':
                    try:
                        caption=orginal_message['caption']
                    except:
                        bot.sendDocument(Channel_username,orginal_message['document']['file_id'])
                    else:
                        bot.sendDocument(Channel_username,orginal_message['document']['file_id'],caption=caption)
                elif content_type == 'video':
                    try:
                        caption=orginal_message['caption']
                    except:
                        bot.sendVideo(Channel_username,orginal_message['video']['file_id'])
                    else:
                        bot.sendVideo(Channel_username,orginal_message['video']['file_id'],caption=caption)
                elif content_type == 'voice':
                    try:
                        caption=orginal_message['caption']
                    except:
                        bot.sendVoice(Channel_username,orginal_message['voice']['file_id'])
                    else:
                        bot.sendVoice(Channel_username,orginal_message['voice']['file_id'],caption=caption)
                elif content_type == 'sticker':
                    try:
                        caption=orginal_message['caption']
                    except:
                        bot.sendSticker(Channel_username,orginal_message['sticker']['file_id'])
                    else:
                        bot.sendSticker(Channel_username,orginal_message['sticker']['file_id'],caption=caption)
                else:
                    bot.answerCallbackQuery(query_id, text='ERROR:不支援的信息種類', show_alert=True)
                    return
            except:
                bot.answerCallbackQuery(query_id, text='ERROR:無法轉寄信息(機器人沒有在頻道內或沒有權限傳送訊息)', show_alert=True)
                print('[ERROR] Unable to send message to',Channel_username,' : Permission denied')
                return
            bot.answerCallbackQuery(query_id, text='操作已完成...', show_alert=True)
            if message_with_inline_keyboard:
                msg_idf = telepot.message_identifier(message_with_inline_keyboard)
                bot.editMessageText(msg_idf, '操作已完成')
            else:
                bot.answerCallbackQuery(query_id, text='ERROR:找不到可編輯的信息', show_alert=True)
                return
        else:
            bot.answerCallbackQuery(query_id, text='ERROR:無法轉寄信息(找不到要轉送的信息)', show_alert=True)
            print('[ERROR] Unable to send message to',Channel_username,' : Message not found')
            return
    elif data == 'Reply':
        if orginal_message:
            if reply_to_id:
                bot.sendMessage(reply_to_id,'管理員對您信息的回覆：')
                bot.forwardMessage(reply_to_id,chat_id,orginal_message['message_id'])
                bot.answerCallbackQuery(query_id, text='操作已完成...', show_alert=True)
                if message_with_inline_keyboard:
                    msg_idf = telepot.message_identifier(message_with_inline_keyboard)
                    bot.editMessageText(msg_idf, '操作已完成')
                else:
                    bot.answerCallbackQuery(query_id, text='ERROR:找不到可編輯的信息', show_alert=True)
                    return
            else:
                bot.answerCallbackQuery(query_id, text='ERROR:無法回覆信息(找不到要回覆的對象)', show_alert=True)
                return
        else:
            bot.answerCallbackQuery(query_id, text='ERROR:無法轉寄信息(找不到要轉送的信息)', show_alert=True)
            return
    elif data == 'cancel':
        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            bot.editMessageText(msg_idf, '操作已被取消')
        else:
            bot.answerCallbackQuery(query_id, text='ERROR:找不到可編輯的信息', show_alert=True)
            return
    reply_to_id = None
    message_with_inline_keyboard=None
    orginal_message=None

bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('[Info] Bot has started')
print('[Info] Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
