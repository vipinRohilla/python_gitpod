# API to extact the google reviews

from google_play_scraper import Sort, reviews_all
import pandas as pd
import numpy as np
import string
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods = ['GET'])

def getGooglePlayStoreHavellsSyncAppReviews():

    # fetching all the Havells Sync reviews from google play store
    havells_android_reviews = reviews_all(
    'com.havells.havellsone',
        lang = 'en',
        country = 'in',
        sort = Sort.NEWEST
    )

    # converting it to python data frame
    havells_android_reviews = pd.DataFrame(np.array(havells_android_reviews), columns =['review'])
    havells_android_reviews = havells_android_reviews.join(pd.DataFrame(havells_android_reviews.pop('review').tolist()))


    # droping the extra column from the data frame of havells_android_reviews and storing it to the new variable (havells_android_reviews_copy)
    havells_android_reviews_copy = havells_android_reviews.drop(columns= ['reviewId', 'userName','userImage', 'thumbsUpCount', 'reviewCreatedVersion', 'at', 'replyContent', 'repliedAt'], axis = 1)

    # storing every field of data frame into some variable to operate some functions
    content_array = np.array(havells_android_reviews['content']).tolist()
    reviewId_array = np.array(havells_android_reviews['reviewId']).tolist()
    userName_array = np.array(havells_android_reviews['userName']).tolist()
    userImage_array = np.array(havells_android_reviews['userImage']).tolist()
    thumbsUpCount_array = np.array(havells_android_reviews['thumbsUpCount']).tolist()
    reviewCreatedVersion_array = np.array(havells_android_reviews['reviewCreatedVersion']).tolist()
    at_array = np.array(havells_android_reviews['at']).tolist()
    replyContent_array = np.array(havells_android_reviews['replyContent']).tolist()
    repliedAt_array = np.array(havells_android_reviews['repliedAt']).tolist()

    #seperating all the words and storing it in final_words
    #example "I am Happy" -> "I" , "am", "Happy"
    final_words = []
    for i in content_array:
        lower_case = i.lower()
        cleaned_text = lower_case.translate(str.maketrans('','',string.punctuation))
        tokenized_words = cleaned_text.split()
        final_words.append(tokenized_words)


    #list of unnecessary words which we need to remove from our reviews 
    removed_all_these_words = ['👍','☹️','😡','1','2','3','4','5','6','7','8','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    #removing the unnecessary words from the reviews and storing it in complete_words
    complete_words = []
    for i in final_words:
        last_words = []
        for j in i:
            if j not in removed_all_these_words:
                last_words.append(j)
        complete_words.append(last_words)

    #good and bad keywords list for segregating the reviews
    good_keys = ['good','gud','gd','nice','noce' 'great','grt', 'awesome', 'awsm','awesum', 'impressive','mprsv', 'imprsv', 'best', 'bst', 'appreciate', 'appriciate', 'aprciate', 'helpfull', 'hlpful', 'helpful', 'easy', 'esy', 'excellent', 'xcllent', 'excelnt', 'excellnt', 'exclnt', 'happy', 'hppy', 'hpy', 'hppy', 'hpyy','noce', 'solved', 'smooth', 'smth', 'smoth', 'smootth',  'enjoy', 'enjy', 'love', 'creative', 'luv', 'wow', 'woww', 'wowww', 'super', 'superrrr' , 'fast', 'convenient', 'marvelous', 'marvlus', 'marvels']
    bad_keys =['worst', 'wrst', 'horrible', 'poor', 'useless', 'waste', 'sham', 'fake', 'problem','problematic','prblm', 'prblmatc','problmatic','prblms', 'problems' ,'false', 'bakwas','bakwass','bakwaas','bkwas', 'bakwaass', 'broke', 'brk','brok', 'frndly', 'friendly', 'friendlly', "don't","dn't", 'slow', 'down', 'dwn', 'bug', 'bugs', 'repair' ,'repairing', 'trouble', 'ba', 'tried', 'unable', 'unble', 'decline','declining','declin', 'declinig', 'pathetic','pathtic', 'pthtc', 'pthtic', '', 'discusting' ,'defective', 'defect','defeat', 'defctive','dfctve', 'dfctive', 'complan', 'complne', 'complained', 'complain', 'cmpln', 'complains', 'complaineds', 'complaints', 'complnts', 'disgusting', 'disgsting', 'dsgustng','disgstng', 'scam', 'foolish', 'ganda', 'bekar', 'ghtiya', 'ghatiya', 'avoid', 'avod', 'stopped', 'stop', 'stoped', 'stopping', 'crash', 'crashing', 'crashed', 'crshd', 'crashd', 'hopeless', 'hoples', 'hopelss', 'hpls','issue', 'issues', 'issu','pachtaoge', 'pastaoge', 'cancelled','unnecessary','wasted','criminal','low','lowest','defective','defect','fault','faulty','fault','khrab','khraab', 'utterly', 'uttrly', 'utterlly', 'utrly','never','erros', 'error', 'err', 'errs', 'ers', 'worse', 'wrs', 'wors', 'confuse', 'confus', 'cnfus', 'hanged', 'hnged', 'hangedd', 'hang' ,'hanging', 'freez', 'freezing', 'rupish', 'rubish', 'wastage', 'wstg', 'wastg', 'hell', 'hel', 'helll', 'delay', 'dissatisfaction', 'disstfction', 'harrasment', 'harsment', 'harrasmnt', 'harsmnt', 'idiot', 'stupid', 'junk', 'ghatiha','cheat', 'cheater', 'cheaters', 'useless','uslss', 'uselss', 'usless', 'uselesss', 'looting','werst', 'loss', 'spoiled', 'spoil', 'spoiling', 'gaadu', 'jaato', 'replaced', 'replacement', 'replacmnt', 'replace', 'rplce', 'replcmnt', 'rudely', 'rudly', 'negative', '-ve', 'ngtive', 'ngtv', 'trouble', 'trble', 'truble', 'fad', 'hate','glitch', 'glitchyil', 'failure', 'failed', 'lazy', 'lzy']


    #generating the good_score and bad_score array
    #good_score implies how many good words we have in a single comment or review
    #bad_score implies how many bad words we have in a single comment or review
    good_score = [];
    bad_score = [];
    good = 0;
    bad = 0;
    for i in complete_words:
      for j in i:
        if j in  good_keys:
          good = good+1;
        elif j in bad_keys:
          bad = bad+1;

      good_score.append(good)
      bad_score.append(bad)
      good = 0;
      bad = 0;

    #rating array
    rating_array = np.array(havells_android_reviews_copy['score']).tolist()

    # generating the good_array, bad_array, neutral_array
    # good_array implies that it is a good review or not, if it is good put 1 otherwise 0
    # bad_array implies that it is a bad review or not, if it is bad put 1 otherwise 0
    size = len(rating_array)
    good = 0;
    bad = 0;
    neutral = 0;
    good_array = [];
    bad_array = [];
    neutral_array = [];
    good_require = 0;
    bad_require = 0;

    for i in range(0, size):
      if(good_score[i] > good_require):
        if(rating_array[i] >= 3):
          good = 1;
          bad = 0;
          neutral = 0;
        elif(rating_array[i]<3):
          good = 0;
          bad = 0;
          neutral = 1;
      elif(bad_score[i] > bad_require):
        if(rating_array[i] < 3):
          good = 0;
          bad = 1;
          neutral = 0;
        elif(rating_array[i] >= 3):
          good = 1;
          bad = 0;
          neutral = 0;
      elif(rating_array[i] >= 3):
        good = 1;
        bad = 0;
        neutral = 0;
      elif(rating_array[i] < 3):
        good = 0;
        bad = 1;
        neutral = 0;
      else:
        good = 0;
        bad = 0;
        neutral = 0;
      good_array.append(good)
      bad_array.append(bad)
      neutral_array.append(neutral)


    # creating the services, ui, iot, solar keywords for segregating the reviews based on these keywords
    services_key = ['शिकायत','समस्या','सर्विस', 'visit', 'palce','place', 'person', 'communication','employee','employees','badtameej','declining','write','wrote','install','span','generated','technisian','visited','visiting','behavior','agency','declining','staffs','booking','rating', 'stopped' , 'charged','criminal', 'waiting','lodge','appointment','irresponsible','executives','fellow','replacement','replacementthen','expertise','booked','services','support','register','answering','rudely','level','ground','mentellay','harassed','talking','feedback','lodging','technician','complaint','status','engineer','poor','ticket','technicians','action', 'untrained', 'serial', 'providers', 'incompetent', 'cleaning', 'customer', 'care', 'number', 'toll', 'support', 'rectification', 'rectification', 'raising', 'req','service', 'services', 'srvcs', 'raised', 'request', 'attends', 'calling', 'call', 'called', 'maintance', 'warrantyguaranteecustomer' ,'warranty', 'installation', 'centre', 'repair','repaired',  ]
    ui_key = ['design', 'user', 'friendly', 'lengthy', 'flow', 'bugs', 'bug', 'hang', 'hanging', 'hanged', 'freeze', 'mobile', 'application', 'homepage' 'redirects', 'uploading', 'image', 'images', 'img', 'functioning', 'barcode', 'features', 'stopped', 'wifi', 'scan', 'qr','code', 'app', 'ui', 'UI', 'uI', 'Ui', 'interface', 'interphase','feedback' ,'otp', 'update', 'updated', ]
    iot_key = ['functioning', 'barcode', 'stopped' ,'lloyd', 'serial','connecting','wifi', 'scan', 'qr','code', 'motor', ]
    solar_key = [  'inverter', 'batteries', 'solar', 'manufacturing', 'manufacturer', 'power', 'powers', 'energy', 'enrgy', 'generation', 'generating', 'generated']


    #generating the services_score, ui_score, iot_score, solar_score array
    #services_score implies how many services words we have in a single comment or review
    #ui_score implies how many ui/app words we have in a single comment or review
    #iot_score implies how many iot words we have in a single comment or review
    #solar_score implies how many solar words we have in a single comment or review
    services_score = []
    ui_score = []
    iot_score = []
    solar_score = []
    services = 0;
    ui = 0;
    iot = 0;
    solar = 0;
    for i in complete_words:
        services = 0;
        ui = 0;
        iot = 0;
        solar = 0;
        for j in i:
            if j in services_key:
                services = services+1;
            if j in ui_key:
                ui = ui+1;
            if j in iot_key:
                iot = iot+1;
            if j in solar_key:
                solar = solar+1;
        services_score.append(services)
        ui_score.append(ui)
        iot_score.append(iot)
        solar_score.append(solar)


    # generating the services_array, ui_array, iot_array and solar_array
    # services_array implies that it is a service review or not, if it is a service review put 1 otherwise 0
    # ui_array implies that it is a ui/app review or not, if it is a ui/app review put 1 otherwise 0
    # iot_array implies that it is a iot review or not, if it is a iot review put 1 otherwise 0
    # solar_array implies that it is a solar review or not, if it is solar review put 1 otherwise 0
    services_array = []
    ui_array = []
    iot_array = []
    solar_array = []
    size = len(services_score)

    for i in range(0,size):
        if(services_score[i] > 0):
            services_array.append(1)
        else:
            services_array.append(0)
        if(ui_score[i] > 0):
            ui_array.append(1)
        else:
            ui_array.append(0)
        if(iot_score[i] > 0):
            iot_array.append(1)
        else:
            iot_array.append(0)
        if(solar_score[i] > 0):
            solar_array.append(1)
        else:
            solar_array.append(0)

    #sending the data
    data_4 = {
          'good_array' : good_array,
          'bad_array' : bad_array,
          'neutral_array' : neutral_array,
          'services_array' : services_array,
          'ui_array' : ui_array,
          'iot_array' : iot_array,
          'solar_array' : solar_array,
          'good_score' : good_score,
          'bad_score' : bad_score,
          'services_score' : services_score,
          'ui_score' : ui_score,
          'iot_score' : iot_score,
          'solar_score' : solar_score,
          'rating_array' : rating_array,
          'latest_comment' : content_array[0],
          'content_array' : content_array,
          'review_id' : reviewId_array,
          'user_name' : userName_array,
          'user_image' : userImage_array,
          'thumbs_up_count' : thumbsUpCount_array,
          'review_created_version' : reviewCreatedVersion_array,
          'at' : at_array,
          'reply_content' : replyContent_array,
          'replied_at' : repliedAt_array
        }

    return jsonify(data_4)

if __name__ == '__main__':
   app.run(debug=False)
