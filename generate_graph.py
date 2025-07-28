import datetime
import json
from typing import Literal, Optional

import plotext
import matplotlib.pyplot as plt


def generate_graph(
    duration: int, 
    json_path: str ='food_record.json', 
    output_format: Literal['ascii', 'png'] ='ascii',
    png_save_path: Optional[str] = None,
):
    """
    Generate calorie summary graph over a date range using the user's food records.
    Each day's total calorie intake is calculated and visualized, regardless of meal type.

    Args:
        duration        : Number of past days to generate the graph, including today
        json_path       : Path to JSON file containing the food records
        output_format   : Specify 'ascii' to return the graph as an ASCII string, or
                          'png' to save the graph as a PNG file and return its file path
        png_save_path   : Specify path of PNG file to save to if output_format='png', else
                          defaults to 'graph.png' in current directory
    Returns:
        An ASCII string or the path of the saved PNG file.
    """
    with open(json_path, 'r') as f:
        records = json.load(f)

    date_list = [
        (datetime.date.today() - datetime.timedelta(days=i)).isoformat() 
        for i in range(duration - 1, -1, -1)
    ]
    graph_data = {date: 0 for date in date_list}
    for date in graph_data:
        if date in records:
            graph_data[date] += records[date]['total_calories']

    stats = {
        'average': round( sum(graph_data.values()) / len(graph_data) ),
        'min': min(graph_data.values()),
        'max': max(graph_data.values())
    }

    title = f'Calorie Summary Graph Over Past {duration} Days'
    xlabel = 'Date'
    ylabel = 'Total daily calories'
    if output_format == 'ascii':
        plotext.plot_size(100, 20)
        
        plotext.plot(list(graph_data.values()))
        plotext.xticks(ticks=list(range(1, duration + 1)), labels=list(graph_data))
        plotext.xlabel(xlabel)
        plotext.ylabel(ylabel)
        plotext.title(title)

        return {
            'ascii': plotext.build(),
            'summary': stats,
        }
    
    elif output_format == 'png':
        if png_save_path is None:
            png_save_path = 'graph.png'

        plt.figure(figsize=(14, 5))

        plt.plot(list(graph_data), list(graph_data.values()), 'o-')
        plt.xticks(rotation=45)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        plt.tight_layout()
        plt.savefig(png_save_path, dpi=300)
        
        return {
            'png_path': png_save_path,
            'summary': stats
        }

    else:
        raise ValueError(f"The parameter output_format must be one of 'ascii', 'png'")
