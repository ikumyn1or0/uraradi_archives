import streamlit as st


import setting as mysetting


mysetting.set_site_config()


st.header("👀ABOUT")

tab_radio, tab_oura, tab_whisper, tab_site = st.tabs(["📻ラジオについて", "🦉大浦るかこについて", "🤖Whisperについて", "🔗本サイトについて"])


with tab_radio:
    st.subheader("裏ラジオウルナイトについて")
    md_text1 = """
- 概ね金曜日25:00からYouTubeで放送中の深夜ラジオ。再生リストのリンクは[こちら](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)。
- パーソナリティは、ななしいんく所属VTuberの[大浦るかこ](https://www.youtube.com/@Rukako_Oura)。
- 2022年12月現在では、公式の切り抜き動画として、[深夜ラジオ総集編#01～#50](https://youtu.be/CdQnrusbXjs)がアップされている。
- おおよそ月1回の頻度でゲストを呼んでおり、同じVTuberである[湖南みあ](https://www.youtube.com/@Mia_Konan)や[緋笠トモシカ](https://www.youtube.com/@-tomoshikahikasa-1255)などの他、動画投稿者である[ハヤシ](https://www.youtube.com/@HayashingElse)や[まだら牛](https://www.youtube.com/@madaraUsi)、歌手の[藍月なくる](https://www.youtube.com/@AitsukiNakuru)などが出演したことがある。（敬称略）
- 放送時間はおよそ１時間半～２時間弱。
    - ラジオでは「今日は１時間以内におさえめます。」と発言することも多い。
- コーナーとして、各放送のタイトルにもなっている週替わりの「今週のメールテーマ」や、複数週にわたって継続した「巷のおもしれー女」「勝手にメールテーマ」などのテーマ、それらのテーマに入らなかったお便りが分類される「ふつおた」がある。
    - 配信時期やゲストの有無に応じて変化するものの、裏ラジではすべて2～4コーナーであったが、2023年1月頃から「週替わりメールテーマ」と「ふつおた」の2コーナー制になった。
- 内容としては、さまざまなジャンルの教養が身に付く話題からR-18な話題まで多岐にわたっており、そのなかでも頻繁に議題に挙がる話題としては以下のようなものがある。（作成者の主観を大いに含む。）
    - [オモコロ](https://omocoro.jp/)および[オモコロチャンネル](https://www.youtube.com/@omocorochannel)
    - [ディスカバリーチャンネル](https://www.youtube.com/@DiscoveryJapan)
    - [しもふりチューブ](https://www.youtube.com/@shimofuritube)および[生涯収支マイナス２億円君](https://www.youtube.com/@soshina/videos)
    - リスナーの健康に関するお悩み
    - リスナーの性事情に関するお悩み
    - 紅茶・コーヒーに関する話
    - アニメ・漫画・本に関する話
    - 774inc所属VTuberに関する話
    - 母（通称：母浦さん）に関する話
    - AIに関する話
    - etc...
    """
    st.markdown(md_text1)


