#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from gooey import Gooey, GooeyParser

#from dateutil.parser import parser as dateutilparser
import dateutil.parser
from babel.core import Locale

#import dateutil
import srt
import os

import datetime
import gpxpy
import gpxpy.gpx

import re #for remove letters from altitude

 
running = True
def write_gpx(path, data):
    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for point in data:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
            point['lat'], point['lon'], elevation=point['altitude'], time=point[0]))

    with open(path, "w") as f:
        f.write(gpx.to_xml())
        
class LocalizedParserinfo(dateutil.parser.parserinfo):

    def __init__(self, locale):
        locale = Locale.parse(locale)
        # Build localized list of words, remove dots
        self.WEEKDAYS = [(locale.days['format']['wide'][i],
                          locale.days['format']['abbreviated'][i].rstrip('.'))
                          for i in range(7)]
        self.MONTHS = [(locale.months['format']['wide'][i],
                        locale.months['format']['abbreviated'][i].rstrip('.'))
                        for i in range(1, 13)]
        super(LocalizedParserinfo, self).__init__()

    def __call__(self):
        return self


class DatetimeParser(object):

    def __init__(self, locale):
        self.info = LocalizedParserinfo(locale)

    def parse(self, s):
        return dateutil.parser.parse(s, parserinfo=self.info)

        
def srt_only(str):
    if  os.path.splitext(str)[1].lower() == '.srt':
        return True
    else:
        return False
    
@Gooey(optional_cols=2, program_name="srt2gpx")
def main():
    settings_msg = "convert subtitles file with coorinates to gpx file \n" \
                 'New file will be saved to source folder'
    parser = GooeyParser(description=settings_msg)
    parser.add_argument('--verbose', help='be verbose', dest='verbose',
                      action='store_true', default=False)
    subs = parser.add_subparsers(help='commands', dest='command')

    srt2gpx_parser = subs.add_parser('srt2gpx', help='convert subtitles file with coorinates to gpx file')
    srt2gpx_parser.add_argument('srt',
                           
                           type=str, widget='MultiFileChooser')  

                           


    args = parser.parse_args()
    if args.command == 'srt2gpx':
        SRTS = args.srt
        srts_list = SRTS.split(";")
        srts_list = filter(srt_only, srts_list)
        
        for srt_file in srts_list:
            srt_type = 'Open Camera'
            with open(srt_file, 'r') as myfile:
                data=myfile.read()#.replace('\n', '')
                
            gpx_filename = os.path.splitext(srt_file)[0]+'.gpx'
            gpx = gpxpy.gpx.GPX()
            gpx_track = gpxpy.gpx.GPXTrack()
            gpx.tracks.append(gpx_track)
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)
            
            subtitle_generator = srt.parse(data.decode('utf-8'))
            subtitles = list(subtitle_generator)
            cnt = 0
            for record in subtitles:
                cnt +=1
                print cnt
                '''
                8 июня 2018 г. 11:44:33 AM
55,69177, 37,66464, 148,0м, 292°
'''
                data = dict()
                datestring = record.content.split('\n')[0]
                datestring = datestring.replace(u'г.',u'')
                datestring = datestring.replace(u'Г.',u'')
                sample = u'8 июня 2018 г.'
                dt = DatetimeParser('ru_RU').parse(datestring)

                second_string = record.content.split('\n')[1]
                #print second_string
                second_strint_spl = second_string.split(',')
                try:
                    data['lat'] = second_strint_spl[0] + '.' + second_strint_spl[1]
                    data['lon'] = second_strint_spl[2] + '.' + second_strint_spl[3]
                    #data['altitude'] = second_strint_spl[4]+'.'+second_strint_spl[5]
                    data['altitude'] = second_strint_spl[4]+'.' + re.sub("\D", "", second_strint_spl[5])
                    data['dir'] = second_strint_spl[6]              

                    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
                        data['lat'], data['lon'], data['altitude'], time=dt))
                except:
                    print 'wrong format record '+str(cnt)

            print 'write to'
            print gpx_filename
            with open(gpx_filename, "w") as f:
                f.write(gpx.to_xml())
            
     

if __name__ == '__main__':
  main()
