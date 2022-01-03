import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
import urllib.request
import uuid
import time
import json
import requests
import camera, RecorD
import os
import webbrowser

mainUI = '../DL/_uiFiles/main.ui'


class InputfileDialog(QDialog):  # 파일 입력할 수 있는 Dialog
    def __init__(self, parent):
        super(InputfileDialog, self).__init__(parent)
        inputfile_ui = '../DL/_uiFiles/inputFile.ui'
        uic.loadUi(inputfile_ui, self)
        self.show()

        self.inputFile.clicked.connect(self.fileopen)
        self.input_quit.clicked.connect(self.quit_input)

    def fileopen(self):
        global filename
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.fileName.setText(filename[0])
        global filepath
        filepath = f'{filename[0]}'

    def quit_input(self):
        self.accept()


class TextDialog(QDialog):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self, parent):
        super(TextDialog, self).__init__(parent)
        text_ui = '../DL/_uiFiles/textInput.ui'
        uic.loadUi(text_ui, self)
        self.show()

        self.textCheck.clicked.connect(self.quit_text)

    def quit_text(self):
        global text_input
        text_input = self.textEdit.toPlainText()
        text_input = str(text_input)
        print(text_input)
        self.detect_lang()
        self.accept()

    def detect_lang(self):
        global lang
        client_id = "t19oy7s6k3"
        client_secret = "JXnfP1GtliSRcli5kvlT7gMiA1cIxSk0SF4NomnH"
        encQuery = urllib.parse.quote(text_input)
        data = "query=" + encQuery
        url = "https://naveropenapi.apigw.ntruss.com/langs/v1/dect"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            lang = response_body.decode('utf-8')
            lang = json.loads(lang)
            lang = lang['langCode']
            print(lang)
        else:
            print("Error Code:" + rescode)


class InputDialog(QDialog):
    def __init__(self, parent):
        super(InputDialog, self).__init__(parent)
        input_ui = '../DL/_uiFiles/input.ui'

        uic.loadUi(input_ui, self)
        self.show()

        self.textRbtn.clicked.connect(self.clicked_option_text)
        self.imageRbtn.clicked.connect(self.clicked_option_file)
        self.voiceRbtn.clicked.connect(self.clicked_option_file)
        self.cameraRbtn.clicked.connect(self.clicked_option_cam)
        self.micRbtn.clicked.connect(self.clicked_option_mic)
        self.okBtn.clicked.connect(self.clicked_okBtn)

    def clicked_okBtn(self):
        self.accept()

    def clicked_option_text(self):
        TextDialog(self)

    def clicked_option_file(self):
        InputfileDialog(self)

    def clicked_option_cam(self):
        global camFile
        camFile = camera.capture(self)
        print(camFile, 'saved')
        #       QMessageBox.about(self, "!", "사진 저장 완료")
        global filepath
        filepath = camFile

    def clicked_option_mic(self):
        app = RecorD.RecGui()
        app.mainloop()
        global filepath
        filepath = RecorD.filename
        filepath = os.path.realpath(filepath)
        print(os.path.realpath(filepath))
        filepath = os.path.realpath(filepath)
        specialChars = "\\"
        for specialChar in specialChars:
            filepath = filepath.replace(specialChar, '/')
            print(filepath)


class LangDialog(QDialog):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self, parent):

        super(LangDialog, self).__init__(parent)
        lang_ui = '../DL/_uiFiles/langselect.ui'
        uic.loadUi(lang_ui, self)
        self.show()

        self.langCheck.clicked.connect(self.quit_lang)

    def quit_lang(self):
        global mainlang
        mainlang = self.selectLang.currentText()
        if mainlang == '한국어':
            mainlang = 'ko'
            print(mainlang)
        elif mainlang == '영어':
            mainlang = 'en'
            print(mainlang)
        elif mainlang == '일본어':
            mainlang = 'ja'
            print(mainlang)
        elif mainlang == '중국어-간체':
            mainlang = 'zh-CN'
            print(mainlang)
        elif mainlang == '중국어-번체':
            mainlang = 'zh-TW'
            print(mainlang)
        elif mainlang == '베트남어':
            mainlang = 'vi'
            print(mainlang)
        elif mainlang == '인도네시아어':
            mainlang = 'id'
            print(mainlang)
        elif mainlang == '태국어':
            mainlang = 'th'
            print(mainlang)
        elif mainlang == '독일어':
            mainlang = 'de'
            print(mainlang)
        elif mainlang == '러시아어':
            mainlang = 'ru'
            print(mainlang)
        elif mainlang == '스페인어':
            mainlang = 'es'
            print(mainlang)
        elif mainlang == '이탈리아어':
            mainlang = 'it'
            print(mainlang)
        elif mainlang == '프랑스어':
            mainlang = 'fr'
            print(mainlang)

        self.accept()


