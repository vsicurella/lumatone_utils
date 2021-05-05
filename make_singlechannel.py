#!/usr/bin/env python3

import sys

# TODO: better argument parsing & help
#       channel overflow options

multichannelPeriod = int(sys.argv[1])
multichannelRootChannel = int(sys.argv[2])
multichannelZeroOffset = int(sys.argv[5]) % 128

singlechannelRootChannel = int(sys.argv[3])
singlechannelRootNote = int(sys.argv[4])

for filename in sys.argv[6:]:
    with open(filename) as input_file:
        output_filename = filename[:-4] + '_singlechannel.ltn'
        with open(output_filename, 'w', newline=('\r\n')) as output_file:
            keyConfig = {}
            for line in input_file:
                if not line.startswith('[Board') and not line.startswith('Col_'):
                    if line.startswith('Key_'):
                        keyConfig = {}
                        prefix, pitch = line.strip().split('=')
                        keyConfig['keyPrefix'] = prefix
                        keyConfig['note'] = (int(pitch) - multichannelZeroOffset) % multichannelPeriod
                        continue
                    if line.startswith('Chan_'):
                        prefix, channel = line.strip().split('=')
                        keyConfig['channelPrefix'] = prefix
                        keyConfig['channel'] = int(channel)
                    if len(keyConfig) == 4:
                        channelOffset = keyConfig['channel'] - multichannelRootChannel
                        newNote = (channelOffset * multichannelPeriod) + keyConfig['note'] + singlechannelRootNote

                        channelFlow = newNote // 128
                        newChannel = singlechannelRootChannel + channelFlow
                        newNote %= 128

                        if (newChannel < 1):
                            newChannel += 16

                        keyLine = '{}={}\n'.format(keyConfig['keyPrefix'], newNote)
                        channelLine = '{}={}\n'.format(keyConfig['channelPrefix'], newChannel)
                        output_file.write(keyLine)
                        output_file.write(channelLine)
                else:
                    output_file.write(line)
        print("Saved {}".format(output_filename))