import sys
import time
import telepot
import urllib
import urllib.request
import os
import io
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

try:
    fs = open("./config.json","r")
except:
    tp, val, tb = sys.exc_info()
    print("Errored when loading config.json:"+str(val).split(',')[0].replace('(','').replace("'",""))
    programPause = input("Press any key to stop...\n")
    exit()

#load config
config = eval(fs.read())
fs.close()
TOKEN = config["TOKEN"]
OWNER_ID = config["OWNER_ID"]   
Channel_username = config["Channel_username"] 
Debug = config["Debug"]
replyorg = {}

def on_chat_message(msg):
    global replyorg
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    log("[Debug] Raw message:"+str(msg))
    dlog = "["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info]"
    try:
        dlog=dlog+"[EDITED"+str(msg['edit_date'])+"]"
    except:
        time.sleep(0)
    try:
        fuser= bot.getChatMember(chat_id,msg['from']['id'])
    except:
        fnick = "Channel Admin"
        fuserid = None
    else:
        fnick = fuser['user']['first_name']
        try:
            fnick = fnick + ' ' + fuser['user']['last_name']
        except:
            fnick = fnick
        try:
            fnick= fnick +"@"+ fuser['user']['username']
        except:
            fnick= fnick
        fuserid = str(fuser['user']['id'])
    if chat_type == 'private':
        dlog = dlog + "[Private]["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            dlog = dlog
        else:
            if reply_to == bot_me['id']:
                dlog = dlog + "( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"
            else:
                tuser= msg['reply_to_message']['from']['first_name']
                try:
                    tuser= tuser + ' ' + msg['reply_to_message']['from']['last_name']
                except:
                    tuser= tuser
                try:
                    tuser= tuser + '@' + msg['reply_to_message']['from']['username']
                except:
                    tuser= tuser 
                dlog = dlog + "( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) : " + msg['text']
        else:
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) sent a "+ content_type
        clog(dlog)
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array=msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
            clog(flog)
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
            clog(flog)
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
            clog(flog)
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
            clog(flog)
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
            clog(flog)
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
            clog(flog)
        #message
        if chat_id == OWNER_ID:
            try:
                reply_to = msg['reply_to_message']
            except:
                markup = inlinekeyboardbutton(False)
                dre = bot.sendMessage(chat_id, '你想要對這信息做甚麼', reply_markup=markup,reply_to_message_id=msg['message_id'])
                log("[Debug] Raw sent data:"+str(dre))
                return
            else:
                if content_type == "text":
                    if msg['text'] == '/action':
                        markup = inlinekeyboardbutton(False)
                        dre = bot.sendMessage(chat_id, '你想要對這信息做甚麼', reply_markup=markup,reply_to_message_id=reply_to['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                        return
                    else:
                        try:
                            reply_to_id = reply_to['forward_from']['id']
                        except:
                            markup = inlinekeyboardbutton(False)
                        else:
                            markup = inlinekeyboardbutton(True)
                            replyorg[msg['message_id']] = msg
                        dre = bot.sendMessage(chat_id, '你想要對這信息做甚麼', reply_markup=markup,reply_to_message_id=msg['message_id'])
                        log("[Debug] Raw sent data:"+str(dre))
                else:
                    try:
                        reply_to_id = reply_to['forward_from']['id']
                    except:
                        markup = inlinekeyboardbutton(False)
                    else:
                        markup = inlinekeyboardbutton(True)
                        replyorg[msg['id']] = msg
                    dre = bot.sendMessage(chat_id, '你想要對這信息做甚麼', reply_markup=markup,reply_to_message_id=msg['message_id'])
                    log("[Debug] Raw sent data:"+str(dre))
        else:
            try:
                edit_date = msg['edit_date']
            except:
                time.sleep(0)
            else:
                dre = bot.sendMessage(OWNER_ID,fnick + "編輯了訊息")
                log("[Debug] Raw sent data:"+str(dre))
            dre = bot.forwardMessage(OWNER_ID,chat_id,msg['message_id'])
            log("[Debug] Raw sent data:"+str(dre))
            return
    elif chat_type == 'group' or chat_type == 'supergroup':
        dlog = dlog + "["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']['from']['id']
        except:
            dlog = dlog
        else:
            if reply_to == bot_me['id']:
                dlog = dlog + "( Reply to my message "+str(msg['reply_to_message']['message_id'])+" )"
            else:
                tuser= msg['reply_to_message']['from']['first_name']
                try:
                    tuser= tuser + ' ' + msg['reply_to_message']['from']['last_name']
                except:
                    tuser= tuser
                try:
                    tuser= tuser + '@' + msg['reply_to_message']['from']['username']
                except:
                    tuser= tuser 
                dlog = dlog + "( Reply to "+tuser+"'s message "+str(msg['reply_to_message']['message_id'])+" )"
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+msg['chat']['title']+' ( '+str(chat_id)+ ' ): ' + msg['text']
        elif content_type == 'new_chat_member':
            if msg['new_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' I have been added to ' +msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
            else:
                tuser= msg['new_chat_member']['first_name']
                try:
                    tuser= tuser + ' ' + msg['new_chat_member']['last_name']
                except:
                    tuser= tuser
                try:
                    tuser= tuser + '@' + msg['new_chat_member']['username']
                except:
                    tuser= tuser 
                dlog = dlog+' '+ tuser +' joined the ' + chat_type+ ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) '
        elif content_type == 'left_chat_member':
            if msg['left_chat_member']['id'] == bot_me['id']:
                dlog = dlog+ ' I have been kicked from ' +msg['chat']['title']+' ( '+str(chat_id)+ ' ) by '+ fnick + " ( "+fuserid+" )"
            else:
                tuser= msg['left_chat_member']['first_name']
                try:
                    tuser= tuser + ' ' + msg['left_chat_member']['last_name']
                except:
                    tuser= tuser
                try:
                    tuser= tuser + '@' + msg['left_chat_member']['username']
                except:
                    tuser= tuser 
                dlog = dlog+' '+ tuser +' left the ' + chat_type + ' '+msg['chat']['title']+' ( '+str(chat_id)+ ' ) '
        else:
            dlog = dlog+ ' ' + fnick + " ( "+fuserid+" ) in "+msg['chat']['title']+' ( '+str(chat_id)+ ' ) sent a '+ content_type
        clog(dlog)
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array=msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
            clog(flog)
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
            clog(flog)
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
            clog(flog)
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
            clog(flog)
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
            clog(flog)
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
            clog(flog)
        #Auto leave group
        dre = bot.sendMessage(chat_id,'I am not belong to here.')
        log("[Debug] Raw sent data:"+str(dre))
        clog('[Info][',msg['message_id'],'] I left the ', chat_type,':',msg['chat']['title'],'(',chat_id,')')
        bot.leaveChat(chat_id)
    elif chat_type == 'channel':
        dlog = dlog + "["+str(msg['message_id'])+"]"
        try:
            reply_to = msg['reply_to_message']
        except:
            dlog = dlog
        else: 
            dlog = dlog + "( Reply to "+str(msg['reply_to_message']['message_id'])+" )"
        if content_type == 'text':
            dlog = dlog+ ' ' + fnick 
            if fuserid:
                dlog = dlog + " ( "+fuserid+" )"
            dlog = dlog + " in channel "+msg['chat']['title']+' ( '+str(chat_id)+ ' ): ' + msg['text']
        else:
            dlog = dlog + ' ' + fnick 
            if fuserid:
                dlog = dlog + " ( "+fuserid+" )"
            dlog = dlog +" in channel"+msg['chat']['title']+' ( '+str(chat_id)+ ' ) sent a '+ content_type
        clog(dlog)
        if content_type == 'photo':
            flog = "[Photo]"
            photo_array=msg['photo']
            photo_array.reverse()
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ photo_array[0]['file_id']
            except:
                flog = flog +"FileID:"+ photo_array[0]['file_id']
            clog(flog)
        elif content_type == 'audio':
            flog = "[Audio]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['audio']['file_id']
            except:
                flog = flog +"FileID:"+ msg['audio']['file_id']
            clog(flog)
        elif content_type == 'document':
            flog = "[Document]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['document']['file_id']
            except:
                flog = flog +"FileID:"+ msg['document']['file_id']
            clog(flog)
        elif content_type == 'video':
            flog = "[Video]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['video']['file_id']
            except:
                flog = flog +"FileID:"+ msg['video']['file_id']
            clog(flog)
        elif content_type == 'voice':
            flog = "[Voice]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['voice']['file_id']
            except:
                flog = flog +"FileID:"+ msg['voice']['file_id']
            clog(flog)
        elif content_type == 'sticker':
            flog = "[Sticker]"
            try:
                flog = flog + "Caption = " +msg['caption'] +" ,FileID:"+ msg['sticker']['file_id']
            except:
                flog = flog +"FileID:"+ msg['sticker']['file_id']
            clog(flog)

def inlinekeyboardbutton(replyable):
    if replyable == True:
        markup = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='直接轉寄到頻道', callback_data='FTC')],
                                [InlineKeyboardButton(text='匿名轉寄到頻道', callback_data='PFTC')],
                                [InlineKeyboardButton(text='回覆他', callback_data='Reply')],
                                [InlineKeyboardButton(text='取消', callback_data='cancel')],
                            ])
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='直接轉寄到頻道', callback_data='FTC')],
                                [InlineKeyboardButton(text='匿名轉寄到頻道', callback_data='PFTC')],
                                [InlineKeyboardButton(text='取消', callback_data='cancel')],
                            ])
    return(markup)