class LangDialog_stt(QDialog):  # 텍스트 입력할 수 있는 Dialog
    def __init__(self, parent):

        super(LangDialog_stt, self).__init__(parent)
        lang_stt = '../DL/_uiFiles/langselect_stt.ui'
        uic.loadUi(lang_stt, self)
        self.show()

        self.langCheck.clicked.connect(self.quit_lang)

    def quit_lang(self):
        global mainlang
        mainlang = self.selectLang.currentText()
        if mainlang == '한국어':
            mainlang = 'Kor'
            print(mainlang)
        elif mainlang == '영어':
            mainlang = 'Eng'
            print(mainlang)
        elif mainlang == '일본어':
            mainlang = 'Jpn'
            print(mainlang)
        elif mainlang == '중국어':
            mainlang = 'Chn'
            print(mainlang)

        self.accept()


class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(mainUI, self)

        self.inputBtn.clicked.connect(self.inputBtn_clicked)
        self.translationBtn.clicked.connect(self.translationBtn_clicked)

        self.ttsBtn.clicked.connect(self.ttsBtn_clicked)
        self.sttBtn.clicked.connect(self.sttBtn_clicked)
        self.ocrBtn.clicked.connect(self.ocrBtn_clicked)
        self.objBtn.clicked.connect(self.objBtn_clicked)
        self.faceBtn.clicked.connect(self.faceBtn_clicked)

        self.connectBtn.clicked.connect(self.connect)
        self.saveBtn.clicked.connect(self.save)
        self.clearBtn.clicked.connect(self.clear)
        self.update()

    def inputBtn_clicked(self):
        inp = InputDialog(self)
        inp.exec_()
        try:
            self.textview.setText(text_input)
            self.imageview.setPixmap(QPixmap(filepath))
            self.fileview.setText(filepath)
        except:
            pass

    def connect(self):
        global text_input, lang, mainlang, filepath
        next = QLabel('  ➜')
        next.setMaximumWidth(250)
        next.setStyleSheet('font: 50pt "이순신 돋움체 M";color:#f9ca24')
        filepath = '../DL/ouput.mp3'
        self.aiSelect.addWidget(next)
        try:
            text_input = self.output.toPlainText()
            self.detect_lang()
        except:
            pass

    def detect_lang(self):
        global lang
        client_id = "t19oy7s6k3"
        client_secret = "JXnfP1GtliSRcli5kvlT7gMiA1cIxSk0SF4NomnH"
        encQuery = urllib.parse.quote(text_input)
        data = "query=" + encQuery
        url = "https://naveropenapi.apigw.ntruss.com/langs/v1/dect"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            lang = response_body.decode('utf-8')
            lang = json.loads(lang)
            lang = lang['langCode']
            print(lang)
        else:
            print("Error Code:" + rescode)

    def save(self):
        i = self.aiSelect.count()
        ai = self.aiSelect.itemAt(i - 1).widget().text()
        print(ai)

        if (ai == 'Translation') or (ai == 'STT') or (ai == 'Object Detection') or (ai == 'OCR'):
            fname = QFileDialog.getSaveFileName(self)
            if fname[0]:
                data = self.output.toPlainText()

                with open(f'{fname[0]}.txt', 'w', encoding='UTF8') as f:
                    f.write(data)

                print("save {}!!".format(fname[0]))
        if (ai == 'TTS'):
            fname = QFileDialog.getSaveFileName(self)
            if fname[0]:
                f = open('output.mp3', 'rb')
                data = f.read()  # bytes
                f.close()

                with open(f'{fname[0]}.mp3', "wb") as f:
                    f.write(data)
                print("save {}!!".format(fname[0]))

    def clear(self):
        global text_input, filepath
        text_input = ''
        filepath = ''
        for i in reversed(range(self.aiSelect.count())):
            self.aiSelect.itemAt(i).widget().setParent(None)
        self.output.clear()
        self.textview.clear()
        self.imageview.clear()
        self.fileview.clear()

    def translationBtn_clicked(self):  # Translation
        btnTrans = QPushButton("Translation")
        btnTrans.setMaximumWidth(250)
        btnTrans.setMinimumHeight(250)
        self.aiSelect.addWidget(btnTrans)

        btnTrans.setStyleSheet(
            '''
            QPushButton{

            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            border-image:url("../DL/image/Translation.png");
            background-color: transparent;
            color: rgb(0,0,0);
            text-align: bottom;
            }
            QPushButton:hover{
            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            background-color: #535c68;
            color: rgb(255, 255, 255);
            }
            QPushButton:pressed{
            background-color: rgb(255, 255, 255);
                border-style: inset;
            color: rgb(0,0,0);
            }
            ''')
        btnTrans.clicked.connect(lambda: self.translation())
        LangDialog(self)

    def translation(self):
        global lang, mainlang

        client_id = "t19oy7s6k3"
        client_secret = "JXnfP1GtliSRcli5kvlT7gMiA1cIxSk0SF4NomnH"
        encText = urllib.parse.quote(text_input)
        data = "source=" + lang + "&target=" + mainlang + "&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            trans_res = response_body.decode('utf-8')
            trans_res = json.loads(trans_res)
            trans_res = trans_res['message']['result']['translatedText']

            self.output.setText(trans_res)
            print(trans_res)

        else:
            print("Error Code:" + rescode)

    def ttsBtn_clicked(self):  # TTS
        btnTTS = QPushButton("TTS")
        btnTTS.setMaximumWidth(250)
        btnTTS.setMinimumHeight(250)
        self.aiSelect.addWidget(btnTTS)

        btnTTS.setStyleSheet(
            '''
            QPushButton{
            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            border-image:url("../DL/image/tts.png");
            background-color: transparent;
            color: rgb(0,0,0);
            text-align: bottom;
            }
            QPushButton:hover{
            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            background-color: #535c68;
            color: rgb(255, 255, 255);
            }
            QPushButton:pressed{
            background-color: rgb(255, 255, 255);
                border-style: inset;
            color: rgb(0,0,0);
            }
            ''')
        btnTTS.clicked.connect(lambda: self.tts())

    def tts(self):
        global lang

        if lang == 'ko':
            voice = 'nara'
        elif lang == 'en':
            voice = 'clara'
        elif lang == 'ja':
            voice = 'nnaomi'

        client_id = "t19oy7s6k3"
        client_secret = "JXnfP1GtliSRcli5kvlT7gMiA1cIxSk0SF4NomnH"
        encText = urllib.parse.quote(text_input)
        data = "speaker=" + voice + "&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            with open('output.mp3', 'wb') as f:
                f.write(response_body)
            webbrowser.open("output.mp3")
        else:
            print("Error Code:" + rescode)

    def sttBtn_clicked(self):  # STT
        btnSTT = QPushButton("STT")
        btnSTT.setMaximumWidth(250)
        btnSTT.setMinimumHeight(250)
        self.aiSelect.addWidget(btnSTT)
        btnSTT.setStyleSheet(
            '''
            QPushButton{

            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            border-image:url("../DL/image/stt.png");
            background-color: transparent;
            color: rgb(0,0,0);
            text-align: bottom;
            }
            QPushButton:hover{
            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            background-color: #535c68;
            color: rgb(255, 255, 255);
            }
            QPushButton:pressed{
            background-color: rgb(255, 255, 255);
                border-style: inset;
            color: rgb(0,0,0);
            }
            ''')
        btnSTT.clicked.connect(lambda: self.stt())
        LangDialog_stt(self)

    def stt(self):
        global stt_res, mainlang, filepath
        lang = mainlang
        client_id = "t19oy7s6k3"
        client_secret = "JXnfP1GtliSRcli5kvlT7gMiA1cIxSk0SF4NomnH"
        url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
        data = open(filepath, 'rb')
        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(url, data=data, headers=headers)
        rescode = response.status_code
        if (rescode == 200):
            stt_res = json.loads(response.text)
            stt_res = stt_res['text']
            self.output.setText(stt_res)
        else:
            print("Error : " + response.text)

    def ocrBtn_clicked(self):  # OCR
        btnOCR = QPushButton("OCR")
        btnOCR.setMaximumWidth(250)
        btnOCR.setMinimumHeight(250)
        self.aiSelect.addWidget(btnOCR)
        btnOCR.setStyleSheet(
            '''
            QPushButton{

            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            border-image:url("../DL/image/ocr.png");
            background-color: transparent;
            color: rgb(0,0,0);
            text-align: bottom;
            }
            QPushButton:hover{
            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            background-color: #535c68;
            color: rgb(255, 255, 255);
            }
            QPushButton:pressed{
            background-color: rgb(255, 255, 255);
                border-style: inset;
            color: rgb(0,0,0);
            }
            ''')
        btnOCR.clicked.connect(lambda: outputOCR())
        api_url = 'https://fac7884071c64544a83b0b6f52a7fe8b.apigw.ntruss.com/custom/v1/9848/78921cb5cc3ef08ee9dd5d3067ebad142e0cacf32ed977945b8094a9e241e027/general'
        secret_key = 'VG1UZHdhektyZEVOTktiSE1tbkZydVRLSlBBcGJCZXU='
        image_file = filepath
        request_json = {
            'images': [
                {
                    'format': 'jpg',
                    'name': 'demo'
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }
        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = [
            ('file', open(image_file, 'rb'))
        ]
        headers = {
            'X-OCR-SECRET': secret_key
        }
        response = requests.request("POST", api_url, headers=headers, data=payload, files=files)

        ocr_res = json.loads(response.text)
        data = ocr_res['images'][0]['fields']

        printText = ' '.join([_['inferText'] for _ in data])
        print(printText)

        def outputOCR():
            self.output.setText(printText)

        return 0

    def objBtn_clicked(self):  # Object Detection
        btnObj = QPushButton("Object Detection")
        btnObj.setMaximumWidth(250)
        btnObj.setMinimumHeight(250)
        self.aiSelect.addWidget(btnObj)
        btnObj.setStyleSheet(
            '''
            QPushButton{
            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            border-image:url("../DL/image/obj.png");
            background-color: transparent;
            color: rgb(0,0,0);
            text-align: bottom;
            }
            QPushButton:hover{
            font: 12pt "이순신 돋움체 M";
            border-radius: 20px;
            background-color: #535c68;
            color: rgb(255, 255, 255);
            }
            QPushButton:pressed{
            background-color: rgb(255, 255, 255);
                border-style: inset;
            color: rgb(0,0,0);
            }
            ''')
        btnObj.clicked.connect(lambda: outputObj())
        client_id = "t19oy7s6k3"
        client_secret = "JXnfP1GtliSRcli5kvlT7gMiA1cIxSk0SF4NomnH"
        url = "https://naveropenapi.apigw.ntruss.com/vision-obj/v1/detect"
        files = {'image': open(filepath, 'rb')}
        headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret}
        response = requests.post(url, files=files, headers=headers)
        rescode = response.status_code
        if (rescode == 200):
            obj_res = json.loads(response.text)
            obj_res = obj_res['predictions'][0]['detection_names']
        else:
            print("Error Code:" + rescode)

        def outputObj():
            for i in obj_res:
                self.output.append(i)

        return 0

    def faceBtn_clicked(self):
        btnFace = QPushButton("Celebrity Face Recognition")
        btnFace.setMaximumWidth(250)
        btnFace.setMinimumHeight(250)
        self.aiSelect.addWidget(btnFace)
        btnFace.setStyleSheet(
            '''
            QPushButton{
            font: 10pt "이순신 돋움체 M";
            border-radius: 20px;
            border-image:url("../DL/image/celebrity.png");
            background-color: transparent;
            color: rgb(0,0,0);
            text-align: bottom;
            }
            QPushButton:hover{
            font: 10pt "이순신 돋움체 M";
            border-radius: 20px;
            background-color: #535c68;
            color: rgb(255, 255, 255);
            }
            QPushButton:pressed{
            background-color: rgb(255, 255, 255);
                border-style: inset;
            color: rgb(0,0,0);
            }
            ''')
        btnFace.clicked.connect(lambda: outputFace())
        client_id = "t19oy7s6k3"
        client_secret = "JXnfP1GtliSRcli5kvlT7gMiA1cIxSk0SF4NomnH"
        url = "https://naveropenapi.apigw.ntruss.com/vision/v1/celebrity"
        files = {'image': open(filepath, 'rb')}
        headers = {'X-NCP-APIGW-API-KEY-ID': client_id, 'X-NCP-APIGW-API-KEY': client_secret}
        response = requests.post(url, files=files, headers=headers)
        rescode = response.status_code
        if (rescode == 200):
            fac_res = json.loads(response.text)
            fac_num = fac_res['info']['faceCount']



        else:
            print("Error Code:" + rescode)

        def outputFace():
            self.output.setText("닮은 유명인의 수: " + str(fac_num))
            for i in range(fac_num):
                fac_cel = "닮은 유명인: " + fac_res['faces'][i]['celebrity']['value'] + ", 닮은 정도: " + str(
                    fac_res['faces'][i]['celebrity']['confidence'])
                self.output.append(fac_cel)


app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

app.exec_()