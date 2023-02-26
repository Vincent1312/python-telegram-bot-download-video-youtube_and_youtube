import re,time,sys
import os,pyshorteners,json,random,string
from telegram import * #Update, InlineKeyboardButton, InlineKeyboardMarkup,KeyboardButton
from telegram.ext import * #Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, PicklePersistence
import requests,keyboard,json,aiohttp,asyncio,datetime , pyshorteners
from pprint import pprint
import tracemalloc
import itertools
from datetime import date


token = 'Your_token'
updater = Updater(token) #điền token t.me/gsdtiki_bot


#Api source from Xdownload

headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
	   }

#download publish video facebook function
def dl_facebook(link_fb,user_id):
	print("aaaaaaa")
	global link_download
	url_res = 'https://x2download.app/api/ajaxSearch'
	data = {'q':f'{link_fb}','vt': 'home'}
	res = requests.post(url_res,headers=headers,data=data)
	try:
		jsondata = res.json()
		data = jsondata['links']
		link_download = data['sd']
		duration = jsondata['duration']
		title = jsondata['title']
		image = jsondata['thumbnail']
		print(link_download)
		print(duration)
		print(title)
		print(image)
		return link_download
	except:
		print("Vui Lòng Kiểm Tra Lại Link! Có Thể Link Sai Hoặc Link Từ Group Kín Facebook.")
		uptele = requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text="+"Vui Lòng Kiểm Tra Lại Link! Có Thể Link Sai Hoặc Link Từ Group Kín Facebook.")



#download video youtube function
def dl_youtube(link_youtube,user_id):
	url_res1 = 'https://x2download.com/api/ajaxSearch'
	headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
   }
	data = {'q':f'{link_youtube}','vt': 'home'}
	res = requests.post(url_res1,headers=headers,data=data)
	try:
		data = res.json()
		print(data)
		vid = data['vid']
		title = data['title']
		token = data['token']
		timeExpires = data['timeExpires']
		print(vid)
		print(title)
		print(token)
		print(timeExpires)
		data_dl_youtube = getlink_youtube(vid,title,token,timeExpires,user_id)
		return data_dl_youtube
	except:
		print("Vui Lòng Kiểm Tra Lại Link.")


def getlink_youtube(vid,title,token,timeExpires,user_id):
	list_fquality = ['1080p','720p','480p','360p','144p']
	for i in list_fquality:
		data = {
	  'v_id': f'{vid}',
	  'ftype': 'mp4',
	  'fquality': f'{i}',
# 	  'fname': f'{title}',
	  'token': f'{token}',
	  'timeExpire': f'{timeExpires}',
	'client': 'X2Download.app'
		}
		try:
			response = requests.post('https://dd107.opoaidazzc.xyz/api/json/convert', headers=headers, data=data)
			datajson = response.json()
			result = datajson['result']
			statusCode = datajson['statusCode']
			if statusCode == 200:
				print(result)
				return result
				break
			else:
				print('Converting')
		except:
			print("Vui Lòng Kiểm Tra Lại Link!.")



#-------------------start facebook download command
def echo_facebook(update: Update, context: CallbackContext):
	user_id = update.effective_user.id
	link_facebook = update.message.text
	if 'facebook' in link_facebook :
		update.message.reply_text(f'Bạn Vui Lòng Chờ Tí Nhé 🥰')
		data = dl_facebook(link_facebook,user_id)
		if data != None:
			update.message.reply_text('✨Dưới Đây Là Link Tải Facebook Của Bạn:',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Click Để Tải ^^', url=f'{data}')]]))
	else :
		update.message.reply_text(f'❗️Hình như không phải link facebook rồi.')
		time.sleep(1)
		update.message.reply_text(f'❗️Nếu bạn muốn dùng commands khác mà bị kẹt command hiện tại thì vui lòng gõ /cancel để thoát khỏi các command cũ.')

def facebook_command(update: Update, context: CallbackContext):
	first_name = update.effective_user.first_name
	user_name = update.effective_user.username
	
	print("Đang có người sử dụng chức năng tải video facebook")
	print(first_name)	
	print(user_name)
	update.message.reply_text(f'✨CHẾ ĐỘ TẢI VIDEO FACEBOOK ➖➖➖➖➖\n✨Mời bạn nhập link cần rút gọn (❗️Nhớ là link facebook chứ không nó lỗi lỗi á 😘): \n')
	updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_facebook))

updater.dispatcher.add_handler(CommandHandler('facebook', facebook_command)) #chạy lệnh command
#-------------------end facebook download command	


#-------------------start youtube download command
def echo_youtube(update: Update, context: CallbackContext):
	user_id = update.effective_user.id
	link_youtube = update.message.text
	if 'youtube' in link_youtube :
		update.message.reply_text(f'Bạn Vui Lòng Chờ Tí Nhé 🥰')
		data = dl_youtube(link_youtube,user_id)
		if data != None:
			update.message.reply_text('✨Dưới Đây Là Link Tải Youtube Của Bạn:',reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Click Để Tải ^^', url=f'{data}')]]))
	else :
		update.message.reply_text(f'❗️Hình như không phải link youtube rồi.')
		time.sleep(1)
		update.message.reply_text(f'❗️Nếu bạn muốn dùng commands khác mà bị kẹt command hiện tại thì vui lòng gõ /cancel để thoát khỏi các command cũ.')

def youtube_command(update: Update, context: CallbackContext):
	first_name = update.effective_user.first_name
	user_name = update.effective_user.username
	print("Đang có người sử dụng chức năng tải video youtube")
	print(first_name)	
	print(user_name)
	update.message.reply_text(f'✨CHẾ ĐỘ TẢI VIDEO YOUTUBE ➖➖➖➖➖\n✨Mời bạn nhập link cần rút gọn (❗️Nhớ là link youtube chứ không nó lỗi lỗi á 😘): \n')
	updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_youtube))

updater.dispatcher.add_handler(CommandHandler('youtube', youtube_command)) #chạy lệnh command
#-------------------end youtube download command	


#--------------- Start cancel command
def cancel_command(update: Update, context: CallbackContext) -> None:
	first_name = update.effective_user.first_name
	user_name = update.effective_user.username
	user_id = update.effective_user.id  
	print("Đang có người sử dụng lệnh cannel")
	print(first_name)	
	print(user_name)	
	print(user_id)
	print("Restarting...")
	update.message.reply_text(f'Đã cancel tất cả các commands trước')	
	os.execl(sys.executable, sys.executable, *sys.argv)
	
updater.dispatcher.add_handler(CommandHandler('cancel', cancel_command)) #chạy lệnh command



updater.start_polling()
updater.idle()