def on_callback_query(msg):
    log("[Debug] Raw query data:"+str(msg))
    orginal_message = msg['message']['reply_to_message']
    message_with_inline_keyboard = msg['message']
    content_type, chat_type, chat_id = telepot.glance(orginal_message)
    bot_me= bot.getMe()
    username= bot_me['username'].replace(' ','')
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info]["+str(query_id)+"] Callback query form "+str(from_id)+" to "+str(orginal_message['message_id'])+" :"+ data)

    if data == 'FTC':
        FTC(chat_id,orginal_message,query_id,message_with_inline_keyboard)
    elif data == 'PFTC':
        PFTC(chat_id,orginal_message,content_type,query_id,message_with_inline_keyboard)
    elif data == 'Reply':
        Reply(chat_id,orginal_message,query_id,message_with_inline_keyboard,orginal_message)
    elif data == 'cancel':
        cancelquery(message_with_inline_keyboard)

def FTC(chat_id,msg,query_id,mwik):
    try:
        dre = bot.forwardMessage(Channel_username,chat_id,msg['message_id'])
        log("[Debug] Raw sent data:"+str(dre))
    except:
        tp, val, tb = sys.exc_info()
        bot.answerCallbackQuery(query_id, text='無法轉寄信息:\n\n'+str(val).split(',')[0].replace('(','').replace("'",""), show_alert=True)
        clog('[ERROR] Unable to forward message to'+Channel_username+' : '+str(val).split(',')[0].replace('(','').replace("'",""))
        return
    bot.answerCallbackQuery(query_id, text='操作已完成\n\n若想要再次對訊息操作請回復訊息並打/action', show_alert=True)
    clog('[Info] Successfully forwarded message to'+Channel_username)
    msg_idf = telepot.message_identifier(mwik)
    bot.editMessageText(msg_idf, '操作已完成\n\n若想要再次對訊息操作請回復訊息並打/action')
    return

