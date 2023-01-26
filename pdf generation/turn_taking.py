import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time

import matplotlib.ticker as ticker

import matplotlib.ticker as ticker

def create_turn_taking_panel(conversation):
    # create a mapping of speakers to numerical values
    speaker_map = {"Speaker 1": 0, "Speaker 2": 1}

    # extract data from conversation
    speakers = [x[0] for x in conversation]
    start_times = [x[1] for x in conversation]
    end_times = [x[2] for x in conversation]
    
    # create figure and axis
    fig, ax = plt.subplots()
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Speaker 1", "Speaker 2"])
    ax.set_xlabel("Time (mm:ss)")
    ax.grid(True)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda sec, _: time.strftime("%M:%S", time.gmtime(sec))))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.FixedLocator([i for i in range(0, int(max(end_times)), 15)]))
    
    # plot segments for each turn
    for i in range(len(conversation)):
        start_time = start_times[i]
        end_time = end_times[i]
        speaker = speakers[i]
        # use the numerical value from the speaker_map dictionary
        ax.broken_barh([(start_time, end_time - start_time)], (speaker_map[speaker], 1), facecolors='blue')
    
    # display plot
    plt.show()


conversation = [("Speaker 1", 0, 12), ("Speaker 2", 12, 24), ("Speaker 1", 24, 30), ("Speaker 2", 30, 67)]
create_turn_taking_panel(conversation)