with tab_oura:
    st.subheader("VTuber大浦るかこについて")
    md_text2 = """
- ななしいんく所属のVTuber。（旧774inc.・有閑喫茶あにまーれ所属。）
- 本人のアカウントとしては、[YouTube](https://www.youtube.com/@Rukako_Oura)と[Twitter](https://twitter.com/Rukako_Oura)がある。
- 2021年2月7日にデビュー。同期には[湖南みあ](https://www.youtube.com/@Mia_Konan)、[月野木ちろる](https://www.youtube.com/@Tirol_Tsukinoki)がいる。
- 誕生日は9月26日。有閑喫茶あにまーれでは経理を担当している。
    - その他のプロファイルについては[初配信](https://www.youtube.com/live/-HtouDbuxUI?feature=share)での自己紹介部分のキャプチャをページ下部に記載するので参照のほど。
    - より詳細なエピソード・パーソナリティについては、有志によって作成された[非公式wiki](https://wikiwiki.jp/774inc/大浦るかこ)などを参照のほど。
- 定期配信としては以下のようなものがある。（2023年3月時点。）
    - 火曜日12時からの同期コラボ配信：[みるちーずLUNCH MTG](https://www.youtube.com/playlist?list=PLShwbdwZFm3qN7rQ_UZ6ReZQoPXULPuCA)
    - 水曜日7時からの朝枠：[COFFEE&CHILL MORNING](https://www.youtube.com/playlist?list=PLShwbdwZFm3rsurz8jw-c1LRl0wqUpr5n)
    - 金曜日25時からの深夜ラジオ：[裏ラジオウルナイト](https://www.youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)
    - 月1回土曜日15時からの紹介型読書会：[電脳図書室](https://youtube.com/playlist?list=PLShwbdwZFm3q9C62t2MSgkZsnKRhMb8zI)
    - 月1回月末24時からの課題本型読書会：[月末読書会#知るかコラボ](https://youtube.com/playlist?list=PLShwbdwZFm3oWGZ052XFFWogkkir4F1S2)
- 特にコラボ等の関わりが多いのは、同期の[湖南みあ](https://www.youtube.com/@Mia_Konan)、[月野木ちろる](https://www.youtube.com/@Tirol_Tsukinoki)のほかにも、774inc.所属の[宗谷いちか](https://www.youtube.com/@Ichika_Souya)、[島村シャルロット](https://www.youtube.com/@Charlotte_Shimamura)、[獅子王クリス](https://www.youtube.com/@ChrisShishio)や、VTuberの[緋笠トモシカ](https://www.youtube.com/@-tomoshikahikasa-1255)、[神楽すず](https://www.youtube.com/@SuzuKagura)、[天城てん](https://www.youtube.com/@AmagiTen)、配信者の[ディズム](https://www.youtube.com/@DizmKDC)などがある。（なお、この項目は作成者の主観を大いに含む。）
    - 有志によって作成された[大浦るかこコラボ先リスト](https://www.youtube.com/playlist?list=PLBd6R8wa6co_Yfc-dlQEW3Xf9E5j96HtQ)もご参照のほど。
"""
    st.markdown(md_text2)

    st.subheader("初配信時の自己紹介")
    st.markdown("初配信のリンクは[こちら](https://www.youtube.com/live/-HtouDbuxUI?feature=share)。")
    st.image("./input/profile/profile_1.png", caption="【謎解き】スパイ、秘密の初配信【大浦るかこ / あにまーれ】 #3:41")
    st.image("./input/profile/profile_2.png", caption="【謎解き】スパイ、秘密の初配信【大浦るかこ / あにまーれ】 #10:20")
    st.image("./input/profile/profile_3.png", caption="【謎解き】スパイ、秘密の初配信【大浦るかこ / あにまーれ】 #17:03")


