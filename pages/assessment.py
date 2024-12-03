import streamlit as st
from datetime import datetime
import requests
import base64
import json
import time
import numpy as np
import os
import wave
import contextlib
import json
import string
import threading
import utils
import sys
import azure.cognitiveservices.speech as speechsdk

if 'results' not in st.session_state:
    st.session_state.page = 'welcome'

# Initialize session state variables
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'recording_data' not in st.session_state:
    st.session_state.recording_data = []

def start_recording():
    st.session_state.is_recording=True
    print("Recording started")
    
def stop_recording():
    st.session_state.is_recording=False
    print("Recording stopped")

def audio_callback(indata, frames, time, status):
    if st.session_state.is_recording:
        st.session_state.recording_data.extend(indata[:, 0])

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

    import difflib
    import json

    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # provide a WAV file as an example. Replace it with your own.
    audio_config = speechsdk.audio.AudioConfig(filename="audio.wav")

    reference_text = "फ्लिपकार्ट फाउंडेशन को 2022 में शुरू किया गया था ताकि फ्लिपकार्ट समूह की ग्रास-रूट लेवल की पहल को समाज के वंचित वर्गों के लिए जारी रखा जा सके। यह देश के विभिन्न राज्यों में ऑन-ग्राउंड संचालन को सक्रिय करता है, फाउंडेशन ने कई एनजीओके साथ सहयोग किया है जो प्रभावशाली कार्य कर रहे हैं। विकलांग बच्चों को समर्थन देने से लेकर वंचित समुदायों की महिलाओं को सशक्त बनाने तक, ये स्टार्टअप भारत में हजारों लोगों के जीवन को बदल रहे हैं। यहां कुछ उपयोगी सहयोगों पर एक नज़र डालें, जिन्होंने कई लोगों के जीवन को बदलने वाले क्षण लाए हैं।"

    # create pronunciation assessment config, set grading system, granularity and if enable miscue based on your requirement.
    enable_miscue = True
    enable_prosody_assessment = True
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text=reference_text,
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
        enable_miscue=enable_miscue)
    if enable_prosody_assessment:
        pronunciation_config.enable_prosody_assessment()

    # Creates a speech recognizer using a file as audio input.
    language = 'hi-IN'
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=language, audio_config=audio_config)
    # apply pronunciation assessment config to speech recognizer
    pronunciation_config.apply_to(speech_recognizer)

    done = False
    recognized_words = []
    fluency_scores = []
    prosody_scores = []
    durations = []

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def recognized(evt: speechsdk.SpeechRecognitionEventArgs):
        print('pronunciation assessment for: {}'.format(evt.result.text))
        pronunciation_result = speechsdk.PronunciationAssessmentResult(evt.result)
        print('    Accuracy score: {}, pronunciation score: {}, completeness score : {}, fluency score: {}, prosody score: {}'.format(
            pronunciation_result.accuracy_score, pronunciation_result.pronunciation_score,
            pronunciation_result.completeness_score, pronunciation_result.fluency_score, pronunciation_result.prosody_score
        ))
        nonlocal recognized_words, fluency_scores, durations, prosody_scores
        recognized_words += pronunciation_result.words
        fluency_scores.append(pronunciation_result.fluency_score)
        prosody_scores.append(pronunciation_result.prosody_score)
        json_result = evt.result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
        jo = json.loads(json_result)
        nb = jo['NBest'][0]
        durations.append(sum([int(w['Duration']) for w in nb['Words']]))

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(recognized)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous pronunciation assessment
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()

    # we need to convert the reference text to lower case, and split to words, then remove the punctuations.
    if language == 'zh-CN':
        # Use jieba package to split words for Chinese
        import jieba
        import zhon.hanzi
        jieba.suggest_freq([x.word for x in recognized_words], True)
        reference_words = [w for w in jieba.cut(reference_text) if w not in zhon.hanzi.punctuation]
    else:
        reference_words = [w.strip(string.punctuation) for w in reference_text.lower().split()]

    # For continuous pronunciation assessment mode, the service won't return the words with `Insertion` or `Omission`
    # even if miscue is enabled.
    # We need to compare with the reference text after received all recognized words to get these error words.
    if enable_miscue:
        diff = difflib.SequenceMatcher(None, reference_words, [x.word.lower() for x in recognized_words])
        final_words = []
        for tag, i1, i2, j1, j2 in diff.get_opcodes():
            if tag in ['insert', 'replace']:
                for word in recognized_words[j1:j2]:
                    if word.error_type == 'None':
                        word._error_type = 'Insertion'
                    final_words.append(word)
            if tag in ['delete', 'replace']:
                for word_text in reference_words[i1:i2]:
                    word = speechsdk.PronunciationAssessmentWordResult({
                        'Word': word_text,
                        'PronunciationAssessment': {
                            'ErrorType': 'Omission',
                        }
                    })
                    final_words.append(word)
            if tag == 'equal':
                final_words += recognized_words[j1:j2]
    else:
        final_words = recognized_words

    # We can calculate whole accuracy by averaging
    final_accuracy_scores = []
    for word in final_words:
        if word.error_type == 'Insertion':
            continue
        else:
            final_accuracy_scores.append(word.accuracy_score)
    accuracy_score = sum(final_accuracy_scores) / len(final_accuracy_scores)
    # Re-calculate fluency score
    fluency_score = sum([x * y for (x, y) in zip(fluency_scores, durations)]) / sum(durations)
    # Calculate whole completeness score
    completeness_score = len([w for w in recognized_words if w.error_type == "None"]) / len(reference_words) * 100
    completeness_score = completeness_score if completeness_score <= 100 else 100
    # Re-calculate prosody score
    prosody_score = sum(prosody_scores) / len(prosody_scores)
    pron_score = accuracy_score * 0.4 + prosody_score * 0.2 + fluency_score * 0.2 + completeness_score * 0.2
    result = {
                    'Paragraph pronunciation score': pron_score,
                    'Accuracy Score': accuracy_score,
                    'Completeness Score': completeness_score,
                    'Fluency Score': fluency_score,
                    'Prosody Score': prosody_score
                }
    if 'results' not in st.session_state:
        st.session_state.results = []
    st.session_state.results.append(result)

    print('    Paragraph pronunciation score: {}, accuracy score: {}, completeness score: {}, fluency score: {}, prosody score: {}'.format(
        pron_score, accuracy_score, completeness_score, fluency_score, prosody_score
    ))

    for idx, word in enumerate(final_words):
        print('    {}: word: {}\taccuracy score: {}\terror type: {};'.format(
            idx + 1, word.word, word.accuracy_score, word.error_type
        ))

