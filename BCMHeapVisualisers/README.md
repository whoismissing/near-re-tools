https://project-zero.issues.chromium.org/42450052#attachment59035499

firmware heap visualisers.

 - [create_dot_graph.py](./create_dot_graph.py) : Creates a "dot" graph containing the heap's free-chunks
 - [create_html_main_chunk.py](./create_html_main_chunk.py) : Creates an HTML visualisation of the heap's main region
 - [create_html_total.py](./create_html_total.py) : Created an HTML visualisation of the entire heap
 - [create_trace_html.py](./create_trace_html.py) : Creates an HTML visualisation for traces from the malloc/free patches
 - [profiles.py](./profiles.py) : The symbols for each firmware "profile"
 - [utils.py](./utils.py) : Utilities related to handling a firmware snapshot
