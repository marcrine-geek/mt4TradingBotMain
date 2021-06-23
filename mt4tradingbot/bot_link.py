@app.route('/leader/<string:telegramid>', methods=['GET','POST'])
def leader(telegramid):
    global user_leader_id
    global leader_id_f_link
    leader_id_f_link = telegramid

    # print('Data being passed to stop the bot')

    # with app.app_context():

    #     db.session.query(Telegram).filter(Telegram.telegramid == closetid).update({Telegram.inviter_id: l_telegram_id})

    #     db.session.commit()

    # print('Data has been passed to stop the bot')

    # saving in a csv file
    row_list = [
        [telegramid]
    ]
    print('telegram ids............', telegramid)
    with open('leaderid.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter = ';')
        writer.writerows(row_list)

    print('Webhook REsource Started to manage Auto-TRading from TradingView')
    #generate api id and hash on https://my.telegram.org
    #name = 'Binance_TradingView_Bot'
  
    print('telegramid-------------------', leader_id_f_link)
    #res = copy(telegramid)
    print('result of leaders id passed ',leader_id_f_link)
        
    print('_____________TESTING ASSET WITHOUT MODEL RESOURCE______________________')

    return "<a href = https://t.me/phemexcopytradingbot?start=testing  >Click here to start bot</a>"
    