import streamlit as st
import pandas as pd

# set page config
st.set_page_config(page_title="裏ラジアーカイブス", page_icon="🦉")

st.title("📻裏ラジアーカイブス🦉")

# ----------

st.header("詳細情報")

tab1, tab2 = st.tabs(["ラジオについて", "AIについて"])

with tab1:
    st.subheader("裏ラジオウルナイトについて")

    md_text1 = """
    - ラジオの再生リストは[こちら](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)
    - 概ね金曜日25:00からYouTubeで放送中の深夜ラジオ。
    - パーソナリティは774.inc所属VTuberの[大浦るかこ](https://www.youtube.com/@Rukako_Oura)。
    - たまにゲストを呼んでおり、同じVTuberである[湖南みあ](https://www.youtube.com/@Mia_Konan)・[緋笠トモシカ](https://www.youtube.com/@-tomoshikahikasa-1255)などの他、[ハヤシ](https://www.youtube.com/@HayashingElse)・[まだら牛](https://www.youtube.com/@madaraUsi)（配信者）、[藍月なくる](https://www.youtube.com/@AitsukiNakuru)（歌手）などが出演したことがある。
    - 放送時間は概ね２時間弱。
    - コーナーとして、各放送のタイトルにも用いられている「今週のメールテーマ」や、「巷のおもしれー女」「勝手にメールテーマ」などの複数週にわたって募集されるメールテーマ、それらのテーマに入らなかったお便りが分類される「ふつおた」がある。
    - 内容としては、さまざまなジャンルの教養が身に付く話題からR-18な話題まで多岐にわたる。
    - 公式の切り抜き動画としては、[深夜ラジオ総集編#01～#50](https://youtu.be/CdQnrusbXjs)がアップされている。（2022年12月現在）
    """
    st.markdown(md_text1)

    # ----------

    st.subheader("VTuber大浦るかこについて")

    md_text2 = """
    - [YouTubeリンク](https://www.youtube.com/@Rukako_Oura)および[Twitterのリンク](https://twitter.com/Rukako_Oura)はこちら。
    - 以下、初配信時の自己紹介・プロフィールを引用。

    > 北区赤羽の有閑喫茶あにまーれに
    >
    > 経理担当として雇用されたフクロウです
    >
    > 好きな色は藍色！
    >
    > 眼鏡はパンツと同義！



    > 誕生日：9月２６日生の天秤座
    >
    > 趣味：シナプスつなぎ、耳の奥から水を出す、読書
    >
    > 好物：叙述トリック、砂肝
    >
    > 苦手なこと：生活、割り算
    >
    > 命の糧：アンジュルム、アイドル全般

    - より詳細な情報については[非公式wiki](https://wikiwiki.jp/774inc/大浦るかこ)などを参照のこと。
"""
    st.markdown(md_text2)

with tab2:
    st.subheader("Whisperについて")

    md_text3 = """
    - 人工知能を研究するアメリカの非営利団体[OpenAI](https://openai.com/)が2022年9月に公開した音声認識システム。
    - Web上から収集した68万時間分のデータを学習に用いており、音声データを入力とする以下のようなタスクに対応することができる。
        - 英語での発話の書き起こし
        - 非英語での発話の書き起こし
        - 非英語での発話から英語への翻訳
    - Whisperの発表時点で、他のオープンソースモデルと比較して様々なタスクにおいて同じくらいか高精度の評価結果を残した。
    """
    st.markdown(md_text3)

    # ----------

    st.subheader("このサイトでの活用について")

    md_text4 = """
    - [裏ラジ#65「いまどこにいるの、AI」](https://youtu.be/SgmH7uaE-ac)を受け、最新のAIを使って何かしら作りたいと思い、作成に至った。
    - 画像生成AI（[Stable Diffusion](https://stablediffusionweb.com/), etc...）や文章生成AI（[GPT-3](https://github.com/openai/gpt-3), etc...）は広く知れ渡っており、多くの活用例が見られるが、今回はWhisperという音声処理タスクに特化したAIモデルを触ってみたいと思った。実際、今回のサイト作成で音声認識AIの現在地ともいえるWhisperに関する様々な知見を得ることができた。
    - 感想としては、かなり認識する精度は高い一方で、日本語については完璧とは言い難く、モデルの推論・再学習を行うコストはかなり高いため、ユーザーが実用的に利用するにはまだまだハードルがあることがわかった。詳細な感想を以下に示す。
    - 2022年で最新のモデルを使ったとしても実用的利用には程遠く、人間がどんな状況でも音声を正しく認識できていることってすごいんだなあという実感とともに、今後のAIの発展に期待したい。
    """
    st.markdown(md_text4)

    with st.expander("詳細な感想"):
        md_text5 = """
        - 使いやすい点
            - 精度が良い点: まだ完璧とは言いませんが、かなりの精度が出ているなと思いました。誤っている箇所も発音は正しいものの単語を間違えているケースなどがあり、音声の認識としてはかなり正確に聞き取れていることがわかりました。
            - 再生時間が取得できる点: このサイトを作成するうえで、文字起こしの結果を実際のYouTubeの再生箇所と照らし合わせて確認できるといいなと思っていたので、文字起こししたテキストが何秒の時点で発話されたものか取得できるのは有り難いと思いました。
        - 使いづらい点
            - 精度が完璧とはいえない点: ラジオの書き起こしでも、正確に認識されていない例がかなりありました。これは、①Whisperのモデル自体が日本語音声に特化したものではないため、②BGMや複数人の会話など、ノイズに影響されてしまっているため、などが理由として考えられます。
            - 推論を行うたびに書き起こし結果が変化してしまう点: 画像や文章の生成とは違い、音声の認識は発話という正解データがあるため、同じ音声データに対しては同じ書き起こし結果を出力できるようになると便利だと思いました。
            - 推論時間が長い点: 今回は一番精度が高いモデルを利用しましたが、ラジオ１回分(２時間弱)の書き起こしを行うのに30分程度かかります(google colab & GPU環境)。時間やGPUの計算リソースがある程度必要となり、気軽に誰でも文字起こしを使えるものにはなっていないでしょう。

            - 固有名詞など語彙の追加に膨大なコストがかかる点: 音声認識からテキスト化まで全てがブラックボックスとなっているWhisperのようなAIモデル全般に言えることですが、商用化されているソフトとは違い、固有名詞を追加するためにはモデルの再学習が必要です。これには音声データと正解となる単語のペアがかなりの数必要であり、また、推論と同じようにマシンリソース・時間リソースが必要です。
        """
        st.markdown(md_text5)
