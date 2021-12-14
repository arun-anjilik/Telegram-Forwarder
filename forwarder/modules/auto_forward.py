from telegram import Bot, Update
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import time
import queue

from forwarder import FROM_CHATS, TO_CHATS, GIF_CHATS, LOGGER, dispatcher
l = queue.Queue(maxsize=100)
@run_async
def forward(bot: Bot, update: Update):
  if not (update.effective_message.text):
        message = update.effective_message  # type: Optional[Message]
        
        from_chat_id = update.effective_chat.id
        from_chat_name = update.effective_chat.title or update.effective_chat.first_name
        mid = message.message_id
        # arr=[]
        # arr.append(mid)
        
        # bot.send_message(chat_id=from_chat_id, text=mid)
        try:
          if not(l.full()):
               # i = 0  
               # rmid = arr[0]
              l.put(mid)
             # for i in range(50):
               #      arr[i] = arr[i+1]
               # arr.append(mid)
          else:
            rmid = l.get()
            bot.delete_message(chat_id=from_chat_id, message_id=rmid)
        except:
                LOGGER.exception("Error while forwarding message from chat \"{}\" to chat \"\".".\
                             format(from_chat_name))
           
        


try:
    FORWARD_HANDLER = MessageHandler(Filters.chat(FROM_CHATS) & ~Filters.status_update & ~Filters.command,
                                     forward, channel_post_updates=True)
    
    dispatcher.add_handler(FORWARD_HANDLER)

except ValueError:  # When FROM_CHATS list is not set because user doesn't know chat id(s)
    LOGGER.warn("I can't FORWARD_HANDLER because your FROM_CHATS list is empty.")   
