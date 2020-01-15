
import os

def to_head( projectpath ):
    pathlayers = os.path.join( projectpath, 'layers/' ).replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image 
"""

def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}
\def\DcnvColor{rgb:blue,5;green,2.5;white,5}
\def\SumColor{rgb:blue,5;green,15}   
"""

def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""

# layers definition

def to_input( pathfile, to='(-3,0,0)', width=8, height=8, name="temp" ):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
"""

# Conv
def to_Conv( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, opacity = 0.5, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +""",
        opacity="""+ str(opacity) +""",
        }
    };
"""

# Conv
def to_DeConv( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\DcnvColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu( name, s_filer=256, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer[0]) +""", """+ str(n_filer[1]) +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""

def to_ConvConvConvRelu( name, s_filer=256, n_filer=(64,64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2,2), height=40, depth=40, caption=" " ):    
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer[0]) +""", """+ str(n_filer[1]) +""", """+ str(n_filer[2]) +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""", """+ str(width[2]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""

def to_ConvConvConvConvRelu( name, s_filer=256, n_filer=(64,64,64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2,2,2), height=40, depth=40, caption=" " ):    
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer[0]) +""", """+ str(n_filer[1]) +""", """+ str(n_filer[2]) +""", """+ str(n_filer[3]) +"""  }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""", """+ str(width[2]) +""" , """+ str(width[3]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""

# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+name+""",
        caption="""+ caption +r""",
        fill=\PoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# unpool4, 
def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+ name +r""",
        caption="""+ caption +r""",
        fill=\UnpoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""



def to_ConvRes( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name + """,
        caption="""+ caption + """,
        xlabel={{ """+ str(n_filer) + """, }},
        zlabel="""+ str(s_filer) +r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


# ConvSoftMax
def to_ConvSoftMax( name, s_filer=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# SoftMax
def to_SoftMax( name, s_filer=10, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        xlabel={{" ","dummy"}},
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


def to_connection( of, to):
    return r"""
\draw [connection]  ("""+of+"""-east)    -- node {\midarrow} ("""+to+"""-west);
"""

def to_skip( of, to, pos=1.25):
    return r"""
\path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
\path ("""+ to +"""-south)  -- ("""+ to +"""-north)  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-top) ;
\draw [connection]  ("""+of+"""-northeast)  
-- node {\midarrow}("""+of+"""-top)
-- node {\midarrow}("""+to+"""-top)
-- node {\midarrow} ("""+to+"""-north);
"""

def to_side( of, to, of_offset = 0.25, of_width = 1, to_width = 4, offset = 1):
    pos1 = 1 + of_offset / of_width * 5
    pos2 = 1 + (offset - of_offset) / to_width * 5

    return r"""
\path ("""+ of +"""-west) -- ("""+ of +"""-east) coordinate[pos="""+ str(pos1) +"""] ("""+ of +"""-east2) ;
\path ("""+ to +"""-east) -- ("""+ to +"""-west) coordinate[pos="""+ str(pos2) +"""] ("""+ to +"""-west2) ;
\draw [connection]  ("""+of+"""-east)  
-- node {}("""+of+"""-east2)
-- node {\midarrow}("""+to+"""-west2)
-- node {\midarrow} ("""+to+"""-west);
"""

def to_sidetop( of, to, of_width = 1, offset = 1):
    pos = 1 + offset / of_width * 5
    # pos2 = 1 + (offset - of_offset) / to_width * 5

    return r"""
\path ("""+ of +"""-west) -- ("""+ of +"""-east) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-east2) ;
\draw [connection]  ("""+of+"""-east)  
-- node {\midarrow}("""+of+"""-east2)
-- node {\midarrow} ("""+to+"""-north);
"""

def to_sidebottom( of, to, of_width = 1, offset = 1):
    pos = 1 + offset / of_width * 5
    # pos2 = 1 + (offset - of_offset) / to_width * 5

    return r"""
\path ("""+ of +"""-west) -- ("""+ of +"""-east) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-east2) ;
\draw [connection]  ("""+of+"""-east)  
-- node {\midarrow}("""+of+"""-east2)
-- node {\midarrow} ("""+to+"""-south);
"""

def to_dotted(of,to):
    return r"""
\draw[densely dashed]
("""+ of +"""-nearnortheast) -- ("""+ to +"""-nearnorthwest)
("""+ of +"""-nearsoutheast) -- ("""+ to +"""-nearsouthwest)
("""+ of +"""-farsoutheast) -- ("""+ to +"""-farsouthwest)
("""+ of +"""-farnortheast) -- ("""+ to +"""-farnorthwest)
;
"""

def to_plus(to, offset, name, radius = 2.5, symbol = '+'):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
{Ball={
    name=""" + name +""",
    fill=\SumColor,
    opacity=0.6,
    radius="""+ str(radius) +""",
    logo="""+ str(symbol) +""",
    }
};
"""


def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""


def to_generate( arch, pathname="file.tex" ):
    with open(pathname, "w") as f: 
        for c in arch:
            print(c)
            f.write( c )
     


