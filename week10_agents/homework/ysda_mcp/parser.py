from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests

def parse_tasks() -> list[dict[str, str]]:
    load_dotenv()
    lk_cookie = os.getenv("LK_SESSION_COOKIE")

    url = "https://lk.dataschool.yandex.ru/learning/assignments/"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; parser/1.0)"
    }

    session = requests.Session()
    if lk_cookie:
        session.cookies.set('Session_id', lk_cookie, domain='.yandex.ru')

    resp = session.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    html = resp.text

    soup = BeautifulSoup(html, "html.parser")
    try:
        open_tasks_table = soup.find("h3", string="Открытые задания").find_next("table")
    except AttributeError:
        raise RuntimeError("Could not find the open tasks table on the page. Check your cookie")

    tasks = []

    for row in open_tasks_table.find_all("tr"):
        date_block = row.find("div", class_="assignment-date")
        if date_block:
            date = date_block.find("span", class_="nowrap").get_text(strip=True)
            time = date_block.get_text(strip=True).replace(date, "")
            deadline = f"{date} {time.strip()}"
        else:
            deadline = None

        assignment_link = row.find_all("a")[0]
        course_link = row.find_all("a")[1]

        assignment_name = assignment_link.get_text(strip=True)
        course_name = course_link.get_text(strip=True)

        tasks.append({
            "course": course_name,
            "assignment": assignment_name,
            "deadline": deadline
        })

    for t in tasks:
        print(f"{t['course']}: {t['assignment']} — {t['deadline']}")

    return tasks


# TODO: Implement function to get a list of upcoming lectures from learning/timetable/
def parse_lectures() -> list[dict[str, str]]:
    load_dotenv()
    lk_cookie = os.getenv("LK_SESSION_COOKIE")

    url = "https://lk.dataschool.yandex.ru/learning/timetable/?year=2025&week=49"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; parser/1.0)"
    }

    session = requests.Session()
    if lk_cookie:
        session.cookies.set('Session_id', lk_cookie, domain='.yandex.ru')

    resp = session.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    html = resp.text

    soup = BeautifulSoup(html, "html.parser")



    timetable_tables = soup.find_all("table", class_="timetable")
    if not timetable_tables:
        raise RuntimeError("Could not find timetable. Check your cookie.")

    lectures = []

    for table in timetable_tables:
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) != 5:  
                continue

            time = cols[0].get_text(strip=True)

            name_link = cols[1].find("a")
            course_link = cols[2].find("a")
            badge = cols[4].find("span")

            if not (name_link and course_link and badge):
                continue

            lecture_type = badge.get_text(strip=True)

           
            '''if "лекц" not in lecture_type.lower():
                continue'''

            location = cols[3].get_text(strip=True)

            lectures.append({
                "course": course_link.get_text(strip=True),
                "lecture": name_link.get_text(strip=True),
                "time": time,
                "location": location,
                "type": lecture_type
            })

    for l in lectures:
        print(f"{l['course']}: {l['lecture']} — {l['time']} ({l['location']})")

    return lectures
