import datetime
from datetime import time
from sqlalchemy import Time

def add_hours_to_time(time_str, hours):
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
    datetime_obj = datetime.datetime.combine(datetime.date.today(), time_obj)
    new_datetime_obj = datetime_obj + datetime.timedelta(hours=hours)
    return new_datetime_obj.time()


def convert_to_time(sublist):
    times = time(int(sublist[0] + sublist[1]), int(sublist[3] + sublist[4]), int(sublist[6] + sublist[7]))
    return Time(times)

def convert_sublist(input_array):
    converted_times = [convert_to_time(sublist) for sublist in input_array]
    return converted_times

"""import nltk
import spacy
# essential entity models downloads
nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.download('averaged_perceptron_tagger')


import locationtagger
place_entity = locationtagger.find_locations(text = address)


print(place_entity.countries)"""