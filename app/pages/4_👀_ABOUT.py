import streamlit as st
import Visualize as myviz


myviz.set_uraradi_config()


st.header("👀ABOUT")


tab_radio, tab_oura, tab_whisper = st.tabs(["ラジオについて", "大浦るかこについて", "Whisperについて"])


with tab_radio:
    st.subheader("裏ラジオウルナイトについて")
    md_text1 = """
- 概ね金曜日25:00からYouTubeで放送中の深夜ラジオ。再生リストのリンクは[こちら](https://youtube.com/playlist?list=PLShwbdwZFm3r77Bwrr1quz2CpqJc6BZVL)。
- パーソナリティは774inc.・有閑喫茶あにまーれ所属VTuberの[大浦るかこ](https://www.youtube.com/@Rukako_Oura)。
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
- 774inc.・有閑喫茶あにまーれ所属のVTuber。
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
    - 人工知能を研究するアメリカの非営利団体[OpenAI](https://openai.com/)が2022年9月に公開した音声認識システム。
    - Web上から収集した68万時間分のデータを学習に用いており、音声データを入力とする以下のようなタスクに対応することができる。
        - 英語での発話の書き起こし
        - 非英語での発話の書き起こし
        - 非英語での発話から英語への翻訳
    - Whisperの発表時点で、他のオープンソースモデルと比較して様々なタスクにおいて同じくらいか高精度の評価結果を残した。
    """
    st.markdown(md_text3)

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
