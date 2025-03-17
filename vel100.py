
import mido

inn = [i for i in mido.get_input_names() if "24:0" in i][0]
inport = mido.open_input(inn)

outt = [i for i in mido.get_output_names() if "128:0" in i][0]
outport = mido.open_output(outt)

for msg in inport:
    if msg.type == 'note_on' or msg.type == 'note_off':
        msg.velocity = 10
    outport.send(msg)
