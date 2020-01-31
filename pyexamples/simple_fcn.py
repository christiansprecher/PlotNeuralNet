
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( 'room.png', name='input_img'),

    #block-001
    to_ConvConvRelu( name='ccr_b1', s_filer='I', n_filer=(16,16), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption='conv1'),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),    

    # to_ConvConvRelu( name='ccr_b2', s_filer='I/2', n_filer=(32,32), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=32, depth=32, caption='conv2'),
    # to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    # to_ConvConvRelu( name='ccr_b3', s_filer='I/4', n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption='conv3'),
    # to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    # to_ConvConvRelu( name='ccr_b4', s_filer='I/8', n_filer=(128,128), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption='conv4'),
    # to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    # to_ConvConvRelu( name='ccr_b5', s_filer='I/16', n_filer=(256,256), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption='conv5'),
    # to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),
    
    *block_2ConvPool( name='b2', botton='pool_b1', top='pool_b2', s_filer='I/2', n_filer=(32,32), offset="(1,0,0)", size=(32,32,2.5), opacity=0.5,caption='conv2'),
    *block_3ConvPool( name='b3', botton='pool_b2', top='pool_b3', s_filer='I/4', n_filer=(64,64,64), offset="(1,0,0)", size=(25,25,3.5), opacity=0.5 ,caption='conv3'),
    *block_3ConvPool( name='b4', botton='pool_b3', top='pool_b4', s_filer='I/8',  n_filer=(128,128,128), offset="(1,0,0)", size=(16,16,4.5), opacity=0.5 ,caption='conv4'),
    *block_3ConvPool( name='b5', botton='pool_b4', top='pool_b5', s_filer='I/16',  n_filer=(256,256,256), offset="(1,0,0)", size=(12,12,5.5), opacity=0.5,caption='conv5'),

    to_Conv( name='c_b5', s_filer='I/16', n_filer=(16), offset="(1,0,0)", to="(pool_b5-east)", width=2, height=12, depth=12, caption=''),
    # to_ConvRes( name='cr_b5', s_filer='I/16', n_filer=(16), offset="(0,0,0)", to="(c_b5-east)", width=3.5, height=12, depth=12, caption=''),
    to_connection('pool_b5','c_b5'),
    to_DeConv( name='dc_b5', s_filer='I/8', n_filer=(16), offset="(1.0,0,0)", to="(c_b5-east)", width=2, height=16, depth=16, caption=''),
    to_dotted('c_b5','dc_b5'),
    to_connection('c_b5','dc_b5'),

    to_Conv( name='c_b4', s_filer='I/8', n_filer=(16), offset="(0,4,0)", to="(dc_b5-west)", width=2, height=16, depth=16, caption=''),
    to_side( of='pool_b4', to='c_b4', of_offset = 0.5 , of_width = 1, to_width = 2, offset = 6.9),

    to_plus(name = 'plus_b4', to='(dc_b5-east)', offset='(1.5,0,0)'),
    to_connection('dc_b5','plus_b4'),
    to_sidetop('c_b4','plus_b4', of_width=2, offset = 1.5),

    ########################################### ASPP
    # Path B
    to_Conv( name='aspp_b1', s_filer='', n_filer=32, offset="(3.5,3,0)", to="(plus_b4-east)", width=2.5, height=16, depth=16, caption=' '),
    to_Conv( name='aspp_b2', s_filer='', n_filer=32, offset="(0,0,0)", to="(aspp_b1-east)", width=2.5, height=16, depth=16, caption='dilation3'),
    to_Conv( name='aspp_b3', s_filer='', n_filer=32, offset="(0,0,0)", to="(aspp_b2-east)", width=2.5, height=16, depth=16, caption=' '),
    to_Conv( name='aspp_b4', s_filer='I/8', n_filer=16, offset="(0,0,0)", to="(aspp_b3-east)", width=2, height=16, depth=16, caption=' '),
    to_side( of='plus_b4', to='aspp_b1', of_offset = 2 , of_width = 5, to_width = 2.5, offset = 3.5),

    # Path C
    to_Conv( name='aspp_c1', s_filer='', n_filer=32, offset="(3.5,-3,0)", to="(plus_b4-east)", width=2.5, height=16, depth=16, caption=' '),
    to_Conv( name='aspp_c2', s_filer='', n_filer=32, offset="(0,0,0)", to="(aspp_c1-east)", width=2.5, height=16, depth=16, caption='dilation6'),
    to_Conv( name='aspp_c3', s_filer='', n_filer=32, offset="(0,0,0)", to="(aspp_c2-east)", width=2.5, height=16, depth=16, caption=' '),
    to_Conv( name='aspp_c4', s_filer='I/8', n_filer=16, offset="(0,0,0)", to="(aspp_c3-east)", width=2, height=16, depth=16, caption=' '),
    to_side( of='plus_b4', to='aspp_c1', of_offset = 2, of_width = 5, to_width = 2.5, offset = 3.5),

    # Path D
    to_Conv( name='aspp_d1', s_filer='', n_filer=32, offset="(3.5,-9.0,0)", to="(plus_b4-east)", width=2.5, height=16, depth=16, caption=' '),
    to_Conv( name='aspp_d2', s_filer='', n_filer=32, offset="(0,0,0)", to="(aspp_d1-east)", width=2.5, height=16, depth=16, caption='dilation12'),
    to_Conv( name='aspp_d3', s_filer='', n_filer=32, offset="(0,0,0)", to="(aspp_d2-east)", width=2.5, height=16, depth=16, caption=' '),
    to_Conv( name='aspp_d4', s_filer='I/8', n_filer=16, offset="(0,0,0)", to="(aspp_d3-east)", width=2, height=16, depth=16, caption=' '),
    to_side( of='plus_b4', to='aspp_d1', of_offset = 2 , of_width = 5, to_width = 2.5, offset = 3.5),

    # Path A
    to_Conv( name='aspp_a4', s_filer='I/8', n_filer=32, offset="(0.0,6.0,0)", to="(aspp_b4-west)", width=2, height=16, depth=16, caption='dilation1'),
    to_side( of='plus_b4', to='aspp_a4', of_offset = 2 , of_width = 5, to_width = 2, offset = 5),

    # to_ConvConvConvConvRelu( name='aspp_b', s_filer='I/8', n_filer=(32,32,32,16), offset="(1,3,0)", to="(plus_b4-east)", width=(2.5,2.5,2.5,2), height=16, depth=16, caption='dil3'),
    
    # Concatenation
    to_Conv( name='aspp_con1', s_filer='', n_filer='', offset="(2.25,-3,0)", to="(aspp_b4-east)", width=0.5, height=12, depth=12, opacity = 0.2, caption=' '),
    to_Conv( name='aspp_con2', s_filer='', n_filer='', offset="(0.15,0,0)", to="(aspp_con1-east)", width=0.5, height=12, depth=12, opacity = 0.2, caption=' '),
    to_Conv( name='aspp_con3', s_filer='', n_filer='', offset="(0.15,0,0)", to="(aspp_con2-east)", width=0.5, height=12, depth=12, opacity = 0.2, caption=' '),
    to_Conv( name='aspp_con4', s_filer='', n_filer='', offset="(0.15,0,0)", to="(aspp_con3-east)", width=0.5, height=12, depth=12, opacity = 0.2, caption=' '),
    to_Conv( name='aspp_con_env', s_filer='I/8', n_filer='64', offset="(-0.15,0,0)", to="(aspp_con1-west)", width=5.75, height=16, depth=16, opacity = 0.5, caption='concatenation'),
    
    to_sidetop('aspp_a4','aspp_con_env', of_width=2, offset = 2.675),
    to_sidetop('aspp_b4','aspp_con_env', of_width=2, offset = 2.675),
    to_sidebottom('aspp_c4','aspp_con_env', of_width=2, offset = 2.675),
    to_sidebottom('aspp_d4','aspp_con_env', of_width=2, offset = 2.675),

    to_Conv( name='aspp_con_conv', s_filer='I/8', n_filer='16', offset="(3.5,0,0)", to="(aspp_con_env-east)", width=2, height=16, depth=16, caption=''),
    to_connection('aspp_con_env','aspp_con_conv'),


    #Decoder
    to_DeConv( name='decoder', s_filer='', n_filer=(16), offset="(3.5,0,0)", to="(aspp_con_conv-east)", width=2, height=40, depth=40, caption='upsampling'),
    to_Conv( name='output', s_filer='I', n_filer='(1)', offset="(0,0,0)", to="(decoder-east)", width=1, height=40, depth=40, caption=''),
    to_dotted('aspp_con_conv','decoder'),
    to_connection('aspp_con_conv','decoder'),

    
    #output
    to_input( 'edge.png', to = '(39,0,0)', name='output_img'),




    # to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),

    # *block_2ConvPool( name='b7', top='pool_b7', s_filer='I/16',  n_filer=(256,256,256), offset="(1,10,0)", size=(12,12,3.5), opacity=0.5,),
    # to_skip( of='ccr_b2', to='ccr_b4', pos=1.25),

    # # to_ConvConvRelu( name='ccr_b8', s_filer='I', n_filer=(16,16), offset="(15,10,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption='conv1'),
    # to_ConvConvRelu( name='ccr_b8', s_filer='I', n_filer=(16,16), offset="(1,5,0)", to="(pool_b4-east)", width=(2,2), height=12, depth=12, caption='conv1'),
    # to_Pool(name="pool_b8", offset="(0,0,0)", to="(ccr_b8-east)", width=1, height=10, depth=10, opacity=0.5),

    # # to_side( of='pool_b4', to='ccr_b8', pos1 = 11 , pos2 =  0),
    # to_side( of='pool_b4', to='ccr_b8', of_offset = 0.2 , of_width = 1, to_width = 4, offset = 1),
    
    # *block_Unconv( name="b6", botton="ccr_b5", top='end_b6', s_filer='I/16',  n_filer=, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    # # to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    # to_skip( of='ccr_b4', to='ccr_res_b5', pos=1.25),

    # #Bottleneck
    # #block-005
    # to_ConvConvRelu( name='ccr_b5', s_filer=32, n_filer=(1024,1024), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck"  ),
    # to_connection( "pool_b4", "ccr_b5"),

    # #Decoder
    # *block_Unconv( name="b6", botton="ccr_b5", top='end_b6', s_filer=64,  n_filer=512, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    # to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    # *block_Unconv( name="b7", botton="end_b6", top='end_b7', s_filer=128, n_filer=256, offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    # to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),    
    # *block_Unconv( name="b8", botton="end_b7", top='end_b8', s_filer=256, n_filer=128, offset="(2.1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    # to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),    
    
    # *block_Unconv( name="b9", botton="end_b8", top='end_b9', s_filer=512, n_filer=64,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5 ),
    # to_skip( of='ccr_b1', to='ccr_res_b9', pos=1.25),
    
    # to_ConvSoftMax( name="soft1", s_filer=512, offset="(0.75,0,0)", to="(end_b9-east)", width=1, height=40, depth=40, caption="SOFT" ),
    # to_connection( "end_b9", "soft1"),
     
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