def PFTC(chat_id,msg,content_type,query_id,mwik):
    try:
        if content_type == 'text':
            dre = bot.sendMessage(Channel_username,msg['text'])
            log("[Debug] Raw sent data:"+str(dre))
        elif content_type == 'photo':
            try:
                caption=msg['caption']
            except:
                photo_array=msg['photo']
                photo_array.reverse()
                dre = bot.sendPhoto(Channel_username,photo_array[0]['file_id'])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                photo_array=msg['photo']
                photo_array.reverse()
                dre = bot.sendPhoto(Channel_username,photo_array[0]['file_id'],caption=caption)
                log("[Debug] Raw sent data:"+str(dre))
        elif content_type == 'audio':
            try:
                caption=msg['caption']
            except:
                dre = bot.sendAudio(Channel_username,msg['audio']['file_id'])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = bot.sendAudio(Channel_username,msg['audio']['file_id'],caption=caption)
                log("[Debug] Raw sent data:"+str(dre))
        elif content_type == 'document':
            try:
                caption=msg['caption']
            except:
                dre = bot.sendDocument(Channel_username,msg['document']['file_id'])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = bot.sendDocument(Channel_username,msg['document']['file_id'],caption=caption)
                log("[Debug] Raw sent data:"+str(dre))
        elif content_type == 'video':
            try:
                caption=msg['caption']
            except:
                dre = bot.sendVideo(Channel_username,msg['video']['file_id'])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = bot.sendVideo(Channel_username,msg['video']['file_id'],caption=caption)
                log("[Debug] Raw sent data:"+str(dre))
        elif content_type == 'voice':
            try:
                caption=msg['caption']
            except:
                dre = bot.sendVoice(Channel_username,msg['voice']['file_id'])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = bot.sendVoice(Channel_username,msg['voice']['file_id'],caption=caption)
                log("[Debug] Raw sent data:"+str(dre))
        elif content_type == 'sticker':
            try:
                caption=msg['caption']
            except:
                dre = bot.sendSticker(Channel_username,msg['sticker']['file_id'])
                log("[Debug] Raw sent data:"+str(dre))
            else:
                dre = bot.sendSticker(Channel_username,msg['sticker']['file_id'],caption=caption)
                log("[Debug] Raw sent data:"+str(dre))
        else:
            dre = bot.answerCallbackQuery(query_id, text='ERROR:暫不支援的信息種類', show_alert=True)
            log("[Debug] Raw sent data:"+str(dre))
            clog("[ERROR] Unsupported content type:"+content_type)
            return
    except:
        tp, val, tb = sys.exc_info()
        bot.answerCallbackQuery(query_id, text='無法轉寄信息:\n\n'+str(val).split(',')[0].replace('(','').replace("'",""), show_alert=True)
        clog('[ERROR] Unable to send message to'+Channel_username+' : '+str(val).split(',')[0].replace('(','').replace("'",""))
        return
    bot.answerCallbackQuery(query_id, text='操作已完成\n\n若想要再次對訊息操作請回復訊息並打/action', show_alert=True)
    clog('[Info] Successfully sent message to'+Channel_username)
    msg_idf = telepot.message_identifier(mwik)
    bot.editMessageText(msg_idf, '操作已完成\n\n若想要再次對訊息操作請回復訊息並打/action')
    return

