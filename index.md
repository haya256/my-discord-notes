---
title: ホーム
nav_order: 0
layout: default
permalink: /
---

# my-discord-notes

Discordの使い方・設定方法を、自分用にまとめたメモです。
Discord本体の機能のほか、Discordと一緒によく使う外部サービス(録音Botの Craig、会員サービスの Patreon など)も扱います。

{: .warning }
これは個人が作成した**非公式**のメモです。Discord Inc. とは関係ありません。
Discordの仕様はよく変わります。各記事の「確認日」と「実機で確認したか」を見て、正確な情報は [Discord公式サポート](https://support.discord.com/) で確認してください。

{: .note }
外部サービスは**Discordの公式機能ではありません**。紹介するだけで、推奨や保証はしません。

## 記事一覧

<!-- toc:start -->

| 記事 | 内容 |
|---|---|
| [用語の基本](docs/01-basics.md) | 用語の基本(サーバー、チャンネル、ロール、カテゴリー、表示名とユーザー名) |
| [通知を減らす](docs/02-notifications.md) | 通知を減らす・ミュート・@everyone抑制 |
| [ファイル送信の容量上限](docs/03-files.md) | ファイル送信の容量上限、大きいファイルの送り方 |
| [Webhookの作り方](docs/04-webhooks.md) | Webhookの作り方と注意点、Botとの違い |
| [開発者モードとIDのコピー](docs/05-developer-mode.md) | 開発者モード、IDのコピー |
| [相手の声がロボットボイスのように途切れる](docs/06-voice-robotic.md) | 通話で相手の声が途切れる・ロボットボイスになるときの切り分け |
| [ボイスチャットを録音する(Craig)](docs/07-voice-recording.md) | ボイスチャットの録音。録音Bot「Craig」の使い方 |
| [Nitro(有料プラン)でできること](docs/08-nitro.md) | Nitro・Nitro Basicの違いと、無料との差 |
| [会員サービスとDiscordのロール連携](docs/09-membership-services.md) | Patreon・FANBOXなど会員サービスと連携して、会員だけにロールを付ける |
| [レイドプロテクション(レイド対策)](docs/10-raid-protection.md) | レイドプロテクション・CAPTCHA・アクティビティアラート・招待の一時停止 |
| [コミュニティ機能](docs/11-community.md) | コミュニティ機能の有効化の条件・できること・無効化 |
| [サーバーブースト](docs/12-server-boost.md) | サーバーブーストのしくみ・レベルごとの特典・追加特典・移し替え |
| [ロールについて](docs/13-roles.md) | ロールとは何か。権限・色・メンション、順番、チャンネルごとの上書きを例で解説 |
| [参加メッセージ(システムメッセージ)の設定](docs/14-system-messages.md) | 新しく参加した人への自動メッセージ・スタンプの促し・ブーストのお知らせを止める・変える |
| [イベント機能](docs/15-events.md) | イベント(予定)の登録と「興味あり」の通知。出欠を取らないゆるい集まりに向く。メンバーに表示しない方法 |
| [文字(フォント)の大きさを変える](docs/16-font-size.md) | チャットの文字が小さくて読みにくいときに、文字の大きさや画面全体の拡大率を変える |

<!-- toc:end -->

## AIに質問する使い方

このメモは、AIに読ませて質問に答えてもらう使い方も想定しています。AIチャットに次のように頼みます。

> このリポジトリをクローンして、README の「AIへの指示」に従って答えてください。
> https://github.com/haya256/my-discord-notes
> 質問:Webhookの作り方は?
