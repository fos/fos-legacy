
def init():
    
    """
    
    Graph related
    -------------
    
    layout
        The layout algorithm used if node_position
        not given. Default: random
        From NetworkX: circular, random, shell, spring, spectral, fruchterman_reingold
        Else: ...
    
    Node related
    ------------
    node_position : (N,3)
        Node positions as ndarray
    
    node_label
        Node labels
    
    node_size
        The size of the node
        
    node_shape
        cube, sphere, pyramid, electrodes (cylinders)
        
    node_color : (N,3)
        The color of the nodes
        Either given [0,1] or [0,255]
        (or: cmap, vmin, vmax)
        
    node_alpha
        The node transparency
    
    -> node_color -> RGBA
    
    node_show_labels
        Show all labels on the nodes / 
        only for specified nodes.
        node_label has to be set
    
    Edge related
    ------------
    
    edge_directed : bool
        Interpret `edge_weight` as directed
    
    edge_weight : (M,1)
        The weight determines the width of the line
        
    edge_color
        The color of the edges
        (or cmap, vmin, vmax)
        
    edge_style
        solid, dashed, dotted, dashdot
        What does OpenGL support natively?
        
    edge_alpha
        The transparency of the edge
        
    edge_label
        The label for the edges
        
    
    Font related (global or per node/edge?)
    ------------
    
    font_size: int
       Font size for text labels (default=12)

    font_color: string
       Font color string (default='k' black)

    font_weight: string
       Font weight (default='normal')

    font_family: string
       Font family (default='sans-serif')
       
    """
    
    # open questions
    # - how to normalize the input node_position distribution
    # - pick a node / edge, show info, etc.
    # - dynamic graph with lifetime on nodes/edges
    # - hierarchic graph
    
    