def Reply(chat_id,msg,query_id,mwik,orginalmsg):
    global replyorg
    try:
        reply_to_id = replyorg[orginalmsg['message_id']]['reply_to_message']['forward_from']['id']
    except:
        tp, val, tb = sys.exc_info()
        bot.answerCallbackQuery(query_id, text='操作已過期\n\n{0}'.format(str(val).split(',')[0].replace('(','').replace("'","")), show_alert=True)
        return
    bot.sendMessage(reply_to_id,'管理員對您信息的回覆：')
    dre = bot.forwardMessage(reply_to_id,chat_id,msg['message_id'])
    log("[Debug] Raw sent data:"+str(dre))
    bot.answerCallbackQuery(query_id, text='操作已完成\n\n若想要再次對訊息操作請回復訊息並打/action', show_alert=True)
    msg_idf = telepot.message_identifier(mwik)
    bot.editMessageText(msg_idf, '操作已完成\n\n若想要再次對訊息操作請回復訊息並打/action')
    del replyorg[orginalmsg['message_id']]
    return

def cancelquery(mwik):
    msg_idf = telepot.message_identifier(mwik)
    bot.editMessageText(msg_idf, '操作已被取消\n\n若想要再次對訊息操作請回復訊息並打/action')

def clog(text):
    print(text)
    log(text)
    return

def log(text):
    if text[0:7] == "[Debug]":
        if Debug == True:
            logger= io.open(logpath+"-debug.log","a",encoding='utf8')
            logger.write("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"]"+text+"\n")
            logger.close()
        return
    logger= io.open(logpath+".log","a",encoding='utf8')
    logger.write(text+"\n")
    logger.close()
    return

if os.path.isdir("./logs") == False:
    os.mkdir("./logs")
logpath = "./logs/"+time.strftime("%Y-%m-%d-%H-%M-%S").replace("'","")
bot = telepot.Bot(TOKEN)
log("[Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
log("[Debug][Logger] If you don't see this file currectly,turn the viewing encode to UTF-8.")
log("[Debug] Bot's TOKEN is "+TOKEN)
answerer = telepot.helper.Answerer(bot)

#bot.message_loop({'chat': on_chat_message})
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info] Bot has started")
clog("["+time.strftime("%Y/%m/%d-%H:%M:%S").replace("'","")+"][Info] Listening ...")

# Keep the program running.
while 1:
    time.sleep(10)
