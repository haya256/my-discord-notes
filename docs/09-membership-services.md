---
title: 会員サービスとDiscordのロール連携
summary: Patreon・FANBOXなど会員サービスと連携して、会員だけにロールを付ける
keywords: [会員制, 会員, メンバーシップ, 有料会員, 支援者, ファンクラブ, ロール, 自動付与, 連携, 認証, 限定チャンネル, Patreon, パトレオン, FANBOX, pixivFANBOX, ファンボックス, Ci-en, シエン, note, Fantia, ファンティア, Ko-fi, YouTubeメンバーシップ, Twitch, サブスク]
checked: 2026-11-04
verified: ネットのみ
thirdparty: [Patreon, pixivFANBOX, Ci-en, Ko-fi, note, Fantia, YouTube, Twitch]
source:
  - https://support.patreon.com/hc/en-us/articles/213552323
  - https://fanbox.pixiv.help/hc/en-us/articles/48305576832921-About-Discord-integration
  - https://fanbox.pixiv.help/hc/en-us/articles/48307814312729-Get-started-with-Discord-integration-for-supporters
  - https://official.fanbox.cc/posts/10465468
  - https://gamebiz.jp/news/298071
  - https://help.ko-fi.com/hc/en-us/articles/360020363857
  - https://www.help-note.com/hc/ja/articles/22752829171225
  - https://support.discord.com/hc/en-us/articles/212112068
  - https://discord.com/creators/subscriber-roles-101
---

# 会員サービスとDiscordのロール連携

> **注意**:この記事で扱う Patreon、pixivFANBOX、Ci-en、Ko-fi、note、Fantia、YouTube、Twitch は、Discordの公式機能ではありません。それぞれ別の会社が提供するサードパーティのサービスです(YouTube・Twitch との連携機能そのものは Discord が提供しています)。紹介はしますが、推奨や保証はしません。

## 要点

- 会員制サーバーは「**会員だけが見られるチャンネル**」と「**会員にロールを付ける仕組み**」の組み合わせで作る
- 会員サービスの中には、**支援しているプランに合わせて、Discordのロールを自動で付けたり外したりできる**ものがある。これを使うと、会員の管理を手作業でしなくて済む
- 自動連携があるのは、Patreon、pixivFANBOX、Ci-en、Ko-fi など。**noteのメンバーシップは、招待URLを特典にできるだけ**(ロールの自動連携は見つからなかった)

## サービスごとの対応状況(2026-11-04 時点で調べた内容)

| サービス | ロールの自動連携 | 内容 |
|---|---|---|
| **Patreon** | あり(公式) | 支援のTier(プラン)ごとにロールを対応させる。Patreon のBotがロールを管理する |
| **pixivFANBOX** | あり(公式) | 支援プランに合ったロールが自動で付く。**支援者が10人以上いるクリエイターだけ**が使える |
| **Ci-en** | あり(公式) | プランに応じてロールを自動で付け、プラン変更でロールも変わる |
| **Ko-fi** | あり(公式) | 支援者・メンバーにロールと招待を出せる。Ko-fi のBotがロールを付ける |
| **note メンバーシップ** | 見つからず | Discordの招待URLを、メンバーだけが見られる特典として置くことはできる。ロールは手動で管理する |
| **Fantia** | 見つからず | 公式の連携機能の情報は見つからなかった |
| **YouTube メンバーシップ** | あり(Discordの公式連携) | **YouTubeパートナー**のチャンネルだけが使える |
| **Twitch サブスク** | あり(Discordの公式連携) | 「Twitch Subscriber」などのロールが自動で作られ、管理される |

## 連携するときの共通の注意

- 連携用のBotのロールは、**ロール一覧で、Botが管理するロールより上**に置く。下にあると、ロールを付けられない(Patreon、Ko-fi の公式ヘルプより)
- Botが自動で管理するのは、連携に使うロールだけ。ほかのロールは手動で管理する
- 退会した人のロールがいつ外れるかは、サービスごとに違う(FANBOX は、解約した月の末まで残り、翌月の初めに外れる)

## サービスごとのメモ

### Patreon
- Patreon のBotに必要な権限は「ロールの管理」と「招待の作成」(公式ヘルプより。日本語の表記は未確認)
- 1つのサーバーに連携できるPatreonのページ(キャンペーン)は1つだけ
- Tierを選ばずに金額だけ決めて支援した人(カスタム支援)には、ロールが付かない

### pixivFANBOX
- 支援者は、FANBOXの設定でDiscordアカウントを連携し、クリエイターのページの「プラン」から Discordサーバーに入る。入ると、支援中のプランのロールが自動で付く
- 提供開始時は「一部のクリエイターを対象に」という告知だった

### Ci-en
- 支援者はDiscordのアカウントをクリエイターに教えなくてよい。招待リンクが広まっても、有料プランの人以外は入れないようにできる(2021年のニュース記事より)

### note メンバーシップ
- 特典として、Discordの招待URLをメンバーだけに見せられる
- Discordの招待リンクは、初期設定では期限がある。期限なしにしておかないと、あとから入った人が使えない
- 退会した人を外す作業は、手動になる

## メモ

- この記事は各サービスの公式ヘルプ・お知らせ・ニュース記事をもとにまとめたもので、実機では未確認
- 各サービスの機能や条件はよく変わる。使う前に、それぞれの公式ヘルプで確認する
- 「会員だけが見られるチャンネル」の作り方(ロールとチャンネル権限の設定)は、まだ記事がない
