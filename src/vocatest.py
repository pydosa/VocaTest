import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSound
import csv
import time

TIMEOUT = 10

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = uic.loadUi("./res/vocatest.ui", self)
        self.ui.show()

        #초기화면 시작 버튼 생성 & 초기화
        self.bnStart = QPushButton(self)
        self.bnStart.setDefault(False)
        self.bnStart.setGeometry(80, 40, 400, 320)
        self.bnStart.setIcon(QIcon(QPixmap("./res/start.jpg")))
        self.bnStart.setIconSize(QSize(390, 310))
        # self.bnStart.setStyleSheet("background-image: url('start.jpg'); border: none;")
        self.bnStart.clicked.connect(self.bnStart_clicked)

        #정답 선택 라벨 마우스 이벤트 설정
        #self.ui.label_select4.mousePressEvent = self.slot_label_select_clicked
        self.ui.label_select1.installEventFilter(self)
        self.ui.label_select2.installEventFilter(self)
        self.ui.label_select3.installEventFilter(self)
        self.ui.label_select4.installEventFilter(self)

        #폰트
        #font = QFont()
        #font.setFamily(_fromUtf8(""))
        #font.setBold(True)
        quesFont = QFont("Times", 21, QFont.Bold)
        self.ui.label_question.setFont(quesFont)
        self.ui.label_question.setStyleSheet("QLabel { background-color : #ffd732; color : black; }");

        scoreFont = QFont("Times", 14, QFont.Bold)
        self.ui.label_score.setFont(scoreFont)
        self.ui.label_score.setStyleSheet("QLabel { color : blue; }");
                                          #"background-color : white;}");
                                          #"border:1px solid rgb(100, 100, 255);}");

        answFont = QFont("굴림", 11, QFont.Normal)
        self.ui.label_select1.setFont(answFont)
        self.ui.label_select2.setFont(answFont)
        self.ui.label_select3.setFont(answFont)
        self.ui.label_select4.setFont(answFont)

        #변수 초기화
        self.timer = None
        self.testNum = 0
        self.selAnswer = ''    #유저가 선택한 답(정답 A,B형인 경우 '1' ~ '4', C형일 경우 'string')
        self.cntAnswer = 0     #정답개수

        #csv 파일 load
        self.vocas = csv.DictReader(open("../data/test.csv"))
        self.vocas = list(self.vocas)
        self.nTestTotal = len(self.vocas)

        self.retImg = QLabel(self)
        self.retImg.setGeometry(30, 270, 190, 120)

        self.label_counter = QLabel(self)
        self.label_counter.setGeometry(510, 70, 50, 50)
        self.label_counter.setFont(quesFont)
        self.label_counter.setStyleSheet("QLabel { color : red; }");
        self.label_counter.setText("%d" % TIMEOUT)
        # "background-color : white;}");
        # "border:1px solid rgb(100, 100, 255);}");

        self.showControls(False)
        self.bnStart.show()
        self.updateScore()
        self.setWindowTitle('뇌새김 단어 맞추기')

    def init_vocaTest(self):
        self.timer = None
        self.testNum = 0
        self.selAnswer = ''  # 유저가 선택한 답(정답 A,B형인 경우 '1' ~ '4', C형일 경우 'string')
        self.cntAnswer = 0  # 정답개수
        self.updateScore()

    def start_timer(self, slot, count=1, interval=1000):
        counter = 0

        def handler():
            nonlocal counter
            counter += 1
            slot(counter)
            '''
            if counter >= count:
                self.timer.stop()
                self.timer.deleteLater()
            '''
        self.timer = QTimer()
        self.timer.timeout.connect(handler)
        self.timer.start(interval)

    def stop_timer(self):
        if self.timer != None:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None

    def timer_func(self, count):
        print('Timer:', count)

        if count >= TIMEOUT:
            self.checkTest('')
            print("Timeout - 다음 문제로 넘어 갑니다.")
            self.testNum += 1
            self.goNextTest(self.testNum)
            self.label_counter.setText("%d" % TIMEOUT)
        else:
            self.label_counter.setText("%d" % (TIMEOUT - count))

    def bnStart_clicked(self):
        self.bnStart.hide()
        self.showControls(True)
        self.init_vocaTest()
        self.setVocaTest(self.testNum)

    def showControls(self, bShow):
        if bShow:
            self.ui.label_descript.show()
            self.ui.label_question.show()
            self.ui.label_select1.show()
            self.ui.label_select2.show()
            self.ui.label_select3.show()
            self.ui.label_select4.show()
            self.ui.label_score.show()
            self.label_counter.show()
        else:
            self.ui.label_descript.hide()
            self.ui.label_question.hide()
            self.ui.label_select1.hide()
            self.ui.label_select2.hide()
            self.ui.label_select3.hide()
            self.ui.label_select4.hide()
            self.ui.label_score.hide()
            self.label_counter.hide()

    #시험문제 준비
    def setVocaTest(self, currNum):
        self.stop_timer()
        test = self.vocas[currNum]
        type = test["TYPE"]
        if type == 'A':
            descript = "{0}. 다음 영단어의 뜻을 고르시오.".format(currNum+1)
        elif type == 'B':
            descript = "{0}. 다음 뜻과 일치하는 영단어를 고르시오.".format(currNum+1)
        elif type == 'C':
            descript = "{0}. 다음에 해당하는 영단어 철자를 입력하시오".format(currNum+1)

        self.ui.label_descript.setText(descript)
        self.ui.label_question.setText(test["QUESTION"])    #폰트 크게

        if type != 'C':
            strSel = '① ' + test["SELECT1"]
            self.ui.label_select1.setText(strSel)
            strSel = '② ' + test["SELECT2"]
            self.ui.label_select2.setText(strSel)
            strSel = '③ ' + test["SELECT3"]
            self.ui.label_select3.setText(strSel)
            strSel = '④ ' + test["SELECT4"]
            self.ui.label_select4.setText(strSel)

        #타이머
        self.start_timer(self.timer_func, TIMEOUT)

    def checkTest(self, selAnswer):
        #정답인 경우
        test = self.vocas[self.testNum]
        answer = test["ANSWER"]
        if selAnswer == answer:
            QSound.play("./res/good.wav")
            imgpath = "./res/good.png"
            self.cntAnswer += 1
        else:
            QSound.play("./res/wrong.wav")
            imgpath = "./res/nogood.png"

        temp = QPixmap(imgpath)
        pixmap = temp.scaled(self.retImg.width(), self.retImg.height())
        self.retImg.setPixmap(pixmap)
        self.retImg.show()
        self.retImg.repaint() #hide하기 전에 repaint를 해줘야 제대로 보이네... update는 안먹힘
        time.sleep(0.5) #결과이미지 보여주고 2초간 대기
        self.retImg.hide()

        self.updateScore()

    def updateScore(self):
        self.strScore = "%d / %d" % (self.cntAnswer, self.nTestTotal)
        self.ui.label_score.setText(self.strScore)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            if source == self.ui.label_select1:
                selAnswer = '1'
            elif source == self.ui.label_select2:
                selAnswer = '2'
            elif source == self.ui.label_select3:
                selAnswer = '3'
            else:
                selAnswer = '4'
            print("The sender is:", source.text())

            self.checkTest(selAnswer)
            # 다음문제로...
            self.testNum += 1
            self.goNextTest(self.testNum)

        return super(Form, self).eventFilter(source, event)

    def goNextTest(self, testNum):
        if testNum < self.nTestTotal:
            self.setVocaTest(testNum)
        elif testNum >= self.nTestTotal:
            # 테스트종료
            self.stop_timer()
            choice = QMessageBox.question(self, '시험 끝 ',
                                          "맞은 개수 : %d\n틀린 개수 : %d\n종합 점수 : %d점\n\n재시도 하시겠습니까?"
                                          % (self.cntAnswer, self.nTestTotal - self.cntAnswer,
                                             self.cntAnswer / self.nTestTotal * 100),
                                          QMessageBox.Yes | QMessageBox.No)
            if choice == QMessageBox.Yes:
                self.bnStart_clicked()
            else:
                sys.exit()
    '''
    def slot_label_select_clicked(self, event):
        label = self.sender()
        label = QLabel(label)
        txt = label.text()
        print("%s clicked" % label.text())
    '''


if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        w = Form()
        sys.exit(app.exec())