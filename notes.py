#!/usr/bin/env python3
"""my-discord-notes の記事を管理するスクリプト。

使い方:
    python3 notes.py status [--todo] [--thirdparty]
                                        記事の一覧(verified / checked / 外部サービス)を表示する
    python3 notes.py check              記事の frontmatter と README の目次を検査する
    python3 notes.py toc                README と index.md(サイトのトップ)の目次を記事から作り直す
    python3 notes.py new SLUG TITLE [SUMMARY]
                                        テンプレートから新しい記事を作り、目次も更新する
    python3 notes.py verify FILE VALUE  記事の verified を変え、checked を今日にする

外部ライブラリは使わない(Python 3 の標準機能だけで動く)。
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
README = ROOT / "README.md"
INDEX = ROOT / "index.md"  # GitHub Pages のトップページ
TEMPLATE = DOCS / "_template.md"

REQUIRED = ["title", "summary", "keywords", "checked", "verified", "source"]
# thirdparty も必須だが、空のリスト [] を許すので REQUIRED とは別に検査する
NOTICE_PHRASE = "Discordの公式機能ではありません"
VERIFIED_VALUES = ["実機", "一部実機", "ネットのみ"]
STALE_DAYS = 180  # checked がこれより古ければ警告する

TOC_START = "<!-- toc:start -->"
TOC_END = "<!-- toc:end -->"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
FILENAME_RE = re.compile(r"^(\d{2})-[a-z0-9-]+\.md$")
# YAML では、この文字で始まる値は引用符で囲まないとエラーになる(GitHub Pages のビルドが失敗する)
YAML_RESERVED_START = "@`!&*|>%{}"


# ---------------------------------------------------------------- 読み書き

def parse_frontmatter(text):
    """記事冒頭の frontmatter を辞書にする。

    このリポジトリで使う書き方だけに対応する:
      key: 値
      key: [a, b, c]
      key:
        - 値
        - 値
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    data = {}
    current = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        item = re.match(r"^\s+-\s*(.*)$", line)
        if item and current is not None:
            if not isinstance(data[current], list):
                data[current] = []
            data[current].append(unquote(item.group(1).strip()))
            continue
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if not kv:
            continue
        key, value = kv.group(1), kv.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            value = [unquote(v.strip()) for v in value[1:-1].split(",") if v.strip()]
        else:
            value = unquote(value)
        data[key] = value
        current = key
    return data


def articles():
    """docs/ の記事(_ で始まるファイルを除く)を番号順に返す。"""
    return sorted(p for p in DOCS.glob("*.md") if not p.name.startswith("_"))


