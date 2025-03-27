
"""
import vel100
args = vel100.get_args()
# fiddle with args
main(args)
"""
import threading

def main(args, stop_event):
    print(args)
    import mido
    inn = [i for i in mido.get_input_names() if args.device_in in i][0]
    inport = mido.open_input(inn)
    outt = [i for i in mido.get_output_names() if args.device_out in i][0]
    outport = mido.open_output(outt)
    print(f"opening {outport} with {args} and {stop_event}")

    try:
        while not stop_event.is_set():
            msg = inport.poll()
            if msg:
                print(msg)
                if msg.type == 'note_on' and msg.velocity > 0:
                    if args.velocity: msg.velocity = min(127,max(0,int(msg.velocity*args.velocity_multiplier + args.velocity)))
                    msg.note = msg.note + args.note_transpose
                outport.send(msg)
    except Exception as e:
        print(e)
    finally:
        inport.close()
        outport.close()


def start_thread(args, stop_event):
    t = threading.Thread(target=main, args=(args, stop_event,))
    t.start()
    return t

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-vo", "--velocity", required=False, type=int, default=None)
    parser.add_argument("-vm", "--velocity-multiplier", required=False, type=float, default=1.0)
    parser.add_argument("-do", "--device-out", required=False, default="128:0")
    parser.add_argument("-di", "--device-in", required=False, default="24:0")
    parser.add_argument("-nt", "--note-transpose", required=False, type=int, default=0)
    parser.add_argument("-e", "--echo", required=False, default=None)
    args, unk = parser.parse_known_args() 
    return args

if __name__ == "__main__":
    args = get_args()
    main(args)
