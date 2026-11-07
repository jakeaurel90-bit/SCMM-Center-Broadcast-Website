"""
patch_announcements.py
Splits OFFICIAL ANNOUNCEMENTS from the random POSTS.

After this patch there are four sections:
    Live Program, Adventist News, Announcements, Post

It builds on the two earlier patches, so run those first:
    python patch_sections.py     (dashboard, index.html)
    python patch_viewer.py       (public page, viewer.html)
Then run:
    python patch_announcements.py

It patches index.html and viewer.html in the project folder and in
broadcast\\templates\\broadcast\\, saving a .bak backup of each first.
Existing posts keep their category. Old posts with no category stay in Post,
and the "Move to" dropdown on each card moves them to Announcements.
"""
import os
import shutil

BT = os.path.join("broadcast", "templates", "broadcast")
FILES = [
    "index.html", os.path.join(BT, "index.html"),
    "viewer.html", os.path.join(BT, "viewer.html"),
]

CATS_OLD = "['live', 'news', 'post'].includes(p.category)"
CATS_NEW = "['live', 'news', 'announce', 'post'].includes(p.category)"

DASH = {
    "base": "scmm-sections:start",
    "done": 'data-section="announce"',
    "edits": [
        ("post: { name: 'Post', sub: 'Announcements and general updates.',",
         "announce: { name: 'Announcements', sub: 'Official announcements for the mission.', heading: '+ Add Announcement', hint: 'Write the announcement here, or paste a link (optional)...', empty: 'No announcements yet. Publish the first one above.' },\n"
         "            post: { name: 'Post', sub: 'Random posts and general updates.',"),
        ('<button type="button" data-section="post">Post <span class="sub-count" id="count-post">0</span></button>',
         '<button type="button" data-section="announce">Announcements <span class="sub-count" id="count-announce">0</span></button>\n'
         '                    <button type="button" data-section="post">Post <span class="sub-count" id="count-post">0</span></button>'),
        ('<option value="post">Post</option>',
         '<option value="announce">Announcements</option>\n                            <option value="post">Post</option>'),
        (CATS_OLD, CATS_NEW),
        ("const c = { live: 0, news: 0, post: 0 };", "const c = { live: 0, news: 0, announce: 0, post: 0 };"),
        ('.section-nav button[data-section="news"]::before{background:var(--accent-gold)}',
         '.section-nav button[data-section="news"]::before{background:var(--accent-gold)}\n'
         '.section-nav button[data-section="announce"]::before{background:#8ecae6}'),
    ],
}

VIEW = {
    "base": "scmm-viewer-sections:start",
    "done": 'data-v="announce"',
    "edits": [
        ("post: { name: 'Announcements', empty: 'No announcements right now. Please check back soon.' }",
         "announce: { name: 'Announcements', empty: 'No announcements right now. Please check back soon.' },\n"
         "            post: { name: 'Posts', empty: 'No posts right now. Please check back soon.' }"),
        (CATS_OLD, CATS_NEW),
        ("const by = { live: [], news: [], post: [] };", "const by = { live: [], news: [], announce: [], post: [] };"),
        ("curTab = by.live.length ? 'live' : by.news.length ? 'news' : 'post';",
         "curTab = by.live.length ? 'live' : by.news.length ? 'news' : by.announce.length ? 'announce' : 'post';"),
        ('<button type="button" data-v="post" aria-selected="false">Announcements <em class="v-count-post">0</em></button>',
         '<button type="button" data-v="announce" aria-selected="false">Announcements <em class="v-count-announce">0</em></button>\n'
         '                <button type="button" data-v="post" aria-selected="false">Posts <em class="v-count-post">0</em></button>'),
        ('<button type="button" data-v="post">Announcements <em class="v-count-post">0</em></button>',
         '<button type="button" data-v="announce">Announcements <em class="v-count-announce">0</em></button>\n'
         '                <button type="button" data-v="post">Posts <em class="v-count-post">0</em></button>'),
        ("(isLive ? 'Latest live program' : 'Latest news')",
         "(isLive ? 'Latest live program' : curTab === 'announce' ? 'Latest announcement' : 'Latest news')"),
        ('.section-nav button[data-v="news"]::before{background:var(--accent-gold)}',
         '.section-nav button[data-v="news"]::before{background:var(--accent-gold)}\n'
         '.section-nav button[data-v="announce"]::before{background:#8ecae6}'),
    ],
}


def patch(path):
    if not os.path.exists(path):
        return True
    spec = DASH if os.path.basename(path) == "index.html" else VIEW
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if spec["done"] in text:
        print(f"  already patched: {path}")
        return True
    if spec["base"] not in text:
        earlier = "patch_sections.py" if spec is DASH else "patch_viewer.py"
        print(f"  skipped: {path}  (run {earlier} on it first)")
        return True
    problems = []
    for old, _ in spec["edits"]:
        n = text.count(old)
        if n != 1:
            problems.append((old.strip().splitlines()[0][:70], n))
    if problems:
        print(f"  NOT patched: {path}")
        for snippet, n in problems:
            print(f"    expected 1 match, found {n}: {snippet}")
        print("    (nothing was changed in this file)")
        return False
    for old, new in spec["edits"]:
        text = text.replace(old, new, 1)
    shutil.copy2(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  patched: {path}  (backup: {path}.bak)")
    return True


if __name__ == "__main__":
    print("Adding the Announcements section...")
    ok = all([patch(p) for p in FILES])
    print("Done." if ok else "Finished with problems, see above.")