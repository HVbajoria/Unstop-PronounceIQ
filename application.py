import requests
import base64
import json
import time
import random
import azure.cognitiveservices.speech as speechsdk

from flask import Flask, jsonify, render_template, request, make_response

app = Flask(__name__)

subscription_key = '8oAh7EnM2XxkSJE2UyijMhk8mcJX6vLiTfJZs0Y3hUx8d4D9LmmoJQQJ99ALACHYHv6XJ3w3AAAAACOGPxr4'
region = "eastus2"
language = "hi-IN"
voice = "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/readalong")
def readalong():
    return render_template("readalong.html")

@app.route("/gettoken", methods=["POST"])
def gettoken():
    fetch_token_url = 'https://%s.api.cognitive.microsoft.com/sts/v1.0/issueToken' %region
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = response.text
    return jsonify({"at":access_token})


@app.route("/gettonguetwister", methods=["POST"])
def gettonguetwister():
    tonguetwisters = ["क्या ऑर्डर से संबंधित कोई प्रश्न है? फ़्लिपकार्ट से संपर्क करने का यह तरीका अपनाएं । क्या आप हमसे बात करना चाहते हैं या अपने हाल ही में किए गए ऑर्डर के बारे में कोई समस्या बताना चाहते हैं? 'My Orders' स्क्रीन के 'Need Help' पर टैप/क्लिक करें (नीचे दिया गया स्क्रीनशॉट देखें) । इस सुविधा का उपयोग करने के लिए आपको अपने पंजीकृत ईमेल/मोबाइल फ़ोन नंबर की मदद से फ़्लिपकार्ट में लॉग इन करना होगा।",
            "“प्रिय फ्लिपकार्ट ग्राहक, बधाई हो! आप जीते हैं …” – इस तरह का एक जाली मैसेज काफी लुभावना दिखाई पड़ सकता है, पर वास्तव में यह एक झांसा होता है। ई-कॉमर्स के काफी तेजी से लोकप्रिय होने के साथ ही, धोखेबाज लोग भी उपभोक्ताओं को फांसकर आसानी से कमाई करने के तरीके ढूंढते रहते हैं और वह भी फ्लिपकार्ट के भरोसेमंद नाम को इस्तेमाल करके। पर आप चिंता न करें! क्लिक करने से बचें। विवरण देने से बचें। फॉरवर्ड करने से बचें। यदि आप किसी जाली मैसेज या कॉल के जरिए दिए गए प्रलोभन का विरोध करते हैं, तो धोखाधड़ी करने वाले लोग आपको कभी फांस नहीं पाएंगे।",
            "वे आपके संवेदनशील डेटा हासिल करना चाहते हैं: जालसाज लोग अपने जाली मैसेज के जरिए आपसे ज्यादा से ज्यादा निजी और वित्तीय जानकारी हासिल करना चाहते हैं। उनके लिंक आपको किसी नकली फ्लिपकार्ट वेबसाइट पर ले जा सकते हैं, जिनमें ऐसे फॉर्म मौजूद रहते हैं, जिनके जरिए आपका डेटा हासिल कर लिया जाता है। यहां तक कि आपसे कोई संदेहास्पद ट्रांजैक्शन भी करवा सकते हैं और उनके लिंक आपके डिवाइस को इंफेक्टेड करने का मार्ग भी हो सकते हैं।",
            "आपको एसएमएस के जरिए जाली मैसेज मिल सकता है, साथ ही ये आपको व्हाट्सऐप, फेसबुक मेसेंजर, टेलीग्राम या अन्य सोशल मेसैजिंग प्लैट्फॉर्म पर भी मिल सकते हैं। व्हाट्सऐप या सोशल मीडिया प्लैटफॉर्म की स्थिति में, स्कैमर नकली इंवॉइस की कॉपी भी अपलोड कर सकता है या असली दिखने वाले ब्रांडिंग के साथ मेसैज भी भेज सकता है, जो बिल्कुल असली दिखाई पड़ते हैं। प्रमाण के तौर पर वे नकली फ्लिपकार्ट आइडी भी पेश कर सकते हैं।",
            "स्कैमर आपसे किसी अज्ञात नम्बर से संपर्क कर सकता है और असली लगने के लिए, फ्लिपकार्ट या इसकी ग्रुप कंपनियों, जैसे कि मिंत्रा, जबोंग, जीवीस या फ़ोनपे का प्रतिनिधि होने का ढोंग कर सकते हैं। यहां तक कि वे आपसे अंग्रेजी या हिंदी में या आपकी पसंद की क्षेत्रीय भाषा में बातचीत कर सकते हैं। उनकी बातचीत किसी शानदार डील के बारे में हो सकती है जिसके लिए आप योग्यता रखते हों या कोई जरूरी अकाउंट कार्यवाही के बारे में हो, जो आपको करने को कहा जा सकता है।",
            "फ्लिपकार्ट फाउंडेशन को 2022 में शुरू किया गया था ताकि फ्लिपकार्ट समूह की ग्रास-रूट लेवल की पहल को समाज के वंचित वर्गों के लिए जारी रखा जा सके। यह देश के विभिन्न राज्यों में ऑन-ग्राउंड संचालन को सक्रिय करता है, फाउंडेशन ने कई एनजीओके साथ सहयोग किया है जो प्रभावशाली कार्य कर रहे हैं। विकलांग बच्चों को समर्थन देने से लेकर वंचित समुदायों की महिलाओं को सशक्त बनाने तक, ये स्टार्टअप भारत में हजारों लोगों के जीवन को बदल रहे हैं। यहां कुछ उपयोगी सहयोगों पर एक नज़र डालें, जिन्होंने कई लोगों के जीवन को बदलने वाले क्षण लाए हैं।",
            "फ्लिपकार्ट एक्सिस बैंक क्रेडिट कार्ड सुनिश्चित करता है कि फ्लिपकार्ट के ग्राहकों को सर्वश्रेष्ठ-इन-क्लास लाभ मिले। और कार्ड का असीमित कैशबैक वादा सुनिश्चित करता है कि कैशबैक पर कोई ऊपरी सीमा नहीं है सभी खर्चों पर*, ऑनलाइन और ऑफलाइन — यह वास्तव में असीमित है!",
            "फ्लिपकार्ट एक्सिस बैंक क्रेडिट कार्ड में एक नई सुविधा दी गई है, कार्ड कंसोल ग्राहकों के लिए अपने कार्ड से संबंधित जानकारी को सीधे फ्लिपकार्ट ऐप से देखने के लिए वन-स्टॉप कॉकपिट दृश्य है, जिससे आपके कार्ड के महत्वपूर्ण पहलुओं को प्रबंधित करना आसान हो जाता है।"]
    
    return jsonify({"tt":random.choice(tonguetwisters)})

