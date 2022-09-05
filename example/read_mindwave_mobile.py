import time
import bluetooth
import requests
import json
from collections import OrderedDict

import mindwavemobile.MindwaveDataPoints
from mindwavemobile.MindwaveDataPoints import RawDataPoint
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import textwrap

def toNodeRequest(key: str, value):
    jsonData = {
        key: value
    }
    headers = {'content-type':'application/json'}

    # print(jsonData)

    requests.get('http://192.168.10.11:3002/BCI', json=jsonData, headers=headers)


if __name__ == '__main__':
    mindwaveDataPointReader = MindwaveDataPointReader()
    mindwaveDataPointReader.start()

    if (mindwaveDataPointReader.isConnected()):    
        while(True):
            dataPoint = mindwaveDataPointReader.readNextDataPoint()
            if (not dataPoint.__class__ is RawDataPoint):
                if (dataPoint.__class__ is mindwavemobile.MindwaveDataPoints.MeditationDataPoint):
                    # print(str(type(mindwavemobile.MindwaveDataPoints.MeditationDataPoint(dataPoint).meditationValue)))
                    # print(mindwavemobile.MindwaveDataPoints.MeditationDataPoint(dataPoint).meditationValue)

                    value = "{0}".format(dataPoint)
                    toNodeRequest('Meditation', value)

                elif (dataPoint.__class__ is mindwavemobile.MindwaveDataPoints.AttentionDataPoint):
                    value = "{0}".format(dataPoint)
                    toNodeRequest('Attention', value)

                elif (dataPoint.__class__ is mindwavemobile.MindwaveDataPoints.EEGPowersDataPoint):
                    value = "{0}".format(dataPoint)
                    toNodeRequest('EEG', value)

                elif (dataPoint.__class__ is mindwavemobile.MindwaveDataPoints.PoorSignalLevelDataPoint):
                    value = "{0}".format(dataPoint)
                    toNodeRequest('PoorSignal', value)

                print(type(dataPoint), ' ', dataPoint)
            # else:
            #normal signal data
            #     print(dataPoint)
    else:
        print((textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " ")))
        

