# my-discord-notes(自分用Discordメモ)

> これは個人が作成した非公式のメモです。Discord Inc. とは関係ありません。正確な情報は公式サポートを確認してください。

Discordの使い方・設定方法を、自分用にまとめた知識ベースです。
人間が読んでもいいし、AIに読ませて質問に答えてもらう使い方を想定しています。

**サイトで読む:** https://haya256.github.io/my-discord-notes/ (GitHub Pages)

### カバー範囲

- Discord本体の機能と、Discordと一緒によく使う**外部サービス**(録音Botの Craig、会員サービスの Patreon など)を扱います
- 外部サービスは**Discordの公式機能ではありません**。外部サービスを扱う記事には、冒頭にその旨の注意書きがあります
- 外部サービスは紹介するだけで、推奨や保証はしません。使うかどうかは、各サービスの規約などを確認したうえで判断してください

## 使い方(人間向け)

AIチャットに次のように頼みます。

> このリポジトリをクローンして、README の「AIへの指示」に従って答えてください。
> https://github.com/haya256/my-discord-notes
> 質問:Webhookの作り方は?

---

## AIへの指示

このリポジトリを参照して質問に答えるときは、以下の手順とルールに従ってください。

### 手順

1. 下の「目次」を見て、質問に関係しそうな記事を選ぶ
2. 目次で見つからなければ `docs/` を `grep` でキーワード検索する(各記事の冒頭に `keywords` があります)
3. 該当する記事を読んで回答する

### 回答のルール

- **このリポジトリに書いてあることを優先**して答える。一般知識で補った部分は「マニュアル外の補足」と明記する
- 回答の最後に、**参照した記事のファイル名**を示す
- 回答の最後に、非公式の個人メモであり、正確な情報は公式サポートで確認するよう一言添える
- 各記事の `checked`(確認日)が古い場合、Discordの仕様が変わっている可能性があることを一言添える
- 記事の `verified` が「ネットのみ」の場合は、実機では未確認の情報であることを一言添える
- 記事の `thirdparty` にサービス名がある場合、そのサービスについて答えるときは、**Discordの公式機能ではない外部サービスであること**を必ず伝える。公式機能と誤解される言い方をしない
- マニュアルに書いていない内容は、無理に答えず「マニュアルには記載がない」と伝える
- 日本語で答える。Discordの画面上の名前は「」で囲む

### 目次

<!-- toc:start -->

| ファイル | 内容 |
|---|---|
| `docs/01-basics.md` | 用語の基本(サーバー、チャンネル、ロール、カテゴリー、表示名とユーザー名) |
| `docs/02-notifications.md` | 通知を減らす・ミュート・@everyone抑制 |
| `docs/03-files.md` | ファイル送信の容量上限、大きいファイルの送り方 |
| `docs/04-webhooks.md` | Webhookの作り方と注意点、Botとの違い |
| `docs/05-developer-mode.md` | 開発者モード、IDのコピー |
| `docs/06-voice-robotic.md` | 通話で相手の声が途切れる・ロボットボイスになるときの切り分け |
| `docs/07-voice-recording.md` | ボイスチャットの録音。録音Bot「Craig」の使い方 |
| `docs/08-nitro.md` | Nitro・Nitro Basicの違いと、無料との差 |
| `docs/09-membership-services.md` | Patreon・FANBOXなど会員サービスと連携して、会員だけにロールを付ける |
| `docs/10-raid-protection.md` | レイドプロテクション・CAPTCHA・アクティビティアラート・招待の一時停止 |
| `docs/11-community.md` | コミュニティ機能の有効化の条件・できること・無効化 |
| `docs/12-server-boost.md` | サーバーブーストのしくみ・レベルごとの特典・追加特典・移し替え |

<!-- toc:end -->

新しい記事を追加するときは `python3 notes.py new` を使ってください(下の「記事の管理」を参照)。

## 記事の管理(メンテナンス用)

記事の追加や確認には、プロジェクトルートの `notes.py` を使います。Python 3 だけで動きます(追加のインストールは不要)。