@app.route("/getstory", methods=["POST"])
def getstory():
    id = int(request.form.get("id"))
    stories = [["Read aloud the sentences on the screen.",
        "We will follow along your speech and help you learn speak English.",
        "Good luck for your reading lesson!"],
        ["The Hare and the Tortoise",
        "Once upon a time, a Hare was making fun of the Tortoise for being so slow.",
        "\"Do you ever get anywhere?\" he asked with a mocking laugh.",
        "\"Yes,\" replied the Tortoise, \"and I get there sooner than you think. Let us run a race.\"",
        "The Hare was amused at the idea of running a race with the Tortoise, but agreed anyway.",
        "So the Fox, who had consented to act as judge, marked the distance and started the runners off.",
        "The Hare was soon far out of sight, and in his overconfidence,",
        "he lay down beside the course to take a nap until the Tortoise should catch up.",
        "Meanwhile, the Tortoise kept going slowly but steadily, and, after some time, passed the place where the Hare was sleeping.",
        "The Hare slept on peacefully; and when at last he did wake up, the Tortoise was near the goal.",
        "The Hare now ran his swiftest, but he could not overtake the Tortoise in time.",
        "Slow and Steady wins the race."],
        ["The Ant and The Dove",
        "A Dove saw an Ant fall into a brook.",
        "The Ant struggled in vain to reach the bank,",
        "and in pity, the Dove dropped a blade of straw close beside it.",
        "Clinging to the straw like a shipwrecked sailor, the Ant floated safely to shore.",
        "Soon after, the Ant saw a man getting ready to kill the Dove with a stone.",
        "Just as he cast the stone, the Ant stung the man in the heel, and he missed his aim,",
        "The startled Dove flew to safety in a distant wood and lived to see another day.",
        "A kindness is never wasted."]]
    if(id >= len(stories)):
        return jsonify({"code":201})
    else:
        return jsonify({"code":200,"storyid":id , "storynumelements":len(stories[id]),"story": stories[id]})

