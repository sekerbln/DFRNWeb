from scholarly import scholarly
from bs4 import BeautifulSoup
import re

# === 设置作者 Google Scholar ID ===
authors = {
    "Theodoros Dounas": "mP0ZiN4AAAAJ",
    "Davide Lombardi": "GHZNDcAAAAAJ",
    "Giancarlo Di Marco": "Cwc7tEIAAAAJ",
    "Jiří Vele": "8eg3EPsAAAAJ",
    # 如果以后找到 Hico McDonald 的 ID，在这里加上
}

# === 文件路径 ===
input_html = "publications.html"
output_html = "publications.html"

def fetch_publications(author_name, author_id):
    """从 Google Scholar 获取作者的最新出版物"""
    print(f"🔍 Fetching publications for {author_name}...")
    try:
        author = scholarly.search_author_id(author_id)
        scholarly.fill(author, sections=['publications'])
        publications = []
        for pub in author['publications'][:10]:  # 获取前 10 篇
            title = pub.get('bib', {}).get('title', 'Untitled')
            year = pub.get('bib', {}).get('pub_year', 'N/A')
            url = pub.get('pub_url', '#')
            publications.append({
                "title": title,
                "year": year,
                "url": url
            })
        return publications
    except Exception as e:
        print(f"❌ Error fetching {author_name}: {e}")
        return []

def build_publication_html():
    """生成 publications 的 HTML 块"""
    html_content = ""
    for author_name, author_id in authors.items():
        pubs = fetch_publications(author_name, author_id)
        if not pubs:
            continue
        html_content += f'<h2>{author_name}</h2>\n'
        for pub in pubs:
            html_content += f'''
            <div class="publication-item">
              <h3>{pub["title"]}</h3>
              <p>({pub["year"]})</p>
              <a href="{pub["url"]}" target="_blank">View on Google Scholar</a>
            </div>
            '''
    return html_content

def replace_publications_in_html(new_content):
    """替换 publications.html 中旧的 <div class="publication-list"> ... </div>"""
    with open(input_html, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    pub_section = soup.find("div", {"class": "publication-list"})
    if pub_section:
        pub_section.clear()  # 清空旧内容
        pub_section.append(BeautifulSoup(new_content, "html.parser"))
        print("✅ 已替换 publication-list 内容")
    else:
        print("⚠️ 未找到 <div class='publication-list'> ，将新建一个。")
        new_div = soup.new_tag("div", **{"class": "publication-list"})
        new_div.append(BeautifulSoup(new_content, "html.parser"))
        soup.body.append(new_div)

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(str(soup.prettify()))

    print(f"🎉 已更新 {output_html}")

if __name__ == "__main__":
    html_block = build_publication_html()
    replace_publications_in_html(html_block)