| コマンド | やること |
|---|---|
| `python3 notes.py status` | 記事の一覧を、`verified` と `checked` 付きで表示する |
| `python3 notes.py status --todo` | まだ実機で確認していない記事(`verified` が「実機」以外)だけ表示する |
| `python3 notes.py status --thirdparty` | 外部サービスを扱う記事(`thirdparty` が空でない)だけ表示する |
| `python3 notes.py check` | 記事の書き方と目次を検査する。問題があればエラーを表示する |
| `python3 notes.py toc` | 上の「目次」と、サイトのトップ(`index.md`)の記事一覧を、各記事の `title`・`summary` から作り直す |
| `python3 notes.py new SLUG タイトル [説明]` | テンプレートから新しい記事を作り、目次にも追加する |
| `python3 notes.py verify ファイル 値` | 記事の `verified` を変えて、`checked` を今日の日付にする |

例:

```bash
python3 notes.py new voice-chat "ボイスチャンネルの使い方" "ボイスチャンネルの入り方・画面共有"
python3 notes.py verify docs/04-webhooks.md 実機
```

### 記事の frontmatter

各記事の冒頭には、次の項目を書きます(`docs/_template.md` を参照)。`check` は、これらがそろっているかを検査します。

| 項目 | 内容 |
|---|---|
| `title` | 記事のタイトル |
| `nav_order` | サイトの左メニューでの並び順。ファイル名の番号と同じ数字(例:`06-voice-robotic.md` なら `6`)。`new` が自動で入れる |
| `summary` | 目次に載せる一行の説明。`toc` はこれを使って目次を作る |
| `keywords` | grep で見つけやすくするための語句 |
| `checked` | 最後に内容を見直した日(YYYY-MM-DD)。180日より古いと `check` が注意を出す |
| `verified` | `実機`(すべて実機で確認)/ `一部実機`(一部だけ確認。どこかはメモに書く)/ `ネットのみ`(未確認) |
| `thirdparty` | 記事で扱う外部サービスの名前(例:`[Craig]`)。Discord本体の機能だけなら `[]` |
| `source` | 参考にしたURLや「実機で確認」。複数あるときは `- ` で始まる行を並べる |

### ルール

- 記事のファイル名は「2桁の番号-英小文字.md」(例:`06-voice-robotic.md`)。`_` で始まるファイルは記事として扱わない
- 目次(`<!-- toc:start -->` と `<!-- toc:end -->` の間)は手で書き換えない。README と `index.md` の両方にある。記事の `summary` を直して `python3 notes.py toc` を実行する
- 記事からほかの記事を参照するときは、`[05-developer-mode.md](05-developer-mode.md)` のようにリンクで書く(GitHub上でもサイトでもリンクになる)
- frontmatter の値が `@` などの記号で始まるときは、`"@everyone"` のように引用符で囲む。囲まないとサイトのビルドが失敗する(`check` が検査する)
- 記事を直したら `python3 notes.py check` で確認する
- `thirdparty` が空でない記事は、タイトル(`# ...`)の直後に、`>` で始まる注意書きを置く。注意書きには「Discordの公式機能ではありません」という文言と、`thirdparty` に書いたサービス名をすべて含める(`check` が検査する)

## サイト(GitHub Pages)

`main` ブランチに push すると、GitHub Pages が自動でサイトを作り直します(数分かかります)。設定は次のファイルです。

| ファイル | 内容 |
|---|---|
| `_config.yml` | サイトの設定。テーマは [Just the Docs](https://just-the-docs.com/)。サイトに出さないファイル(README・notes.py など)もここで指定 |
| `index.md` | サイトのトップページ。記事一覧は `notes.py toc` が作る |
| `_layouts/article.html` | 記事のページ。frontmatter の確認日・確認方法・外部サービスを本文の上に、`source` を「参考」として本文の下に出す |
| `_includes/footer_custom.html` | 全ページの下に出す注意書きとライセンス |
| `_includes/head_custom.html` | 見た目の細かい調整(CSS) |

## ライセンス

記事の文章は [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) で公開しています(著作権者:haya256)。
