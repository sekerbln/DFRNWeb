from scholarly import scholarly
from bs4 import BeautifulSoup

# 🧩 作者列表（使用 Google Scholar ID）
AUTHORS = [
    {"name": "Theodoros Dounas", "id": "mP0ZiN4AAAAJ"},
    {"name": "Davide Lombardi", "id": "GHZNDcAAAAAJ"},
    {"name": "Jiří Vele", "id": "8eg3EPsAAAAJ"},
    {"name": "Giancarlo Di Marco", "id": "Cwc7tEIAAAAJ"},
]

# 🧩 初始化 HTML 容器
soup = BeautifulSoup("<div class='publication-list'></div>", "html.parser")
pub_list = soup.div

for person in AUTHORS:
    print(f"🔍 Fetching author: {person['name']} ...")
    try:
        # 通过 ID 直接抓取数据（比搜索名字更稳定）
        author = scholarly.search_author_id(person['id'])
        author = scholarly.fill(author, sections=['publications'])
        print(f"✅ Found author: {author['name']}")

        # 添加作者标题
        header = soup.new_tag('h2')
        header.string = author['name']
        pub_list.append(header)

        # 遍历每篇论文
        for pub in author['publications'][:10]:  # 仅显示前 10 篇
            title = pub.get('bib', {}).get('title', 'Untitled')
            year = pub.get('bib', {}).get('pub_year', '—')
            venue = pub.get('bib', {}).get('venue', '')
            pub_url = pub.get('pub_url', '#')

            pub_div = soup.new_tag('div', **{'class': 'publication-item'})
            
            # 标题
            title_tag = soup.new_tag('h3')
            title_tag.string = title
            pub_div.append(title_tag)

            # 期刊/会议 + 年份
            meta_p = soup.new_tag('p')
            meta_p.string = f"{venue} ({year})"
            pub_div.append(meta_p)

            # 链接
            link_a = soup.new_tag('a', href=pub_url, target='_blank')
            link_a.string = "View on Google Scholar"
            pub_div.append(link_a)

            pub_list.append(pub_div)

    except Exception as e:
        print(f"❌ Error fetching {person['name']}: {e}")
        continue

# 🧩 输出 HTML 文件
with open("publications_generated.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("🎉 Done! File saved as publications_generated.html")