@app.route("/ackaud", methods=["POST"])
def ackaud():
    f = request.files['audio_data']
    reftext = request.form.get("reftext")
    #    f.save(audio)
    #print('file uploaded successfully')

    # a generator which reads audio data chunk by chunk
    # the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
    def get_chunk(audio_source, chunk_size=1024):
        while True:
            #time.sleep(chunk_size / 32000) # to simulate human speaking rate
            chunk = audio_source.read(chunk_size)
            if not chunk:
                #global uploadFinishTime
                #uploadFinishTime = time.time()
                break
            yield chunk

    # build pronunciation assessment parameters
    referenceText = reftext
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\",\"EnableMiscue\":\"True\"}" % referenceText
    pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

    # build request
    url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=%s&usePipelineVersion=0" % (region, language)
    headers = { 'Accept': 'application/json;text/xml',
                'Connection': 'Keep-Alive',
                'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
                'Ocp-Apim-Subscription-Key': subscription_key,
                'Pronunciation-Assessment': pronAssessmentParams,
                'Transfer-Encoding': 'chunked',
                'Expect': '100-continue' }

    #audioFile = open('audio.wav', 'rb')
    audioFile = f
    # send request with chunked data
    response = requests.post(url=url, data=get_chunk(audioFile), headers=headers)
    #getResponseTime = time.time()
    audioFile.close()

    #latency = getResponseTime - uploadFinishTime
    #print("Latency = %sms" % int(latency * 1000))

    return response.json()

@app.route("/gettts", methods=["POST"])
def gettts():
    reftext = request.form.get("reftext")
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice

    offsets=[]

    def wordbound(evt):
        offsets.append( evt.audio_offset / 10000)

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Subscribes to word boundary event
    # The unit of evt.audio_offset is tick (1 tick = 100 nanoseconds), divide it by 10,000 to convert to milliseconds.
    speech_synthesizer.synthesis_word_boundary.connect(wordbound)

    result = speech_synthesizer.speak_text_async(reftext).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #print("Speech synthesized for text [{}]".format(reftext))
        #print(offsets)
        audio_data = result.audio_data
        #print(audio_data)
        #print("{} bytes of audio data received.".format(len(audio_data)))
        
        response = make_response(audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
        # response.headers['reftext'] = reftext
        response.headers['offsets'] = offsets
        return response
        
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return jsonify({"success":False})

@app.route("/getttsforword", methods=["POST"])
def getttsforword():
    word = request.form.get("word")

    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voice

    # Creates a speech synthesizer with a null output stream.
    # This means the audio output data will not be written to any output channel.
    # You can just get the audio from the result.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_text_async(word).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #print("Speech synthesized for text [{}]".format(reftext))
        #print(offsets)
        audio_data = result.audio_data
        #print(audio_data)
        #print("{} bytes of audio data received.".format(len(audio_data)))
        
        response = make_response(audio_data)
        response.headers['Content-Type'] = 'audio/wav'
        response.headers['Content-Disposition'] = 'attachment; filename=sound.wav'
        # response.headers['word'] = word
        return response
        
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return jsonify({"success":False})
