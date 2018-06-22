#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from gooey import Gooey, GooeyParser

from dateutil import parser
import srt


 
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
        
        for srt_file in srts_list:
            srt_type = 'Open Camera'
            with open(srt_file, 'r') as myfile:
                data=myfile.read()#.replace('\n', '')
            subtitle_generator = srt.parse(data.decode('utf-8'))
            subtitles = list(subtitle_generator)
            for record in subtitles:
                print '-'
                #print record.content
                '''
                8 июня 2018 г. 11:44:33 AM
55,69177, 37,66464, 148,0м, 292°
'''
                data = dict()
                dt = parser.parse(record.content.split('\n')[0])
                data['date'] = 
                second_string = record.content.split('\n')[1]
                second_strint_spl = second_string.split(',')
                data['lat'] = second_strint_spl[0] + '.' + second_strint_spl[1]
                data['lon'] = second_strint_spl[2] + '.' + second_strint_spl[3]
                data['altitude'] = second_strint_spl[4]+'.'+second_strint_spl[5]
                data['dir'] = second_strint_spl[6]
                print data
     

if __name__ == '__main__':
  main()
