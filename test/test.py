from __future__ import print_function
import ncepbufr

hdstr='SID XOB YOB DHR TYP ELV SAID T29'
obstr='POB QOB TOB ZOB UOB VOB PWO MXGS HOVI CAT PRSS TDO PMO'
qcstr='PQM QQM TQM ZQM WQM NUL PWQ PMQ'
oestr='POE QOE TOE NUL WOE NUL PWE     '

# read prepbufr file.

bufr = ncepbufr.open('prepbufr')
bufr.dump_table('prepbufr.table')
bufr.print_table() # print embedded table
while bufr.advance() == 0: # loop over messages.
    print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
    #bufr.read_subset(obstr) # should raise subset not loaded error
    while bufr.load_subset() == 0: # loop over subsets in message.
        hdr = bufr.read_subset(hdstr)
        station_id = hdr[0].tostring()
        obs = bufr.read_subset(obstr)
        nlevs = obs.shape[-1]
        oer = bufr.read_subset(oestr)
        qcf = bufr.read_subset(qcstr)
        print('station_id, lon, lat, time, station_type, levels =',\
        station_id,hdr[1].item(),hdr[2].item(),hdr[3].item(),int(hdr[4].item()),nlevs)
        for k in range(nlevs):
            if nlevs > 1:
                print('level',k+1)
            print('obs',obs[:,k])
            print('oer',oer[:,k])
            print('qcf',qcf[:,k])
    # stop after first 2 messages.
    if bufr.msg_counter == 2: break
bufr.close()
