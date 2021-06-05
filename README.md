-------------------------

# getScript

* __동영상 자막 추출__ : 분리되지 않는 영상 내 자막을 추출해 자막 텍스트 파일을 생성합니다.

* __자막 오디오 변환__ : 자막 텍스트 파일을 음성으로 변환해 자막 오디오 파일을 생성합니다.

* __자막 번역__ : 영어 자막을 한국어로 번역해 자막 번역 파일을 생성합니다.


-------------------------

<br>

## Google-Cloud-Vision API 키 발급 및 코드 수정

> **getScript**는 **Google-Cloud-Vision API**를 사용하고 있습니다. 
>
> 키를 발급받은 후 소스코드에 키 경로를 명시해 주었을 때 작동 가능합니다.


**Vision API 키 발급 참고**

<https://manord.tistory.com/15>

**코드 수정**

[writeScript.py](https://github.com/jiwoo-jus/getScript/blob/c611daefbcaf70b3dc72b7314d367bd221412879/writeScript.py) **line 4**

```python
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"발급받은 json 키파일 경로"
````

<br>

## 필요 라이브러리 설치
```bash
$ pip install PyQt5
$ pip install opencv-python
$ pip install google-cloud-vision
$ pip install googletrans==4.0.0-rc1
$ pip install gTTS
```
*ModuleNotFoundError: No module named 'urllib3'* 에러 발생 시
```bash
$ pip install urllib3
```
*ModuleNotFoundError: No module named 'six'* 에러 발생 시
```bash
$ pip uninstall six
$ pip install six
```

<br>

## 사용 방법

### 동영상 자막 추출 

**프로그램 실행**

```python
>>> python main.py
```

**동영상 선택**

> 파일 다이어로그의 초기 경로는 getScript/sample 이며, 해당 경로에 샘플 영상이 있습니다.

`Open File` *click*

**자막 추출**

`Run` *click*

**자막 영역 설정**

1. 자동 재생된 영상에 자막이 보이면 키 `c`를 눌러 일시정지합니다.

2. 자막 영역을 드래그합니다. (영상의 전반적인 자막 영역)

3. 지정한 영역이 마음에 들면 키 `c`, `q`를 순서대로 눌러 자막 영역 설정을 종료합니다.

4. 지정한 영역이 마음에 들지 않으면 키 `r`을 눌러 동영상을 이어서 재생합니다. 이후 위 과정을 반복합니다.

### 자막 오디오 변환

`Text To Speech` *click*

### 자막 번역

> 전체 영문인 자막파일만 번역 가능합니다.

`Translate` *click*
