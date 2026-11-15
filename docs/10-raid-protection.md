---
title: レイドプロテクション(レイド対策)
nav_order: 10
summary: レイドプロテクション・CAPTCHA・アクティビティアラート・招待の一時停止
keywords: [レイド, レイドプロテクション, レイド保護, raid, Raid Protection, 荒らし, 大量参加, CAPTCHA, キャプチャ, アクティビティアラート, Activity Alerts, セキュリティアクション, Security Actions, 招待の一時停止, Pause Invites, AutoMod, 認証レベル, 安全設定, Safety Setup]
checked: 2026-11-15
verified: ネットのみ
thirdparty: []
source:
  - https://support.discord.com/hc/en-us/articles/10989121220631-How-to-Protect-Your-Server-from-Raids-101 (公式ヘルプ。本文は取得できず、検索結果の要約のみ)
  - https://support.discord.com/hc/en-us/articles/17439993574167-Activity-Alerts-Security-Actions (公式ヘルプ。本文は取得できず、検索結果の要約のみ)
  - https://discord.com/blog/new-anti-spam-raid-automod-safety-update (公式ブログ、2022-09-21)
  - https://n3tc0rd.digitalpress.blog/discords-new-raid-protection-feature/ (非公式、2022-12-24)
  - https://frameworks.securityalliance.org/guides/account-management/discord/ (非公式)
---

# レイドプロテクション(レイド対策)

## 要点

- **レイド**とは、多くのアカウント(Botが多い)が短い時間にまとめてサーバーに入り、スパムや荒らしの投稿を一斉にする行為のこと
- **レイドプロテクション**はDiscord本体の機能。機械学習でレイドらしい大量参加を見つけると、決めておいたチャンネルに**アラート**を出す。その後**1時間**は、新しく入る人に**CAPTCHA**(ロボットでないことの確認)を求める
- レイドが起きているときは、**セキュリティアクション**で招待やDMを一時停止して、追加で人が入ってくるのを止められる

## 機能の一覧

| 機能(英語版の名前) | やること |
|---|---|
| レイドプロテクションとCAPTCHA(Raid Protection and CAPTCHA) | レイドを見つけて知らせる。参加する人にCAPTCHAを求める |
| アクティビティアラート(Activity Alerts) | 参加やDMが普段より異常に多いときに知らせる |
| セキュリティアクション(Security Actions) | 招待とDMを一時停止する。止める時間を決められる |
| 招待の一時停止(Pause Invites) | 招待リンクを消さずに、新しい人が入れないようにする |
| AutoMod | スパムや、大量のメンションをするメッセージをブロックする |

- 日本語版の画面での名前は未確認です。上の表のかっこ内は英語版の名前

## 手順(PC)

### レイドプロテクションを設定する(平常時にやっておく)

1. サーバー名を押して「サーバー設定」を開く
2. 左メニューの安全設定の項目(英語版は「Safety Setup」。日本語版での名前は未確認)を開く
3. 「Raid Protection and CAPTCHA」の項目で、次を設定する
   - アラートを送るチャンネルを選び、アラートを有効にする(モデレーターが見られるチャンネルにする)
   - 必要に応じて、次の2つを有効にする
     - 怪しいアカウントが参加する前にCAPTCHAを求める(CAPTCHA suspicious accounts before they are able to join)
     - レイドが疑われるあいだは、全員に参加前のCAPTCHAを求める(CAPTCHA all accounts before they are able to join during a suspected raid)
   - 「Activity Alerts」を有効にする

### レイドが起きたときに止める

1. セキュリティアクションを開く。開く場所は次のどれか
   - サーバー名のドロップダウンメニュー
   - メンバー一覧(Members)のタブ
   - 届いたアラートのメッセージ
2. 招待とDMを一時停止し、止めておく時間を選ぶ
3. 落ち着いたら停止を解除する。決めた時間が来る前でも、自分でオフにできる

- 「サーバー設定」→「招待」(Invites)からも、招待を一時停止できる。招待リンクは消えずに表示されたままになるが、そのリンクから新しい人は入れなくなる

### あわせてやっておくと良いこと

- 「サーバー設定」→「AutoMod」で、スパム対策(Block Spam Content)とメンションスパム対策(Block Mention Spam)を有効にする。メンションスパムの項目には、メンションレイドを検出する設定(英語版は「Enable mention raid detection」)もある
- 認証レベル(なし・低・中・高 など)を上げて、作ったばかりのアカウントがすぐ投稿できないようにする
- 荒らしの投稿を消して、荒らしのアカウントをBANしてから、招待の停止を解除する

## メモ

- この記事はネットの情報だけでまとめた。**実機では確認していない**。画面での名前や設定する場所は、変わっている可能性がある
- レイドプロテクションは、2022年末に「ベータ版」として始まった機能。その後名前が「Raid Protection and CAPTCHA」に変わったらしい
- 公式ブログ(2022年)では、AutoModのスパム対策を使うには**コミュニティ機能が有効**になっていることが必要とされている。レイドアラートも、コミュニティサーバーに少しずつ提供されていた。コミュニティでないサーバーでは、表示されない項目があるかもしれない
- 大型イベントなどで、レイドではない参加の急増でもアラートが出ることがある。公式FAQでは、これは普通のことだとしている
- Wick などのセキュリティBotでも同じような対策ができるが、それらは外部サービスでDiscordの公式機能ではない。この記事では扱わない
