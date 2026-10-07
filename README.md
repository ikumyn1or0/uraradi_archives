# uraradi_archives

## 説明

- [裏ラジアーカイブス](https://uraradi-archives.streamlit.app/)開発用のディレクトリ
- このプロジェクトでは、ローカル環境において作成したWhisperによるラジオ書き起こしテキスト(csv)をもとにした可視化サイトを作成する
- 以下の機能を備えている
  - ラジオの情報(放送時間など)可視化機能
  - ラジオ書き起こしcsv全文表示機能
  - ラジオ書き起こしcsv検索機能

## サイトの運用

- [大浦るかこさんの事務所退社](https://x.com/Rukako_Oura/status/1769651462584537089?s=20)に伴って更新は停止する。
- ただし、公開に使用しているStreamlit Community Cloudが無償利用できる限りは公開を継続する。

## 使用パッケージ

- pandas
- streamlit
- plotly
- Whisper(ローカル環境でラジオ書き起こしテキストを作成した際のみ使用、ここではインポート不要)

## 依存関係の固定

- Streamlit Community Cloudは`requirements.txt`を`pyproject.toml`より優先して読み込むため、本番環境のバージョンは`requirements.txt`で全パッケージ固定している(Python 3.10で動作確認済み)
- ローカル環境は`poetry.lock`で固定している(Python 3.9)
- パッケージを更新する場合は、表示が変わらないことを確認したうえで両方を更新すること
