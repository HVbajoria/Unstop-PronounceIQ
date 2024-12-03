def startAssessment():

    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        print("""
        Importing the Speech SDK for Python failed.
        Refer to
        https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
        installation instructions.
        """)
        sys.exit(1)


    # Set up the subscription info for the Speech Service:
    # Replace with your own subscription key and service region (e.g., "westus").
    speech_key, service_region = "EFR12ZIeNCCPgdtX256d8vRo5JM9amhgdtD6ok2ExrTx8Q97ayTwJQQJ99ALACHYHv6XJ3w3AAAAACOGb59J", "eastus2"

    # Specify the path to an audio file containing speech (mono WAV / PCM with a sampling rate of 16
    # kHz).
    weatherfilename = "audio.wav"
    weatherfilenamemp3 = "whatstheweatherlike.mp3"
    weatherfilenamemulaw = "whatstheweatherlike-mulaw.wav"
    seasonsfilename = "audio.wav"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Ask for detailed recognition result
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    print("Using audio file: ", speech_config.output_format)
    # If you also want word-level timing in the detailed recognition results, set the following.
    # Note that if you set the following, you can omit the previous line
    #   "speech_config.output_format = speechsdk.OutputFormat.Detailed",
    # since word-level timing implies detailed recognition results.
    speech_config.request_word_level_timestamps()

    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)
   
    # Creates a speech recognizer using a file as audio input, also specify the speech language
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, language="en-US", audio_config=audio_config)

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognition text as result.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))

        # Time units are in hundreds of nanoseconds (HNS), where 10000 HNS equals 1 millisecond
        print("Offset: {}".format(result.offset))
        print("Duration: {}".format(result.duration))

        # Now get the detailed recognition results from the JSON
        json_result = json.loads(result.json)

        # The first cell in the NBest list corresponds to the recognition results
        # (NOT the cell with the highest confidence number!)
        print("Detailed results - Lexical: {}".format(json_result['NBest'][0]['Lexical']))
        # ITN stands for Inverse Text Normalization
        print("Detailed results - ITN: {}".format(json_result['NBest'][0]['ITN']))
        print("Detailed results - MaskedITN: {}".format(json_result['NBest'][0]['MaskedITN']))
        print("Detailed results - Display: {}".format(json_result['NBest'][0]['Display']))

        # Print word-level timing. Time units are HNS.
        words = json_result['NBest'][0]['Words']
        print("Detailed results - Word timing:\nWord:\tOffset:\tDuration:")
        for word in words:
            print(f"{word['Word']}\t{word['Offset']}\t{word['Duration']}")

        # You can access alternative recognition results through json_result['NBest'][i], i=1,2,..

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    # </SpeechRecognitionFromFileWithDetailedRecognitionResults>


    # provide a WAV file as an example. Replace it with your own.
    audio_config = speechsdk.audio.AudioConfig(filename="audio.wav")

    reference_text = "फ्लिपकार्ट फाउंडेशन को 2022 में शुरू किया गया था ताकि फ्लिपकार्ट समूह की ग्रास-रूट लेवल की पहल को समाज के वंचित वर्गों के लिए जारी रखा जा सके। यह देश के विभिन्न राज्यों में ऑन-ग्राउंड संचालन को सक्रिय करता है, फाउंडेशन ने कई एनजीओके साथ सहयोग किया है जो प्रभावशाली कार्य कर रहे हैं। विकलांग बच्चों को समर्थन देने से लेकर वंचित समुदायों की महिलाओं को सशक्त बनाने तक, ये स्टार्टअप भारत में हजारों लोगों के जीवन को बदल रहे हैं। यहां कुछ उपयोगी सहयोगों पर एक नज़र डालें, जिन्होंने कई लोगों के जीवन को बदलने वाले क्षण लाए हैं।"
