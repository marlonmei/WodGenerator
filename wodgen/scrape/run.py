import csv
from datetime import datetime
from secrets import (
    SCRAPER_URL,
    WORKOUT_TITLE_CLASS,
    WORKOUT_DESCRIPTION_CLASS, PATH_PROCESSED
)
from config import CSV_FILENAME, CSV_ENCODING
from scraper import WorkoutScraper, StringProcessor

if __name__ == '__main__':

    starttime = datetime.now()
    print(starttime)
    wod_scraper = WorkoutScraper()
    wod_scraper.extract_raw_content(url=SCRAPER_URL)

    titles = wod_scraper.extract_class_content(
        title_class=WORKOUT_TITLE_CLASS,
        html_tag='div'
    )
    titles = wod_scraper.simple_strip_of_list(
        list_of_strings=titles
    )
    descriptions = wod_scraper.extract_class_content(
        title_class=WORKOUT_DESCRIPTION_CLASS,
        html_tag='p'
    )
    descriptions = wod_scraper.simple_strip_of_list(
        list_of_strings=descriptions
    )

    string_processor = StringProcessor()

    titles = string_processor.process_extensively(
        list_of_strings=titles
    )
    descriptions = string_processor.process_extensively(
        list_of_strings=descriptions
    )

    with open(
            file=f'{PATH_PROCESSED}/{CSV_FILENAME}',
            mode='w',
            newline='',
            encoding=CSV_ENCODING
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["name", "description", "time", "type"])
        for title, description in zip(titles, descriptions):
            writer.writerow([title, description])


    print(len(titles))
    print(len(descriptions))
    endtime = datetime.now()
    print(endtime)
    print(f'total duration: {endtime - starttime}')
