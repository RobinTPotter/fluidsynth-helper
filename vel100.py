import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-vo", "--velocity", required=False, type=int, default=None)
parser.add_argument("-vm", "--velocity-multiplier", required=False, type=float, default=1.0)
parser.add_argument("-do", "--device-out", required=False, default="128:0")
parser.add_argument("-di", "--device-in", required=False, default="24:0")
parser.add_argument("-nt", "--note-transpose", required=False, type=int, default=0)

args = parser.parse_args() 

print(args)

import mido

inn = [i for i in mido.get_input_names() if args.device_in in i][0]
inport = mido.open_input(inn)

outt = [i for i in mido.get_output_names() if args.device_out in i][0]
outport = mido.open_output(outt)

for msg in inport:
    if msg.type == 'note_on' and msg.velocity > 0:
        if args.velocity: msg.velocity = min(127,max(0,int(msg.velocity*args.velocity_multiplier + args.velocity)))
        msg.note = msg.note + args.note_transpose
    outport.send(msg)