with tab_whisper:
    st.subheader("Whisperについて")
    md_text3 = """
    - [Whisper](https://openai.com/research/whisper)とは、人工知能を研究するアメリカの非営利団体[OpenAI](https://openai.com/)が2022年9月に公開した音声認識システム。
    - Web上から収集した68万時間分のデータを学習に用いており、音声データを入力とする以下のようなタスクに対応することができる。
        - 英語での発話の書き起こし
        - 非英語での発話の書き起こし
        - 非英語での発話から英語への翻訳
    - Whisperの発表時点で、他のオープンソースモデルと比較して様々なタスクにおいて同じくらいか高精度の評価結果を残した。
    - なお、この情報は2022年11月時点のものである。
    """
    st.markdown(md_text3)

    with st.expander("Whisperを使ってみての感想"):
        md_text4 = """
- 使いやすい点
    - 精度が良い点: まだ完璧とは言えないが、一般的な会話に関してはかなり精度が高いと思った。誤認識箇所も、発音は正しいものの単語を間違えてたケースなどがあり、音声自体の認識としてはかなり正確だと分かった。
    - 再生時間が取得できる点: このサイトを作成するうえで、文字起こしの結果と実際のYouTubeの再生箇所を照らし合わせる機能は実装したかったため、文字起こししたテキストが音声の何秒の時点で発話されたか取得できるのはありがたかった。
- 使いづらい点
    - 精度が完璧ではない点: ラジオの書き起こしでも、正確に認識されていない例がかなりあった。これは、①Whisperが日本語に特化したモデルになっていないため、②BGMや複数人の会話といったノイズに影響されているため、などが理由として考えられる。
    - 推論を行うたびに書き起こし結果が変化する点: 画像や文章の生成とは違い、音声の認識は発言という正解データがあるため、同じ音声データに対しては同じ書き起こし結果を出力できるようになるとよいと思った。
    - 推論時間が長い点: 今回は一番精度が高いlargeモデルを利用したが、ラジオ１回分(２時間弱)の書き起こしを行うのに30分程度かかった(google colab & GPU環境)。時間やGPUの計算リソースがある程度必要となり、気軽に誰でも文字起こしを使えるものにはなっていない。
    - 固有名詞などの語彙の追加に膨大なコストがかかる点: 音声認識からテキスト化まで全てがブラックボックスとなっているWhisperのようなAIモデル全般に言えることだが、商用化ソフトとは異なり、固有名詞を追加するためにはモデルの再学習が必要。これには音声データと正解となる単語のペアがかなりの数用意する必要があり、かつマシンリソース・時間リソースが必要となる。
"""
        st.markdown(md_text4)

#     st.subheader("このサイトにおけるWhisperの活用について")
#     md_text5 = """
# 下に示す3つのgoogle colablatoryを実行することで、裏ラジプレイリスト全件の書き起こしデータを作成している。

# **STEP1 裏ラジプレイリストデータから必要な情報を抜き出したcsvファイルの作成**

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ikumyn1or0/uraradi_archives/blob/master/notebook/step1_playlist_to_csv.ipynb)

# **STEP2 csvファイルから裏ラジ全件のmp3データをダウンロード**

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ikumyn1or0/uraradi_archives/blob/master/notebook/step2_csv_to_mp3.ipynb)

# **STEP3 mp3データをWhisperによって書き起こし**

# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ikumyn1or0/uraradi_archives/blob/master/notebook/step3_mp3_to_transcript.ipynb)
# """
#     st.markdown(md_text5)


with tab_site:
    st.subheader("このサイトの作成にあたって")
    md_text6 = """
- [裏ラジ#65「いまどこにいるの、AI」](https://youtu.be/SgmH7uaE-ac)を受け、最新のAIを使って何かしら作りたいと思い、作成に至った。
- 画像生成AI（[Stable Diffusion](https://stablediffusionweb.com/), etc...）や文章生成AI（[GPT-3](https://github.com/openai/gpt-3), etc...）は多くの活用例が見られるが、Whisperという音声処理特化AIモデルを使用した例はあまり見られていなかった。今回のサイト作成で音声認識AIの現在地ともいえるWhisperに関する様々な知見を得ることができた。
    - かなり認識精度は高い一方、日本語の精度は完璧ではなく、固有名詞に特化するためのモデルの再学習を行うコストはかなり高く、ユーザーが利用するうえではハードルがあることがわかった。詳細な感想を以下に示す。
- 2022年で最新のAIを使っても音声認識の実用的利用にはハードルがあり、人間がどんな状況でも音声を正しく認識できていることってすごいんだなあという実感とともに、今後のAIのさらなる発展に期待したい。
- なお、この情報は2022年11月時点のものである。
"""
    st.markdown(md_text6)

    st.subheader("注意事項")
    md_text7 = """
- 「放送日付」とは、一般的に金曜日の日付を表す。
- 本サイト作成において使用したYouTubeの音声データおよびYouTubeの画像データ、立ち絵データはすべて774inc.および大浦るかこさんに帰属するものであり、本サイトはこれらの二次創作です。
- 本サイトに関する質問・バグの報告などは[@mega_ebi](https://twitter.com/mega_ebi)までお願いします。ソースコードは[こちら](https://github.com/ikumyn1or0/uraradi_archives)。
    """
    st.markdown(md_text7)
