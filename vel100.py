import argparse
import mido

parser = argparse.ArgumentParser()
parser.add_argument("-vo", "--velocity", required=False, type=int, default=None)
parser.add_argument("-do", "--device-out", required=False, default="24:0")
parser.add_argument("-di", "--device-in", required=False, default="128:0")

args = parser.parse_args() 

inn = [i for i in mido.get_input_names() if args.device_in in i][0]
inport = mido.open_input(inn)

outt = [i for i in mido.get_output_names() if args.device_out in i][0]
outport = mido.open_output(outt)

for msg in inport:
    if msg.type == 'note_on' and msg.velocity > 0:
        if args.velocity: msg.velocity = args.velocity

    outport.send(msg)