def unquote(value):
    """前後の引用符("..." または '...')を取り除く。"""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def yaml_unsafe_values(text):
    """frontmatter の中で、引用符なしで YAML の予約文字から始まる値を返す。"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return []
    values = []
    for line in m.group(1).splitlines():
        item = re.match(r"^\s+-\s*(.*)$", line)
        kv = re.match(r"^[A-Za-z_]+:\s*(.*)$", line)
        raw = item.group(1) if item else kv.group(1) if kv else ""
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            values += [v.strip() for v in raw[1:-1].split(",")]
        else:
            values.append(raw)
    return [v for v in values if v and v[0] in YAML_RESERVED_START]


def load(path):
    return parse_frontmatter(path.read_text(encoding="utf-8"))


def rel(path):
    return path.relative_to(ROOT).as_posix()


def today():
    return datetime.date.today()


# ---------------------------------------------------------------- 目次

def build_toc():
    """README 用の目次(ファイル名と説明)。AI がファイル名で記事を探せるようにする。"""
    lines = ["| ファイル | 内容 |", "|---|---|"]
    for path in articles():
        fm = load(path) or {}
        summary = fm.get("summary") or fm.get("title") or ""
        lines.append(f"| `{rel(path)}` | {summary} |")
    return "\n".join(lines)


def build_index_toc():
    """index.md(サイトのトップ)用の目次。記事へのリンク付き。"""
    lines = ["| 記事 | 内容 |", "|---|---|"]
    for path in articles():
        fm = load(path) or {}
        title = fm.get("title") or path.stem
        summary = fm.get("summary") or ""
        lines.append(f"| [{title}]({rel(path)}) | {summary} |")
    return "\n".join(lines)


def with_toc(text, toc):
    """text の目次部分を toc に置きかえた全文を返す。マーカーが無ければ None。"""
    pattern = re.compile(re.escape(TOC_START) + r".*?" + re.escape(TOC_END), re.S)
    if not pattern.search(text):
        return None
    block = f"{TOC_START}\n{toc}\n{TOC_END}"
    return pattern.sub(lambda _: block, text, count=1)


def toc_targets():
    """目次を持つファイルと、その目次の作り方。"""
    return [(README, build_toc), (INDEX, build_index_toc)]


# ---------------------------------------------------------------- サードパーティ

def check_thirdparty_notice(text, names):
    """外部サービスを扱う記事の注意書きを検査する。問題があればその説明、なければ None。

    注意書きは、見出し(# ...)の直後の引用(> ...)に置き、
    NOTICE_PHRASE と、thirdparty に書いたサービス名をすべて含める。
    """
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    lines = [l for l in body.splitlines() if l.strip()]
    if not lines or not lines[0].startswith("# "):
        return "本文の最初の行を「# タイトル」にする"
    notice = []
    for line in lines[1:]:
        if not line.startswith(">"):
            break
        notice.append(line)
    notice = " ".join(notice)
    if NOTICE_PHRASE not in notice:
        return f"外部サービスを扱う記事は、タイトルの直後に「{NOTICE_PHRASE}」を含む注意書き(> で始まる行)を置く"
    missing = [n for n in names if n not in notice]
    if missing:
        return f"注意書きに thirdparty のサービス名がない: {', '.join(missing)}"
    return None


# ---------------------------------------------------------------- コマンド

def cmd_status(args):
    rows = []
    for path in articles():
        fm = load(path) or {}
        verified = fm.get("verified", "?")
        if args.todo and verified == "実機":
            continue
        thirdparty = fm.get("thirdparty") or []
        if args.thirdparty and not thirdparty:
            continue
        extra = f"  [外部: {', '.join(thirdparty)}]" if thirdparty else ""
        rows.append((path.name, verified, fm.get("checked", "?"), fm.get("title", "?") + extra))
    if not rows:
        print("該当する記事はありません。")
        return 0
    w0 = max(len(r[0]) for r in rows)
    w1 = max(len(r[1]) for r in rows)
    for name, verified, checked, title in rows:
        # 全角文字を含むので、列ぞろえは目安
        print(f"{name.ljust(w0)}  {verified.ljust(w1, '　')}  {checked}  {title}")
    return 0


def cmd_check(args):
    errors, warnings = [], []
    names = set()
    template = load(TEMPLATE) or {}

    for path in articles():
        name = rel(path)
        if not FILENAME_RE.match(path.name):
            errors.append(f"{name}: ファイル名は「2桁の番号-英小文字.md」にする(例: 06-voice-robotic.md)")
        else:
            num = path.name[:2]
            if num in names:
                errors.append(f"{name}: 番号 {num} がほかの記事と重複している")
            names.add(num)

        fm = load(path)
        if fm is None:
            errors.append(f"{name}: 冒頭に frontmatter(--- で囲んだ部分)がない")
            continue

        for key in REQUIRED:
            if not fm.get(key):
                errors.append(f"{name}: {key} がない、または空")

        if FILENAME_RE.match(path.name):
            expected = str(int(path.name[:2]))
            if fm.get("nav_order") != expected:
                errors.append(f"{name}: nav_order はファイル名の番号と同じ {expected} にする(サイトのメニューの並び順)")

        for v in yaml_unsafe_values(path.read_text(encoding="utf-8")):
            errors.append(f"{name}: 「{v}」は記号で始まるので引用符で囲む(例: \"{v}\")。囲まないとサイトのビルドが失敗する")

        if "thirdparty" not in fm:
            errors.append(f"{name}: thirdparty がない(外部サービスを扱わないなら thirdparty: [] と書く)")
        else:
            thirdparty = fm["thirdparty"]
            if not isinstance(thirdparty, list):
                errors.append(f"{name}: thirdparty は [Craig, Patreon] のようにリストで書く")
            elif thirdparty:
                problem = check_thirdparty_notice(path.read_text(encoding="utf-8"), thirdparty)
                if problem:
                    errors.append(f"{name}: {problem}")

        for key in ("title", "summary", "keywords", "source"):
            if fm.get(key) and fm.get(key) == template.get(key):
                errors.append(f"{name}: {key} がテンプレートのまま")

        verified = fm.get("verified")
        if verified and verified not in VERIFIED_VALUES:
            errors.append(f"{name}: verified は {' / '.join(VERIFIED_VALUES)} のどれか(今は「{verified}」)")

        checked = fm.get("checked")
        if checked:
            try:
                d = datetime.date.fromisoformat(checked)
                age = (today() - d).days
                if age > STALE_DAYS:
                    warnings.append(f"{name}: checked が {age} 日前({checked})。内容を見直す")
                if age < 0:
                    errors.append(f"{name}: checked が未来の日付({checked})")
            except ValueError:
                errors.append(f"{name}: checked は YYYY-MM-DD 形式にする(今は「{checked}」)")

    for target, build in toc_targets():
        if not target.exists():
            errors.append(f"{rel(target)}: ファイルがない")
            continue
        current = target.read_text(encoding="utf-8")
        updated = with_toc(current, build())
        if updated is None:
            errors.append(f"{rel(target)}: 目次のマーカー({TOC_START} / {TOC_END})がない")
        elif updated != current:
            errors.append(f"{rel(target)}: 目次が記事と合っていない → python3 notes.py toc で直せる")

    for w in warnings:
        print(f"注意: {w}")
    for e in errors:
        print(f"エラー: {e}")
    if not errors and not warnings:
        print(f"OK: 記事 {len(articles())} 本、問題なし")
    elif not errors:
        print(f"OK(注意 {len(warnings)} 件)")
    return 1 if errors else 0


def cmd_toc(args):
    status = 0
    for target, build in toc_targets():
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        updated = with_toc(current, build())
        if updated is None:
            print(f"エラー: {rel(target)} に目次のマーカー({TOC_START} / {TOC_END})がない")
            status = 1
        elif updated == current:
            print(f"{rel(target)} の目次は最新です。")
        else:
            target.write_text(updated, encoding="utf-8")
            print(f"{rel(target)} の目次を更新しました。")
    return status


def cmd_new(args):
    if not re.match(r"^[a-z0-9-]+$", args.slug):
        print("エラー: SLUG は英小文字・数字・ハイフンだけにする(例: voice-chat)")
        return 1
    numbers = [int(p.name[:2]) for p in articles() if FILENAME_RE.match(p.name)]
    num = max(numbers, default=0) + 1
    path = DOCS / f"{num:02d}-{args.slug}.md"
    if path.exists():
        print(f"エラー: {rel(path)} はすでにある")
        return 1

    text = TEMPLATE.read_text(encoding="utf-8")
    text = re.sub(r"^title: .*$", f"title: {args.title}", text, count=1, flags=re.M)
    text = re.sub(r"^nav_order: .*$", f"nav_order: {num}", text, count=1, flags=re.M)
    if args.summary:
        text = re.sub(r"^summary: .*$", f"summary: {args.summary}", text, count=1, flags=re.M)
    text = re.sub(r"^checked: .*$", f"checked: {today().isoformat()}", text, count=1, flags=re.M)
    text = re.sub(r"^verified: .*$", "verified: ネットのみ", text, count=1, flags=re.M)
    text = text.replace("# (記事タイトル)", f"# {args.title}", 1)
    path.write_text(text, encoding="utf-8")
    print(f"{rel(path)} を作りました。")

    cmd_toc(args)
    print("keywords・source などを書いたら、python3 notes.py check で確認してください。")
    return 0


def cmd_verify(args):
    if args.value not in VERIFIED_VALUES:
        print(f"エラー: VALUE は {' / '.join(VERIFIED_VALUES)} のどれか")
        return 1
    path = Path(args.file)
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    if not path.exists():
        # ファイル名だけ(例: 04-webhooks.md)でも受け付ける
        path = DOCS / Path(args.file).name
    if not path.exists():
        print(f"エラー: {args.file} が見つからない")
        return 1

    text = path.read_text(encoding="utf-8")
    if load(path) is None:
        print(f"エラー: {rel(path)} に frontmatter がない")
        return 1
    m = FRONTMATTER_RE.match(text)
    head = m.group(0)
    head = re.sub(r"^verified: .*$", f"verified: {args.value}", head, count=1, flags=re.M)
    head = re.sub(r"^checked: .*$", f"checked: {today().isoformat()}", head, count=1, flags=re.M)
    path.write_text(head + text[m.end():], encoding="utf-8")
    print(f"{rel(path)}: verified を「{args.value}」、checked を {today().isoformat()} にしました。")
    print("source に「実機で確認」を書いたか確認してください。")
    return 0


def main():
    parser = argparse.ArgumentParser(description="my-discord-notes の記事を管理する")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("status", help="記事の一覧を表示する")
    p.add_argument("--todo", action="store_true", help="verified が「実機」でない記事だけ表示する")
    p.add_argument("--thirdparty", action="store_true", help="外部サービス(thirdparty)を扱う記事だけ表示する")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("check", help="frontmatter と README・index.md の目次を検査する")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("toc", help="README と index.md の目次を作り直す")
    p.set_defaults(func=cmd_toc)

    p = sub.add_parser("new", help="テンプレートから新しい記事を作る")
    p.add_argument("slug", help="ファイル名の英語部分(例: voice-chat)")
    p.add_argument("title", help="記事のタイトル")
    p.add_argument("summary", nargs="?", help="目次に載せる一行の説明")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("verify", help="verified を変えて checked を今日にする")
    p.add_argument("file", help="記事のファイル(例: docs/04-webhooks.md)")
    p.add_argument("value", help=" / ".join(VERIFIED_VALUES))
    p.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
