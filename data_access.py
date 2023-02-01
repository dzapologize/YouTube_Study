# importing the youtube_video module
from pytube import YouTube
# importing the Subtitles module
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
# importing the Translation module
import json
import pysrt
import requests


def Download_video(link):
    youtubeObject = YouTube(link)
    youtubeObject2 = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject2.download()
        caption = youtubeObject.captions.get_by_language_code('en')
        print(caption)
    except:
        print("下载失败!!!")
    print("success")
    caption = youtubeObject.captions.get_by_language_code('en')
    print("下载视频的语言为: ", caption)


def Download_Subtitles(video_id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    formatter = SRTFormatter()
    # Translated Text
    # Original subtitle text
    for transcript in transcript_list:
        zh_hans = transcript.translate('zh-Hans').fetch()
        srt_zh_hans_formatted = formatter.format_transcript(zh_hans)
        print('srt_zh_hans_formatted', srt_zh_hans_formatted)
        with open(video_id + ".srt", "w") as f:
            # iterating through each element of list srt
            f.write(srt_zh_hans_formatted)


def translate(word):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    key = {
        'type': "AUTO",
        'i': word,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    response = requests.post(url, data=key)
    if response.status_code == 200:
        return response.text
    else:
        print("有道词典调用失败")
        return None


# 获得翻译结果
def get_reuslt(repsonse):
    #
    result = json.loads(repsonse)
    return result['translateResult'][0][0]['tgt']


def translate(video_id):
    try:
        subs = pysrt.open(video_id+'.srt')
    except:
        print("打开文件失败，请输入本文件夹下正确的SRT文件名")
        return 0
    for line in subs:
        print(line.text)
        # 在此可以添加对每句话的操作，如去掉末尾句号
        list_trans = translate(line.text)
        line.text = get_reuslt(list_trans)
    subs.save(video_id + '_CN.srt', encoding='utf-8')

# TODO 剪映配字幕的优化
def main():
    video_link = "https://www.youtube.com/watch?v=eZe4Q_58UTU"
    Download_video(video_link)
    video_id = video_link.split("?v=")[1]
    Download_Subtitles(video_id)
    translate(video_id)

if __name__ == '__main__':
    main()