def show_assessment_page():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Your Speaking Task")
        st.write("Please speak the text given in the white box.")
        
        # Audio recording controls
        if 'is_recording' not in st.session_state:
            st.session_state.is_recording = False

        if st.session_state.is_recording:
            if st.button("End Assessment"):
                stop_recording()
                # Save recording data
                # Get the duration of the audio file
                audio_file_path = 'audio.wav'
                duration = 0
                with contextlib.closing(wave.open(audio_file_path, 'r')) as f:
                    frames = f.getnframes()
                    rate = f.getframerate()
                    duration = frames / float(rate)
                    print(f"Duration: {duration} seconds")
                startAssessment()
                recording = {
                    'Timestamp': datetime.now(),
                    'Text': "फ्लिपकार्ट फाउंडेशन को 2022 में शुरू किया गया था ताकि फ्लिपकार्ट समूह की ग्रास-रूट लेवल की पहल को समाज के वंचित वर्गों के लिए जारी रखा जा सके। यह देश के विभिन्न राज्यों में ऑन-ग्राउंड संचालन को सक्रिय करता है, फाउंडेशन ने कई एनजीओके साथ सहयोग किया है जो प्रभावशाली कार्य कर रहे हैं। विकलांग बच्चों को समर्थन देने से लेकर वंचित समुदायों की महिलाओं को सशक्त बनाने तक, ये स्टार्टअप भारत में हजारों लोगों के जीवन को बदल रहे हैं। यहां कुछ उपयोगी सहयोगों पर एक नज़र डालें, जिन्होंने कई लोगों के जीवन को बदलने वाले क्षण लाए हैं।",
                    'Duration': f'{int(duration // 60)}:{int(duration % 60):02d}'
                }
                if 'recordings' not in st.session_state:
                    st.session_state.recordings = []
                st.session_state.recordings.append(recording)
                st.session_state.page = 'history'
        else:
            if st.button("Start Assessment"):
                start_recording()
                st.success("Recording in progress...")
    
    with col2:
        st.markdown("""
        <div style='background-color:#f0f2f6; padding: 20px; border-radius: 10px; color: black;'>
            <h3 style='color: black;>The Text</h3>
            <p>फ्लिपकार्ट फाउंडेशन को 2022 में शुरू किया गया था ताकि फ्लिपकार्ट समूह की ग्रास-रूट लेवल की पहल को समाज के वंचित वर्गों के लिए जारी रखा जा सके। यह देश के विभिन्न राज्यों में ऑन-ग्राउंड संचालन को सक्रिय करता है, फाउंडेशन ने कई एनजीओके साथ सहयोग किया है जो प्रभावशाली कार्य कर रहे हैं। विकलांग बच्चों को समर्थन देने से लेकर वंचित समुदायों की महिलाओं को सशक्त बनाने तक, ये स्टार्टअप भारत में हजारों लोगों के जीवन को बदल रहे हैं। यहां कुछ उपयोगी सहयोगों पर एक नज़र डालें, जिन्होंने कई लोगों के जीवन को बदलने वाले क्षण लाए हैं।</p>
        </div>
        """, unsafe_allow_html=True)

# Display the assessment page
show_assessment_page()